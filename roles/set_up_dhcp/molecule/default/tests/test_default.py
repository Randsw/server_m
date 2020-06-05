import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_dhcp_is_running(host):
    assert host.service('isc-dhcp-server').is_running

def test_ssh_pub_key(host):
    dhcp_conf = host.file('/etc/dhcp/dhcpd.conf')
    assert dhcp_conf.exists
    assert dhcp_conf.contains('option domain-name-servers 172.17.0.2')
