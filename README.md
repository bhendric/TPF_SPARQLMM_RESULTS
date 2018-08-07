# Results of SPARQL-MM enabled TPF client vs Apache Marmotta
This repository contains all the code and results for the performance results comparing the unoptimised and optimised TPF client with SPARQL-MM functionality with the Apache Marmotta implementation of SPARQL-MM.

The `Queries` folder contains Python scripts for creating query pickle files which are used during testing. These queries depend on the the optimisation we want to test.

The `Results` folder contains subfolders with jupyter notebooks creating graphs of the results retrieved from the servers.

The `Scripts for server` folder contains all shell scripts and configuration files used during testing in order to monitor and set up the server

The `Tests` folder contains subfolders for each experiment. It contains the Python scripts for both the monitoring client machine and the querying client machine. All the results of experiments are also aggregated in these folders.
