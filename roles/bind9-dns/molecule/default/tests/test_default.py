import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_bins_is_working(host):
    cmd = host.run('docker exec bind service named status')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'running') > -1

def test_server_is_resolved(host):
    cmd = host.run('docker exec bind nslookup dep7server.com 172.18.0.2')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'192.168.1.142') > -1

def test_mailserver_is_resolved(host):
    cmd = host.run('docker exec bind nslookup mail.dep7server.com 172.18.0.2')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'192.168.1.142') > -1

def test_reposerver_is_resolved(host):
    cmd = host.run('docker exec bind nslookup repo.dep7server.com 172.18.0.2')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'192.168.1.144') > -1

def test_jenkinsserver_is_resolved(host):
    cmd = host.run('docker exec bind nslookup jenkins.dep7server.com 172.18.0.2')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'192.168.1.143') > -1