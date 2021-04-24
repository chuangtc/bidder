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
(venv) ubuntu@ip-172-31-9-189:~/bidder$ sudo apt-get install build-essential
(venv) ubuntu@ip-172-31-9-189:~/bidder$ pip install gunicorn
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
Modify  /etc/systemd/system/gunicorn.socket
```bash
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Modify /etc/systemd/system/gunicorn.service
```bash
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/bidder
ExecStart=/home/ubuntu/bidder/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          bidder.wsgi:application

[Install]
WantedBy=multi-user.target
```
We can now start and enable the Gunicorn socket. This will create the socket file at /run/gunicorn.sock now and at boot. When a connection is made to that socket, systemd will automatically start the gunicorn.service to handle it:
```bash
ubuntu@ip-172-31-9-189:~$ sudo systemctl start gunicorn.socket
ubuntu@ip-172-31-9-189:~$ sudo systemctl enable gunicorn.socket
```

Check the status of the process to find out whether it was able to start:
```bash
ubuntu@ip-172-31-9-189:~$ sudo systemctl status gunicorn.socket
```

Next, check for the existence of the gunicorn.sock file within the /run directory:
```bash
ubuntu@ip-172-31-9-189:~$ file /run/gunicorn.sock
/run/gunicorn.sock: socket
```
Currently, if you’ve only started the gunicorn.socket unit, the gunicorn.service will not be active yet since the socket has not yet received any connections. You can check this by typing:
```bash
ubuntu@ip-172-31-9-189:~$ sudo systemctl status gunicorn
● gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
     Active: active (running) since Sat 2021-04-24 20:56:58 UTC; 59s ago
TriggeredBy: ● gunicorn.socket
   Main PID: 24026 (gunicorn)
      Tasks: 4 (limit: 1160)
     Memory: 93.8M
     CGroup: /system.slice/gunicorn.service
             ├─24026 /home/ubuntu/bidder/venv/bin/python3 /home/ubuntu/bidder/venv/bin/gunicorn --access-logfile - --wor>
             ├─24038 /home/ubuntu/bidder/venv/bin/python3 /home/ubuntu/bidder/venv/bin/gunicorn --access-logfile - --wor>
             ├─24039 /home/ubuntu/bidder/venv/bin/python3 /home/ubuntu/bidder/venv/bin/gunicorn --access-logfile - --wor>
             └─24040 /home/ubuntu/bidder/venv/bin/python3 /home/ubuntu/bidder/venv/bin/gunicorn --access-logfile - --wor>

```
To test the socket activation mechanism, we can send a connection to the socket through curl by typing: (You should see html)
```bash
ubuntu@ip-172-31-9-189:~$ curl --unix-socket /run/gunicorn.sock localhost
```

```bash
ubuntu@ip-172-31-9-189:~$ sudo systemctl daemon-reload
ubuntu@ip-172-31-9-189:~$ sudo systemctl restart gunicorn
```

Configure Nginx to Proxy Pass to Gunicorn

Modify /etc/nginx/sites-available/bidder
```bash
server {
    listen 80;
    server_name bridgewell.chuangtc.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/bidder;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
Save and close the file when you are finished. Now, we can enable the file by linking it to the sites-enabled directory:
```bash
ubuntu@ip-172-31-9-189:~$ sudo ln -s /etc/nginx/sites-available/bidder /etc/nginx/sites-enabled
ubuntu@ip-172-31-9-189:~$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
ubuntu@ip-172-31-9-189:~$ sudo systemctl restart nginx

```
