Provisioning a new site
========================

## Required packages:

* nginx
* Python 3.7
* virtualenv + pip
* git

eg, on Ubuntu:
    
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install nginx git python37 python3.6-venv
    
## Nginx Virtual Host config

* see nginx.template.conf
* replace DOMAIN with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace DOMAIN with, e.g., staging.my-domain.com
