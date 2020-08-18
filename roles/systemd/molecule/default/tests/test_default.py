import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_rocket_is_running(host):
    assert host.service('RocketChat').is_running

def test_rocketchat_container_is_running(host):
    rocketchat = host.docker("root_rocketchat_1")
    assert rocketchat.is_running

def test_mongodb_container_is_running(host):
    mongodb = host.docker("root_mongo_1")
    assert mongodb.is_running

def test_listening_http(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening

def test_listening_https(host):
    assert host.socket("tcp://0.0.0.0:443").is_listening

def test_listening_imap(host):
    assert host.socket("tcp://0.0.0.0:143").is_listening

def test_listening_pop3(host):
    assert host.socket("tcp://0.0.0.0:110").is_listening

def test_listening_pop3s(host):
    assert host.socket("tcp://0.0.0.0:993").is_listening

def test_listening_imaps(host):
    assert host.socket("tcp://0.0.0.0:995").is_listening

def test_listening_startls(host):
    assert host.socket("tcp://0.0.0.0:487").is_listening

def test_listening_smtps(host):
    assert host.socket("tcp://0.0.0.0:587").is_listening