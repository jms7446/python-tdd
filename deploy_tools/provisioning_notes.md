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
    sudo apt install nginx git python36 python3.6-venv
    
## Nginx Virtual Host config

* see nginx.template.conf
* replace DOMAIN with, 

e.g., superlists.my-domain.com:

    cat ./deploy_tools/nginx.template.con \
        | sed "s/DOMAIN/superlists.my-domain.com/g" \
        | sudo tee /etc/nginx/sites-available/superlists.my-domain.com
        
    sudo systemctl reload nginx

## Systemd service

* see gunicorn-systemd.template.service
* replace DOMAIN with, 

e.g., superlists.my-domain.com

    cat ./deploy_tools/gunicorn-systemd.template.service \
        | sed "s/DOMAIN/superlists.my-domain.com/g" \
        | sudo tee /etc/systemd/system/gunicorn-superlists.my-domain.com.service
        
    sudo systemctl daemon-reload
    sudo systemctl enable gunicorn-superlists.my-domain.com
    sudo systemctl start gunicorn-superlists.my-domain.com

