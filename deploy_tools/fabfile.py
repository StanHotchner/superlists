# -*- coding: utf-8 -*-
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/StanHotchner/superlists.git'

def _create_directory_structure_if_nessary(site_folder): # 创建目录结构
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))
        
def _get_lastest_source(source_folder):
    if exists(source_folder + '/.git'): # 检查source_folder 是不是一个 git 仓库
        run('cd %s && git fetch' % (source_folder,)) # 如果是的话就从github 上拉取最新的提交
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
        
    current_commit = local("git log -n 1 --format=%H", capture=True) # 取得本地（开发环境中）的提交哈希
    run('cd %s && git reset --hard %s' % (source_folder, current_commit)) # 把被部署服务器仓库版本切换到与本地一致
    
def _update_settings(source_folder, site_name):
    setting_path = source_folder + '/superlists/settings.py'
    sed(setting_path, 'DEBUG = True', 'DEBUG = False')
    sed(setting_path, 'ALLOWED_HOSTS =.+$', 'ALLOWED_HOSTS = ["%s"]' % (site_name,))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'MyNameIsStan.ILovaKrystal.IhaveBeenInShenzhenForNineYears.!@#$%^&*()'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY='%s'" % (key,))
    append(setting_path, '\nfrom .secret_key import SECRET_KEY')
    
def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))  
    
def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (source_folder,))
    
def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (source_folder, ))

def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    #print(site_folder)
    
    source_folder = site_folder + '/source'
    _create_directory_structure_if_nessary(site_folder)
    _get_lastest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    