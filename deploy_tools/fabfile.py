from fabric.contrib.files import append, exists, sed
from fabric.apt import env, local, run

REPO_URL = 'https://github.com/StanHotchner/superlists.git'

def _create_directory_structure_if_nessary(site_folder): # 创建目录结构
    for subfolder in ('daabase', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))
        
def _get_lastest_source(source_folder):
    if exists(source_folder + '.git'): # 检查source_folder 是不是一个 git 仓库
        run('cd %s && git fetch' % (source_folder,)) # 如果是的话就从github 上拉取最新的提交
    
    
def deploy()
    site_folder = '/home/%s/sites/%s/' % (env.user, env.hosts)
    source_foler = site_folder + '/source'
    _create_directory_structure_if_nessary(site_folder)
    _get_lastest_source(source_foler)
    _update_settings(source_foler, env.host)
    _update_virtualenv(source_foler)
    _update_static_files(source_folder)
    _update_database(source_folder)