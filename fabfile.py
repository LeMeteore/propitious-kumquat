#!/usr/bin/env python
# -*- coding:utf-8 -*-

import posixpath
import os
from fabric.api import run, local, env, settings, cd, task, sudo
from fabric.contrib.files import exists
from fabric.operations import _prefix_commands, _prefix_env_vars
#from fabric.decorators import runs_once
#from fabric.context_managers import cd, lcd, settings, hide

# one way of using specific key, user, host, port
# fab command -i /path/to/key.pem [-H [user@]host[:port]]

env.hosts = ['phobos']
env.use_ssh_config = True
env.ssh_config_path = '/home/nsukami/.ssh/config'
# env.user = 'patrick'
# env.key_filename = ['/home/nsukami/.ssh/id_rsa_phobos']
env.virtualenv = '/webapps/wappa'
env.project_dir = '/webapps/wappa/'
env.code_dir = '/webapps/wappa/source/'
env.static_root = '/webapps/wappa/source/wappa/media/'
env.code_repo = 'git@bitbucket.org:wappa-team/wappa1.git'
env.django_settings_module = 'settings.prod'
env.owner = 'awa'

PYTHON_BIN = "python3.5"
PYTHON_PREFIX = ""  # e.g. /usr/local  Use "" for automatic
PYTHON_FULL_PATH = "%s/bin/%s" % (PYTHON_PREFIX, PYTHON_BIN) if PYTHON_PREFIX else PYTHON_BIN

def virtualenv(venv_dir):
    """
    Context manager that establishes a virtualenv to use.
    """
    return settings(venv=venv_dir)


def run_venv(command, **kwargs):
    """
    Runs a command in a virtualenv (which has been specified using
    the virtualenv context manager
    """
    run("source %s/bin/activate" % env.virtualenv + " && " + command, **kwargs)


def install_dependencies():
    ensure_virtualenv()
    # activate virtualenv
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            sudo("pip install -r requirements/prod.txt", user='awa')


def ensure_virtualenv():
    # virtualenv exists do nothing
    if exists(env.virtualenv):
        return
    # otherwise create virtualenv
    with cd(env.code_dir):
        sudo("pyvenv-3.5 %s" % env.virtualenv, user='awa')

@task
def ensure_src_dir():
    if not exists(env.code_dir):
        sudo("mkdir -p %s" % env.code_dir, user='awa')
    with cd(env.code_dir):
        if not exists(posixpath.join(env.code_dir, '.git')):
            sudo('git clone %s .' % (env.code_repo), user='awa')
            # branches should be params
            # sudo('git checkout -b %s %s' %('beta-back-office', 'origin/beta-back-office'), user='awa')
            sudo('git checkout -b %s %s' %('dashboard', 'origin/dashboard'), user='awa')

@task
def push_sources():
    """
    Push source code to server
    """
    ensure_src_dir()
    #local('git push origin_wappa beta-back-office')
    local('git push origin_wappa dashboard')
    with cd(env.code_dir):
        sudo('git pull origin dashboard', user='awa')


@task
def run_tests():
    """ Runs the Django test suite as is.  """
    local("coverage run manage.py test -v 2 --settings=wappa.settings.dev")


@task
def version():
    """ Show last commit to the deployed repo. """
    with cd(env.code_dir):
        run('git log -1')


@task
def uname():
    """ Prints information about the host. """
    run("uname -a")


@task
def nginx_stop():
    """
    Stop the webserver that is running the Django instance
    """
    run("service nginx stop")


@task
def nginx_start():
    """
    Starts the webserver that is running the Django instance
    """
    run("service nginx start")


@task
def nginx_restart():
    """
    Restarts the webserver that is running the Django instance
    """
    if DJANGO_SERVER_RESTART:
        with cd(env.code_dir):
            run("touch %s/wsgi.py" % env.project_dir)
    else:
        with settings(warn_only=True):
            webserver_stop()
        webserver_start()


def restart():
    """ Restart the wsgi process """
    with cd(env.code_dir):
        run("touch %s/ccos/wsgi.py" % env.code_dir)


def build_static():
    assert env.static_root.strip() != '' and env.static_root.strip() != '/'
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            run_venv("./manage.py collectstatic -v 0 --clear --noinput")
    run("chmod -R ugo+r %s" % env.static_root)


@task
def first_deployment_mode():
    """
    Use before first deployment to switch on fake south migrations.
    """
    env.initial_deploy = True


@task
def update_database(app=None):
    """
    Update the database (run the migrations)
    Usage: fab update_database:app_name
    """
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            if getattr(env, 'initial_deploy', False):
                run_venv("./manage.py syncdb --all")
                run_venv("./manage.py migrate --fake --noinput")
            else:
                run_venv("./manage.py syncdb --noinput")
                if app:
                    run_venv("./manage.py migrate %s --noinput" % app)
                else:
                    run_venv("./manage.py migrate --noinput")


@task
def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """
    # Handle context manager modifications
    wrapped_cmd = _prefix_commands(_prefix_env_vars(cmd), 'remote')
    try:
        host, port = env.host_string.split(':')
        return local(
            "ssh -p %s -A %s@%s '%s'" % (port, env.user, host, wrapped_cmd)
        )
    except ValueError:
        return local(
            "ssh -A %s@%s '%s'" % (env.user, env.host_string, wrapped_cmd)
        )


@task
def deploy():
    """
    Deploy the project.
    """
    with settings(warn_only=True):
        webserver_stop()
    push_sources()
    install_dependencies()
    update_database()
    build_static()
    webserver_start()


# @task
# def testing():
#     sudo('su - awa', user='root')
