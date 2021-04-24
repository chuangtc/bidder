# bidder
Bidding server

## Introduction
It's interview test from [Bridgewell](https://www.bridgewell.com/en/). The assignment was giveen on 2021/4/16 evening, and the due date is 2021/4/26. The communication was done through slack.

## Design working environment
Ubuntu 20.04 LTS

Python 3.8

Django 3.2 LTS

## Install dependentable libraries
```bash
pip install Django==3.2
pip install protobuf
```

## Production environment steps
AWS EC2 (Ubuntu 20.04 LTS) 64-bit (x86) + Python 3.8 + Django 3.2 + Nginx 1.18 + Gunicorn 20.1 + Postgresql 12
```bash
ssh -i xxxxxx.pem ubuntu@public_IP_v4_address
# Inside Ubuntu server
sudo apt-get update
sudo apt-get upgrade
ssh-keygen -t rsa
sudo apt-get install python3-venv
git clone https://github.com/chuangtc/bidder.git
```
Start the interesting part
```bash
ubuntu@ip-172-31-9-189:~$ cd bidder/
ubuntu@ip-172-31-9-189:~/bidder$ python3 -m venv venv
ubuntu@ip-172-31-9-189:~/bidder$
ubuntu@ip-172-31-9-189:~/bidder$ source venv/bin/activate
(venv) ubuntu@ip-172-31-9-189:~/bidder$ python --version
Python 3.8.5
(venv) ubuntu@ip-172-31-9-189:~/bidder$ pip install Django==3.2
(venv) ubuntu@ip-172-31-9-189:~/bidder$ pip install protobuf
(venv) ubuntu@ip-172-31-9-189:~/bidder$ sudo apt-get install libpq-dev python-dev-is-python3
(venv) ubuntu@ip-172-31-9-189:~/bidder$ sudo apt-get install postgresql postgresql-contrib
(venv) ubuntu@ip-172-31-9-189:~/bidder$ sudo apt-get install nginx
(venv) ubuntu@ip-172-31-9-189:~/bidder$ sudo su - postgres
postgres@ip-172-31-9-189:~$ psql
postgres=# create database dsp_rtb;
postgres=# create user dsp_rtb with encrypted password 'password';
CREATE ROLE
postgres=# grant all privileges on database dsp_rtb to dsp_rtb;
GRANT
postgres=# exit
postgres@ip-172-31-9-189:~$ exit
(venv) ubuntu@ip-172-31-9-189:~/bidder$ pip install gunicorn
(venv) ubuntu@ip-172-31-9-189:~/bidder$ sudo apt-get install build-essential
(venv) ubuntu@ip-172-31-9-189:~/bidder$ pip install psycopg2
```
Modify /home/ubuntu/bidder/bidder/settings.py
```bash
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'dsp_rtb',
            'USER': 'dsp_rtb',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False
    ALLOWED_HOSTS = ['bridgewell.chuangtc.com']

```
Migration DB and create superuser
```bash
(venv) ubuntu@ip-172-31-9-189:~/bidder$ python manage.py makemigrations
No changes detected
(venv) ubuntu@ip-172-31-9-189:~/bidder$ python manage.py migrate
(venv) ubuntu@ip-172-31-9-189:~/bidder$ python manage.py createsuperuser
Username (leave blank to use 'ubuntu'): ubuntu
Email address:
Password:
Password (again):
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.

```
Test Gunicorn with Django 
```bash
(venv) ubuntu@ip-172-31-9-189:~/bidder$ gunicorn --bind 0.0.0.0:8000 bidder.wsgi
[2021-04-24 16:58:52 +0000] [21676] [INFO] Starting gunicorn 20.1.0
[2021-04-24 16:58:52 +0000] [21676] [INFO] Listening at: http://0.0.0.0:8000 (21676)
[2021-04-24 16:58:52 +0000] [21676] [INFO] Using worker: sync
[2021-04-24 16:58:52 +0000] [21678] [INFO] Booting worker with pid: 21678
```
