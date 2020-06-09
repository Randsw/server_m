import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_mc_is_installed(host):
    assert host.service('vsftpd').is_running

def test_git_is_installed(host):
    assert host.service('vsftpd').is_running

def test_htop_is_installed(host):
    assert host.service('vsftpd').is_running

def test_ncdu_is_installed(host):
    assert host.service('vsftpd').is_running

def test_nload_is_installed(host):
    assert host.service('vsftpd').is_running