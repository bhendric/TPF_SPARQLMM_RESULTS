# Script to test the ldf implementation without optimization
# # -*- coding: utf-8 -*-
from paramiko import *
from scp import SCPClient
import csv
import numpy as np
import time
import threading
import os
import sys
import random
import pickle
import subprocess
from SPARQLWrapper import SPARQLWrapper, JSON
import traceback

global old_bandwidth
global queries
global output_file

def start_client(rejections, exec_times, seed, ip, number_of_clients):
    # SSH execute the client python file. This will create an output which will be the number of rejections. It will also create a file called times.txt which will contain all the execution times of the queries
    if ip == 'localhost':
        # Run the local client file
        # pass
        p = subprocess.Popen("python client_sparql.py " + str(seed) + " " + str(number_of_clients) + "", stdout=subprocess.PIPE, shell=True)
        (rejection, err) = p.communicate()
        p_status = p.wait()

        with open('times_' + str(seed) + '.txt', 'r') as csvfile:
            for line in csvfile:
                try:
                    exec_times.append(float(line))
                except ValueError:
                    pass
   	os.remove('times_' + str(seed) + '.txt')
 
    else:
        # Run the remote client file at the client with given ip
        client = SSHClient()
        client.load_system_host_keys()
        client.connect(ip, username=user, password=***REMOVED***)
        stdin,stdout,stderr = client.exec_command("python ./client_sparql.py " + str(seed) + " " + str(number_of_clients) + "")
        stdout.channel.recv_exit_status()
        rejection = stdout.read()

        scp = SCPClient(client.get_transport())
        scp.get('./times_' + str(seed) + '.txt')


        with open('times_' + str(seed) + '.txt', 'r') as csvfile:
            for line in csvfile:
                try:
                    exec_times.append(float(line))
                except ValueError:
                    pass

        client.exec_command("rm ~/times_" + str(seed) + ".txt")
        client.close()
        os.remove('times_' + str(seed) + '.txt')

    rejections.append(int(rejection))    


def monitor(clients):
    print "monitoring"
    global old_bandwidth
    host = "192.168.1.1"
    user = user
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(host, username=user, password=***REMOVED***)

    # Get the initial bandwidth so we can check how much is used with each run
    client.exec_command("nohup python3 cpurecord2.py \"$(pgrep 'java|postgres' | tr '\n' ' ')\" --interval 0.5 --log SPARQLMM.txt --include-children &")
    stdin,stdout,stderr = client.exec_command("~/record_bandwidth_total.sh")
    stdout.channel.recv_exit_status()
    old_bandwidth = float(stdout.read())

    clients.append(client)


def perform_parsing(client, exectime, number_of_executed, number_of_queried):
    print "Parsing results"
    global old_bandwidth
    cpu_error = False
   

    # get the CPU usage results
    # Try 5 times to get the cpu log file. If the sparqlmm server is too loaded, things can get pretty bad and we need some tries to get the file.
    for x in range(5):
        try:
            scp = SCPClient(client.get_transport())
            scp.get('~/SPARQLMM.txt')
            str_error = None
        
        except Exception as str_error:
            if x < 4:
                pass
            else:
                cpu_error = True
        
        if str_error:
            client.exec_command("nohup python3 cpurecord2.py \"$(pgrep 'java|postgres' | tr '\n' ' ')\" --interval 0.5 --log SPARQLMM.txt --include-children &")
	    time.sleep(10)
        else:
            break

    client.exec_command("pkill -f python3")
    if not cpu_error:
         # Stop the logging of the CPU and parse the data collected
        
        client.exec_command("rm ~/SPARQLMM.txt")
    
    # Get the bandwidth used
    stdin,stdout,stderr = client.exec_command("~/record_bandwidth_total.sh")
    stdout.channel.recv_exit_status()
    bandwidth = float(stdout.read())
    client.close()

    # The csv file has the following layout. Each second the cpu usage of all the
    # postgres and java processes are monitored and stored in the file. We thus get
    # the following:
    # second_1 PID CPU_Usage
    # second_1 PID CPU_Usage
    # etc
    # We thus have to take the sum of all the individual processes for each second
    # in order to get the total load of marmotta on the System.
    # After this, we will check what the maximum load has been and use this as the
    # CPU load for the query execution.
    results = []
    if not cpu_error:
        with open('SPARQLMM.txt', 'r') as csvfile:
            for line in csvfile:
                try:
                    results.append(float(line))
                except ValueError:
                    pass

    else:
        results.append(1500)


    # Divide by the number of cores of the machine to get the real CPU percentage
    if not results:
        results.append(0.0)
    results = np.array(results)

    # Divide by 16 because we have 16 cores to get to a percentage
    results = results/16.0

    print "Average query execution time for client: " + str(exectime)
    print "Number of clients with timeout/rejection: " + str(number_of_queried - number_of_executed)
    print "Maximum CPU Usage: " + str(np.max(results))
    print "Bandwidth used: " + str(bandwidth - old_bandwidth)

    with open(output_file + '_intermediate.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow([number_of_queried, number_of_queried - number_of_executed, exectime, np.max(results), bandwidth - old_bandwidth])

    result_bandwidth = bandwidth - old_bandwidth
    old_bandwidth = bandwidth
    
    os.remove('SPARQLMM.txt')
    print "Done parsing results\n\n"
    return number_of_queried - number_of_executed, exectime, np.max(results), result_bandwidth


if __name__ == '__main__':
    global output_file
    output_file = sys.argv[1]
    random.seed(3)
    try:
        with open ('queries.pkl', 'rb') as fp:
            for i in range(1, 40):
                aggregated_rejections = []
                aggregated_execution_time = []
                aggregated_CPU_usage = []
                aggregated_bandwidth = []
                for j in range(10):
                    print "Starting testing for " + str(5) + " simultaneous clients, " + str(i) + " each, round " + str(j)
                    threads = []
                    rejections = []
                    exec_times = []
                    clients = []
                    ips = ['localhost','192.168.1.3','192.168.1.4','192.168.1.5','192.168.1.6']

                    # Create a thread that will take the number of clients and perform the monitor function
                    monitoring_thread = threading.Thread(
                        target=monitor, args=(clients, ))

                    for j in range(5):
                        client = threading.Thread(target=start_client, args=(rejections, exec_times, random.randint(0,10000), ips[j], i))
                        threads.append(client)

                    monitoring_thread.start()
                    monitoring_thread.join()

                    # Wait a random between 10 and 100 milliseconds in order to lower the load a bit for the server and maybe get some more stable results
                    for thread in threads:
                        thread.start()


                    for thread in threads:
                        thread.join()
                    
                    rejections, execution_time, CPU_usage, bandwidth =  perform_parsing(clients[0], np.sum(exec_times) / len(exec_times), 5*i - np.sum(rejections), 5*i)
                    aggregated_rejections.append(rejections)
                    aggregated_execution_time.append(execution_time)
                    aggregated_CPU_usage.append(CPU_usage)
                    aggregated_bandwidth.append(bandwidth)
                    time.sleep(10)

                aggregated_bandwidth = np.array(aggregated_bandwidth)
                aggregated_CPU_usage = np.array(aggregated_CPU_usage)
                aggregated_execution_time = np.array(aggregated_execution_time)
                aggregated_rejections = np.array(aggregated_rejections)

                print "Parsing all rounds for " + str(5*i) + " clients:"
                print "Writing mean results of all rounds to file"
                with open(output_file + '.csv', 'a') as csvfile:
                    # Structure of csv file is as follows: number of clients, mean number of rejected, min number of rejected, max number of rejected, mean execution time, min execution time, max execution time, mean cpu usage, min cpu usage, max cpu usage, mean bandwidth, min bandwidth, max bandwidth
                    writer = csv.writer(csvfile, delimiter=";")
                    writer.writerow([5*i, int(np.mean(aggregated_rejections)), np.min(aggregated_rejections), np.max(aggregated_rejections), np.mean(aggregated_execution_time), np.min(aggregated_execution_time), np.max(aggregated_execution_time), np.mean(aggregated_CPU_usage), np.min(aggregated_CPU_usage), np.max(aggregated_CPU_usage), np.mean(aggregated_bandwidth), np.min(aggregated_bandwidth), np.max(aggregated_bandwidth)])
        
        print "Done\n\n"

    except Exception as e:
        #print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print(traceback.format_exc())
        pass
