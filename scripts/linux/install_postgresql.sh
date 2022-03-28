#!/bin/bash

echo "======================================================"
echo "======================================================"
echo "installing postgresql"
echo "======================================================"
echo "======================================================"

sudo apt update
sudo apt install postgresql postgresql-contrib

echo "======================================================"
echo "======================================================"
echo "psql version:"
psql --version
echo "======================================================"
echo "======================================================"

sudo chmod 777 /etc/postgresql/12/main/pg_hba.conf
sudo sed -i "s/local   all             postgres                                peer/local   all             postgres                                md5/g" /etc/postgresql/12/main/pg_hba.conf
sudo systemctl start postgresql.service
sudo service postgresql status