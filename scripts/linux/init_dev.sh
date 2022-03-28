#!/bin/bash

echo "======================================================"
echo "======================================================"
echo "preparing development machine"
echo "======================================================"
echo "======================================================"

#pushd $(pwd) >/dev/null

bash ./install_docker.sh
bash ./install_postgresql.sh
bash ./db_create.sh
bash ./migrate.sh

#popd >/dev/null