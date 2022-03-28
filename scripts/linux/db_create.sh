#!/bin/bash

db_name=$"blackemployer_db"

cmd=$(<../postgres/db_create.sql)
cmd=$(echo $cmd | sed -e "s/\$db_name/$db_name/g")

echo "======================================================"
echo "======================================================"
echo "executing psql command: '$cmd'"
echo "======================================================"
echo "======================================================"
sudo -u postgres -H -- psql -c "$cmd"
