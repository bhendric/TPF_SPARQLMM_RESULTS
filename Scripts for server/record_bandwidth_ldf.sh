#!/bin/bash
# This script will only record the bandwidth created by the ldf server and not by the caching server. 
# It thus gives us an oppertunity to determine how much data needs to be provided by the ldf server and how much caching can be done by running the total bandwidth recording next to this one
bandwidth=$(cat /data/log/nginx/access.log | awk '{if( $NF != "HIT") SUM+=$10;}END{print SUM/1024/1024}')

echo $bandwidth 
#> ./bandwidth_ldf.txt
