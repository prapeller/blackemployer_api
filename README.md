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
cd ../../nginx
```
make 3 files here with ssl certificate info
1) blackemployer.com.crt
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
2) blackemployer.com.key
```
-----BEGIN RSA PRIVATE KEY-----
your key goes here
-----END RSA PRIVATE KEY-----

```
3) ca.crt
```
-----BEGIN CERTIFICATE-----
your root cert goes here
-----END CERTIFICATE-----
```
copy .env file with environment variables and fill it with your data
```
cp /blackemployer_api/app/app/settings/.env.example /blackemployer_api/app/app/settings/.env

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
cp app/settings/.env.example app/settings/.env
```
fill .env with your email host variables
```
cd app/
python manage.py migrate --settings="app.settings.dev_postgres"
python manage.py runserver --settings="app.settings.dev_postgres"
```
