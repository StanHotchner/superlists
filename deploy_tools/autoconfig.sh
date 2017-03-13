#!/bin/bash
sed "s/SITENAME/superlists.sunplus-prof.com/g" nginx.template.conf | \
sudo tee /etc/nginx/sites-available/superlists.sunplus-prof.com

sudo rm -f /etc/nginx/sites-enabled/superlists.sunplus-prof.com

sudo ln -s /etc/nginx/sites-available/superlists.sunplus-prof.com \
/etc/nginx/sites-enabled/superlists.sunplus-prof.com

sed "s/SITENAME/superlists.sunplus-prof.com/g" gunicorn-upstart.template.conf  | \
sudo tee /etc/init/gunicorn-superlists.sunplus-prof.com.conf
 

