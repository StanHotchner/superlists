配置新网站
===========

## 需要安装的包：

nginx
Python3
git
pip
virtualenv

Ubuntu 中的安装命令：
* sudo apt-get install nginx git python3 python3-pip
* sudo pip3 install virtualenv

## 配置nginx 虚拟主机:

* 参考 nginx.template.conf
* 把 SITENAME 换成所需的域名，例如：superlists-staging.sunplus-prof.com

## upstart 任务

* 参考 gunicorn-upstart.template.conf
* 把 SITENAME 换成所需的域名，例如：superlists-staging.sunplus-prof.com

## 文件夹结构：

假设有用户账户，Home 目录为 /home/username

/home/username
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv



