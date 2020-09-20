import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_ssh_is_running(host):
    assert host.service('sshd').is_running

def test_ssh_pub_key(host):
    ssh_conf = host.file('/etc/ssh/sshd_config')
    pub_key = host.file('/home/dep7admin/.ssh/authorized_keys')
    assert ssh_conf.exists
    assert pub_key.exists
    assert ssh_conf.contains('PermitRootLogin no')
    assert pub_key.contains('cluster01@cluster01-PC')

def test_net_services_work(host):
    assert host.socket("tcp://172.17.0.2:22").is_listening