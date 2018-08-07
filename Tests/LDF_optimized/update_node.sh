sudo route del default gw 10.2.15.254 && sudo route add default gw 10.2.15.253
sudo route add -net 10.11.0.0 netmask 255.255.0.0 gw 10.2.15.254
sudo route add -net 10.2.32.0 netmask 255.255.240.0 gw 10.2.15.254
sudo npm cache clean -f
sudo npm install -g n
sudo n stable
