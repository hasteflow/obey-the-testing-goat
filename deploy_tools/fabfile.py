
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/hasteflow/obey-the-testing-goat.git'


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')

    else:
        run(f'git clone {REPO_URL} {source_folder}')

    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'

    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_folder}')

    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_settings(source_folder, site_name, chapter=''):
    settings_path = source_folder + '/' + chapter + '/superlists/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'ALLOWED_HOSTS = .+$', f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file = source_folder + '/' + chapter + '/superlists/superlists/secret_key.py'

    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')

    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../../../virtualenv/bin/python manage.py collectstatic --noinput'
    )


def _update_database(source_folder):
    run(f'cd {source_folder}'
        ' && ../../../virtualenv/bin/python manage.py migrate --noinput'
    )


def vagrant():
    env.user = 'ubuntu'
    env.hosts = ['127.0.0.1:2222']
    env.key_filename = '/home/razvan.blaga@3pillar.corp/Documents/zenspace/obeythetestinggoat/vagrant_host/.vagrant/machines/server/virtualbox/private_key'


def deploy():
    chapter = 'chapter_9'
    site_folder = f'/home/ubuntu/sites/tddgoat.me'
    source_folder = site_folder + '/source'

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, 'tddgoat.me', chapter)

    _update_virtualenv(source_folder)
    _update_static_files(source_folder + '/' + chapter + '/superlists')
    _update_database(source_folder + '/' + chapter + '/superlists')

