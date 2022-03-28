#!/bin/bash

echo "======================================================"
echo "======================================================"
echo "preparing development machine"
echo "======================================================"
echo "======================================================"

#pushd $(pwd) >/dev/null

./install_docker.sh
./install_postgresql.sh
./dp_create.sh

#popd >/dev/null