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

def test_listening_service(host):
    assert host.socket("tcp://0.0.0.0:3000").is_listening
