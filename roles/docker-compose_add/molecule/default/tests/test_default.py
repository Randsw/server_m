import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_webmail_container_is_running(host):
    webmail = host.docker("docker_compose_webmail_1")
    assert webmail.is_running

def test_smtp_container_is_running(host):
    smtp = host.docker("docker_compose_smtp_1")
    assert smtp.is_running

def test_imap_container_is_running(host):
    imap = host.docker("docker_compose_imap_1")
    assert imap.is_running

def test_antispam_container_is_running(host):
    antispam = host.docker("docker_compose_antispam_1")
    assert antispam.is_running

def test_admin_container_is_running(host):
    admin = host.docker("docker_compose_admin_1")
    assert admin.is_running

def test_webdav_container_is_running(host):
    webdav = host.docker("docker_compose_webdav_1")
    assert webdav.is_running

def test_database_container_is_running(host):
    database = host.docker("docker_compose_database_1")
    assert database.is_running

def test_fetchmail_container_is_running(host):
    fetchmail = host.docker("docker_compose_fetchmail_1")
    assert fetchmail.is_running

def test_antivirus_container_is_running(host):
    antivirus = host.docker("docker_compose_antivirus_1")
    assert antivirus.is_running

def test_redis_container_is_running(host):
    redis = host.docker("docker_compose_redis_1")
    assert redis.is_running

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
    assert host.socket("tcp://0.0.0.0:465").is_listening

def test_listening_smtps(host):
    assert host.socket("tcp://0.0.0.0:587").is_listening

def test_compose_config_dir_exist(host):
    grafana_dir = host.file('/home/root/docker_compose/monitoring/grafana')
    assert grafana_dir.exists
    assert oct(grafana_dir.mode) == '0o777'
    grafana_data_dir = host.file('/home/root/docker_compose/monitoring/grafana/grafana_data')
    assert grafana_data_dir.exists
    assert oct(grafana_data_dir.mode) == '0o777'
    prometheus_dir = host.file('/home/root/docker_compose/monitoring/prometheus')
    assert prometheus_dir.exists
    assert oct(prometheus_dir.mode) == '0o777'
    prometheus_data_dir = host.file('/home/root/docker_compose/monitoring/prometheus/prometheus_data')
    assert prometheus_data_dir.exists
    assert oct(prometheus_data_dir.mode) == '0o777'
    mail_dir = host.file('/home/root/docker_compose/mail')
    assert mail_dir.exists
    assert oct(mail_dir.mode) == '0o777'
    mail_data_dir = host.file('/home/root/docker_compose/mail/data')
    assert mail_data_dir.exists
    assert oct(mail_data_dir.mode) == '0o750'
    es_data_dir = host.file('/home/root/docker_compose/logging/elasticsearch/data')
    assert es_data_dir.exists
    assert oct(es_data_dir.mode) == '0o777'