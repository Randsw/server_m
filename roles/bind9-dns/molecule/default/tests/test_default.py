import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_named_conf(host):
    named_conf = host.file('/home/root/docker_compose/bind/etc/named.conf')
    assert named_conf.exists
    assert named_conf.contains('192.168.1.0/24;')
    assert named_conf.contains("zone \"dep7server.com\" IN")
    assert named_conf.contains("zone \"1.168.192.in-addr.arpa\" IN")

def test_zone_conf(host):
    zone_conf = host.file('/home/root/docker_compose/bind/etc/dep7server.com')
    assert zone_conf.exists
    assert zone_conf.contains('mail')
    assert zone_conf.contains("jenkins")
    assert zone_conf.contains("repo")

def test_reverse_zone_conf(host):
    reverse_zone_conf = host.file('/home/root/docker_compose/bind/etc/1.168.192.in-addr.arpa')
    assert reverse_zone_conf.exists
    assert reverse_zone_conf.contains('mail.dep7server.com.')
    assert reverse_zone_conf.contains("jenkins.dep7server.com.")
    assert reverse_zone_conf.contains("repo.dep7server.com.")

def test_named_default_conf(host):
    named_default_conf = host.file('/home/root/docker_compose/bind/etc/named.conf.default-zones')
    assert named_default_conf.exists
    assert named_default_conf.contains('127.in-addr.arpa')
    assert named_default_conf.contains("0.in-addr.arpa")
    assert named_default_conf.contains("255.in-addr.arpa")

def test_auth_file(host):
    auth_file = host.file('/home/root/docker_compose/bind/etc/auth_transfer.conf')
    assert auth_file.exists
    assert auth_file.contains('algorithm hmac-sha256;')
