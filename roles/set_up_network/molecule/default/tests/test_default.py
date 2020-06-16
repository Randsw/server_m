import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_network_config_exists(host):
    network_conf = host.file('etc/netplan/config.yaml')
    assert network_conf.exists


def test_network_config_is_valid(host):
    network_conf = host.file('etc/netplan/config.yaml')
    assert network_conf.contains('172.17.0.100/16')

def test_network_config_working(host):
    cmd = host.run('ip a')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'172.17.0.100') > -1
    