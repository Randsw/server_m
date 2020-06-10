import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

cmd = host.run('jython --version')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'Jython 2') > -1


def test_mc_is_installed(host):
    cmd = host.run('mc --version')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'GNU Midnight Commander') > -1

def test_git_is_installed(host):
    cmd = host.run('git --version')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'git version') > -1

def test_htop_is_installed(host):
    cmd = host.run('git --version')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'htop') > -1

def test_ncdu_is_installed(host):
    cmd = host.run('ncdu --version')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'ncdu') > -1

def test_nload_is_installed(host):
    cmd = host.run('nload --help')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'nload version') > -1