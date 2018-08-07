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

def test_run(queue, query):
    begin = time.time()
    res = subprocess.check_output(["./TPF Client/bin/ldf-client", "http://192.168.1.1/images", "-q", query])
    end = time.time()
    queue.append(end - begin)

if __name__ == '__main__':
    seed = int(sys.argv[1])
    number_of_clients = int(sys.argv[2])
    random.seed(seed)
    try:
        with open ('queries.pkl', 'rb') as fp:
            queries = pickle.load(fp)
            threads = []
            q = []
            clients = []

            for j in range(number_of_clients):
                query = random.choice(queries)
                test = threading.Thread(target=test_run, args=(q, query,  ))
                threads.append(test)


            # Wait a random between 10 and 100 milliseconds in order to lower the load a bit for the server and maybe get some more stable results
            for thread in threads:
                thread.start()


            for thread in threads:
                thread.join()

            with open('times_' + str(seed) + '.txt', 'w') as csvfile:
                # Structure of csv file is as follows: number of clients, mean number of rejected, min number of rejected, max number of rejected, mean execution time, min execution time, max execution time, mean cpu usage, min cpu usage, max cpu usage, mean bandwidth, min bandwidth, max bandwidth
                writer = csv.writer(csvfile, delimiter=",")
                for time in q:
                    writer.writerow([time])

        print number_of_clients - len(q)

    except Exception as e:
        #print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
