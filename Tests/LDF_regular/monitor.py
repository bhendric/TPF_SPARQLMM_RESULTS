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

global old_bandwidth_ldf
global old_bandwidth_total
global old_requests
global queries
global output_file

def start_client(rejections, exec_times, seed, ip, number_of_clients):
    # SSH execute the client python file. This will create an output which will be the number of rejections. It will also create a file called times.txt which will contain all the execution times of the queries
    if ip == 'localhost':
        # Run the local client file
        # pass
        p = subprocess.Popen("python client_ldf_regular.py " + str(seed) + " " + str(number_of_clients) + "", stdout=subprocess.PIPE, shell=True)
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
        stdin,stdout,stderr = client.exec_command("python ./client_ldf_regular.py " + str(seed) + " " + str(number_of_clients) + "")
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
    global old_bandwidth_ldf
    global old_bandwidth_total
    global old_requests
    host = "192.168.1.1"
    user = user
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(host, username=user, password=***REMOVED***)

    # Get the initial bandwidth so we can check how much is used with each run
    client.exec_command("nohup python3 cpurecord2.py \"$(pgrep 'node' | tr '\n' ' ')\" --interval 1 --log LDF.txt --include-children &")
    client.exec_command("nohup python3 cpurecord2.py \"$(pgrep 'nginx' | tr '\n' ' ')\" --interval 1 --log NGINX.txt --include-children &")
    # Check the bandwidth used by ldf server = cache misses
    stdin,stdout,stderr = client.exec_command("~/record_bandwidth_ldf.sh")
    stdout.channel.recv_exit_status()
    old_bandwidth_ldf = float(stdout.read())

    # Get global bandwidth usage = cache hits + misses
    stdin,stdout,stderr = client.exec_command("~/record_bandwidth_total.sh")
    stdout.channel.recv_exit_status()
    old_bandwidth_total = float(stdout.read())

    # Get number of requests done to server
    stdin,stdout,stderr = client.exec_command("~/record_requests.sh")
    stdout.channel.recv_exit_status()
    old_requests = int(stdout.read())

    clients.append(client)


def perform_parsing(client, exectime, number_of_executed, number_of_queried):
    print "Parsing results"
    global old_bandwidth_ldf
    global old_bandwidth_total
    global old_requests

    # Stop the logging of the CPU and parse the data collected
    client.exec_command("pkill -f python3")

    # get the CPU usage results
    for x in range(5):
        try:
            scp = SCPClient(client.get_transport())
            scp.get('~/LDF.txt')
            scp.get('~/NGINX.txt')
            str_error = None

        except Exception as str_error:
            if x < 4:
                pass
            else:
                raise
        
        if str_error:
            time.sleep(5)
        else:
            break

    client.exec_command("rm ~/LDF.txt")
    client.exec_command("rm ~/NGINX.txt")

    # Get the bandwidth used by ldf server = cache misses
    stdin,stdout,stderr = client.exec_command("~/record_bandwidth_ldf.sh")
    stdout.channel.recv_exit_status()
    bandwidth_ldf = float(stdout.read())

    # Get the global bandwidth usage = cache hits + misses
    stdin,stdout,stderr = client.exec_command("~/record_bandwidth_total.sh")
    stdout.channel.recv_exit_status()
    bandwidth_total = float(stdout.read())

    # Get number of requests done to server
    stdin,stdout,stderr = client.exec_command("~/record_requests.sh")
    stdout.channel.recv_exit_status()
    requests = int(stdout.read())


    # Rotate the access logs of nginx. Otherwise we will fill up our hdd with logs and crash the system
    stdin,stdout,stderr = client.exec_command("sudo rm /data/log/nginx/access.log")
    stdout.channel.recv_exit_status()

    stdin,stdout,stderr = client.exec_command("sudo kill -USR1 `cat /var/run/nginx.pid`")
    stdout.channel.recv_exit_status()

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
    results_LDF = []
    results_NGINX = []
    with open('LDF.txt', 'r') as csvfile:
        for line in csvfile:
            try:
                results_LDF.append(float(line))
            except ValueError:
                pass

    with open('NGINX.txt', 'r') as csvfile:
        for line in csvfile:
            try:
                results_NGINX.append(float(line))
            except ValueError:
                pass



    # Divide by the number of cores of the machine to get the real CPU percentage
    if not results_LDF:
        results_LDF.append(0.0)
    results_LDF = np.array(results_LDF)
    results_LDF = results_LDF/16.0

    if not results_NGINX:
        results_NGINX.append(0.0)
    results_NGINX = np.array(results_NGINX)
    results_NGINX = results_NGINX/16.0

    print "Average query execution time for client: " + str(exectime)
    print "Number of clients with timeout/rejection: " + str(number_of_queried - number_of_executed)
    print "Maximum CPU Usage LDF server: " + str(np.max(results_LDF))
    print "Maximum CPU Usage NGINX server: " + str(np.max(results_NGINX))
    print "Bandwidth used by ldf server: " + str(bandwidth_ldf - old_bandwidth_ldf)
    print "Bandwidth used in total between clients and server: " + str(bandwidth_total - old_bandwidth_total)
    print "Number of requests done to server: " + str(requests - old_requests)

    # CSV file contains following columns: number of clients, number of rejected clients, mean execution time, max CPU usage LDF server, max CPU usage NGINX server, bandwidth produced by LDF server (= cache misses), bandwidth produced in total by server (=cahce hits + misses), number of requests
    with open(output_file + '_intermediate.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow([number_of_queried, number_of_queried - number_of_executed, exectime, np.max(results_LDF), np.max(results_NGINX), bandwidth_ldf - old_bandwidth_ldf, bandwidth_total - old_bandwidth_total, requests - old_requests])

    bandwidth_result_ldf = bandwidth_ldf - old_bandwidth_ldf
    bandwidth_result_total = bandwidth_total - old_bandwidth_total
    requests_result = requests - old_requests
    old_bandwidth_ldf = bandwidth_ldf
    old_bandwidth_total = bandwidth_total
    old_requests = requests
    os.remove('LDF.txt')
    os.remove('NGINX.txt')
    print "Done parsing results\n\n"
    return number_of_queried - number_of_executed, exectime, np.max(results_LDF), np.max(results_NGINX), bandwidth_result_ldf, bandwidth_result_total, requests_result


if __name__ == '__main__':
    global output_file
    output_file = sys.argv[1]
    random.seed(3)
    try:
        with open ('queries.pkl', 'rb') as fp:
            with open(output_file + '.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=";")
                writer.writerow(["number of clients", "number of clients", "mean number of rejected", "min number of rejected", "max number of rejected", "mean execution time", "min execution time", "max execution time", "mean cpu usage ldf", "min cpu usage ldf", "max cpu usage ldf", "mean cpu usage nginx", "min cpu usage nginx", "max cpu usage nginx", "mean bandwidth ldf", "min bandwidth ldf", "max bandwidth ldf", "mean bandwidth total", "min bandwidth total", "max bandwidth total", "mean number of requests", "min number of requests", "max number of requests"])
            
            for i in range(1, 41):
                aggregated_rejections = []
                aggregated_execution_time = []
                aggregated_CPU_usage_ldf = []
                aggregated_CPU_usage_nginx = []
                aggregated_bandwidth_total = []
                aggregated_bandwidth_ldf = []
                aggregated_requests = []
                
                for j in range(5):
                    print "Starting testing for " + str(5) + " simultaneous clients, " + str(i) + " each, round " + str(j+1)
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
                    
                    rejections, execution_time, CPU_usage_ldf, CPU_usage_nginx ,bandwidth_ldf, bandwidth_total, request = perform_parsing(clients[0], np.sum(exec_times) / len(exec_times), 5*i - np.sum(rejections), 5*i)
                    aggregated_rejections.append(rejections)
                    aggregated_execution_time.append(execution_time)
                    aggregated_CPU_usage_ldf.append(CPU_usage_ldf)
                    aggregated_CPU_usage_nginx.append(CPU_usage_nginx)
                    aggregated_bandwidth_total.append(bandwidth_total)
                    aggregated_bandwidth_ldf.append(bandwidth_ldf)
                    aggregated_requests.append(request)
                    time.sleep(5)

                aggregated_bandwidth_total = np.array(aggregated_bandwidth_total)
                aggregated_bandwidth_ldf = np.array(aggregated_bandwidth_ldf)
                aggregated_CPU_usage_ldf = np.array(aggregated_CPU_usage_ldf)
                aggregated_CPU_usage_nginx = np.array(aggregated_CPU_usage_nginx)
                aggregated_execution_time = np.array(aggregated_execution_time)
                aggregated_rejections = np.array(aggregated_rejections)
                aggregated_requests = np.array(aggregated_requests)

                print "Parsing all rounds for " + str(5*i) + " clients:"
                print "Writing mean results of all rounds to file"
                with open(output_file + '.csv', 'a') as csvfile:
                    # Structure of csv file is as follows: number of clients, mean number of rejected, min number of rejected, max number of rejected, mean execution time, min execution time, max execution time, mean cpu usage ldf, min cpu usage ldf, max cpu usage ldf, mean cpu usage nginx, min cpu usage nginx, max cpu usage nginx, mean bandwidth ldf, min bandwidth ldf, max bandwidth ldf, mean bandwidth total, min bandwidth total, max bandwidth total, mean requests, min requests, max requests
                    writer = csv.writer(csvfile, delimiter=";")
                    writer.writerow([5*i, int(np.mean(aggregated_rejections)), np.min(aggregated_rejections), np.max(aggregated_rejections), np.mean(aggregated_execution_time), np.min(aggregated_execution_time), np.max(aggregated_execution_time), np.mean(aggregated_CPU_usage_ldf), np.min(aggregated_CPU_usage_ldf), np.max(aggregated_CPU_usage_ldf), np.mean(aggregated_CPU_usage_nginx), np.min(aggregated_CPU_usage_nginx), np.max(aggregated_CPU_usage_nginx), np.mean(aggregated_bandwidth_ldf), np.min(aggregated_bandwidth_ldf), np.max(aggregated_bandwidth_ldf), np.mean(aggregated_bandwidth_total), np.min(aggregated_bandwidth_total), np.max(aggregated_bandwidth_total), int(np.mean(aggregated_requests)), np.min(aggregated_requests), np.max(aggregated_requests)])
        print "Done\n\n"

    except Exception as e:
        #print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print(traceback.format_exc())
        pass
