#!/bin/bash

echo "======================================================"
echo "======================================================"
echo "installing docker"
echo "======================================================"
echo "======================================================"

sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
echo "======================================================"
echo "======================================================"
echo "docker version:"
docker --version
echo "======================================================"
echo "======================================================"

echo "======================================================"
echo "======================================================"
echo "installing docker-compose"
echo "======================================================"
echo "======================================================"

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose;        # Apply executable permissions to the binary:
sudo usermod -aG docker $USER                       # to add myself to docker group
sudo chgrp docker /usr/local/bin/docker-compose     # to give docker-compose to docker group,
sudo chmod 750 /usr/local/bin/docker-compose        # to allow docker group users to execute it

echo "======================================================"
echo "======================================================"
echo "docker-compose version:"
docker-compose --version
echo "======================================================"
echo "======================================================"
