#!/bin/bash

echo "================================================================="
echo "| This script will apply requirements, migrations, static files |"
echo "================================================================="

#cwd=`cd $(dirname $0); pwd -P`
#echo "$cwd/$(basename $0)"
#cd $cwd
#pushd $cwd >/dev/null
#source $cwd/_env.sh
#cd ../..

pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic

echo "================================================================="
echo "| Migration complete |"
echo "================================================================="

#popd >/dev/null
