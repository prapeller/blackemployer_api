source ../../venv/bin/activate

pushd $(pwd) >/dev/null
cd ../../app/settings/

db_name=`python -c "from dev_postgres import DATABASES; print(DATABASES['default']['NAME'])"`
#echo DB name: $db_name
db_user=`python -c "from dev_postgres import DATABASES; print(DATABASES['default']['USER'])"`
#echo DB user: $db_user
db_pass=`python -c "from dev_postgres import DATABASES; print(DATABASES['default']['PASSWORD'])"`
#echo DB pass: $db_pass

popd >/dev/null
