# blackemployer.com
service for tracking potential employers and cases of communication with them))

if you give test task to developer-beginner and gives no feedback - you will be tracked here))

and other beginning developers will be able to search info about you first before start making your test task.

### Stack:

-gunicorn driven python in django framework

-docker-compose, nginx and bash scripts for deploy

-and a little of vanilla js and css in django-based frontend

## Deploy:

### to production remote host based on Ubuntu:
```
cd /
git clone git@github.com:prapeller/blackemployer_api.git
cd /blackemployer_api/scripts/linux
bash install_docker.sh
```

make 4 files locally

first 3 are with your ssl cert info for pasting to /blackemployer.com/nginx/
1) blackemployer.com.crt 

with content as follows >> 
```
-----BEGIN CERTIFICATE-----
your ssl cert goes here 
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
your intermidiate cert goes here
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
your root cert goes here
-----END CERTIFICATE-----
```

2) blackemployer.com.key << 

with content as follows >> 

```
-----BEGIN RSA PRIVATE KEY-----
your key goes here
-----END RSA PRIVATE KEY-----

```
3) ca.crt

with content as follows >> 
```
-----BEGIN CERTIFICATE-----
your root cert goes here
-----END CERTIFICATE-----

```
the 4th file with enviroment variables for pasting to /blackemployer_api/app/settings/
4) .env
with content based on .env.example file that you can find here >> 

```
nano /blackemployer_api/app/settings/.env.example
```
and finally run docker-compose file
```
cd /blackemployer_api/
docker-compose up
```

### to development local host based on Ubuntu:

```
git clone git@github.com:prapeller/blackemployer_api.git
sudo chmod 777 blackemployer_api
cd blackemployer_api/scripts/linux
bash install_postgresql.sh
bash db_create.sh
cd ../..
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic

cd app/
python manage.py runserver --settings="app.settings.dev_postgres"
```
