import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_webmail_container_is_running(host):
    webmail = host.docker("mail_server_webmail_1")
    assert webmail.is_running

def test_smtp_container_is_running(host):
    smtp = host.docker("mail_server_smtp_1")
    assert smtp.is_running

def test_imap_container_is_running(host):
    imap = host.docker("mail_server_imap_1")
    assert imap.is_running

def test_antispam_container_is_running(host):
    antispam = host.docker("mail_server_antispam_1")
    assert antispam.is_running

def test_admin_container_is_running(host):
    admin = host.docker("mail_server_admin_1")
    assert admin.is_running

def test_webdav_container_is_running(host):
    webdav = host.docker("mail_server_webdav_1")
    assert webdav.is_running

def test_database_container_is_running(host):
    database = host.docker("mail_server_database_1")
    assert database.is_running

def test_fetchmail_container_is_running(host):
    fetchmail = host.docker("mail_server_fetchmail_1")
    assert fetchmail.is_running

def test_antivirus_container_is_running(host):
    antivirus = host.docker("mail_server_antivirus_1")
    assert antivirus.is_running

def test_redis_container_is_running(host):
    redis = host.docker("mail_server_redis_1")
    assert redis.is_running


def test_listening_service(host):
    assert host.socket("tcp://0.0.0.0:3000").is_listening