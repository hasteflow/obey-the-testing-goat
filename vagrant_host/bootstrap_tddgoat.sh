#!/usr/bin/env bash

sudo apt-get -y update
sudo apt-get -y install nginx
sudo add-apt-repository -y ppa:jonathonf/python-3.6
sudo apt-get -y update
sudo apt-get -y install python3.6 python3.6-venv
sudo apt-get -y install git


# configure hosts file for our internal network defined by Vagrantfile
cat >> /etc/hosts <<EOL

# vagrant environment nodes
10.0.15.10  tddgoatserver
EOL
