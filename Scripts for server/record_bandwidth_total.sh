#!/bin/bash
# This script will record the total bandwidth going through the server. This also includes the data transferred when having cache hits.

bandwidth=$(cat /data/log/nginx/access.log | awk '{SUM+=$10}END{print SUM/1024/1024}')

echo $bandwidth 
#> ./bandwidth_total.txt
