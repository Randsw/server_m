import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_firewall_is_installed(host):
    cmd = host.run('iptables -L')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'dpt:20') > -1
    assert cmd.stdout.find(u'dpt:21') > -1
    assert cmd.stdout.find(u'spts:1024:65535') > -1

def test_iptables_is_running(host):
    assert host.service('firewall').is_running
