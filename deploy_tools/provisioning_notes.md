��������վ
===========

## ��Ҫ��װ�İ���

nginx
Python3
git
pip
virtualenv

Ubuntu �еİ�װ���
sudo apt-get install nginx git python3 python3-pip
sudo pip3 install virtualenv

## ����nginx ��������:

* �ο� nginx.template.conf
* �� SITENAME ������������������磺superlists-staging.sunplus-prof.com

## upstart ����

* �ο� gunicorn-upstart.template.conf
* �� SITENAME ������������������磺superlists-staging.sunplus-prof.com

## �ļ��нṹ��

�������û��˻���Home Ŀ¼Ϊ /home/username

/home/username
������ sites
    ������ SITENAME
        ������ database
        ������ source
        ������ static
        ������ virtualenv



