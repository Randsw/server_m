import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_webmail_container_is_running(host):
    webmail = host.docker("roundcube")
    assert webmail.is_running

def test_smtp_container_is_running(host):
    smtp = host.docker("mail_smtp")
    assert smtp.is_running

def test_imap_container_is_running(host):
    imap = host.docker("mail_imap")
    assert imap.is_running

def test_antispam_container_is_running(host):
    antispam = host.docker("mail_antispam")
    assert antispam.is_running

def test_admin_container_is_running(host):
    admin = host.docker("mail_admin")
    assert admin.is_running

def test_webdav_container_is_running(host):
    webdav = host.docker("mail_webdav")
    assert webdav.is_running

def test_database_container_is_running(host):
    database = host.docker("mail_postgresql")
    assert database.is_running

def test_fetchmail_container_is_running(host):
    fetchmail = host.docker("fetchmail")
    assert fetchmail.is_running

def test_antivirus_container_is_running(host):
    antivirus = host.docker("mail_antivirus")
    assert antivirus.is_running

def test_redis_container_is_running(host):
    redis = host.docker("mail_redis")
    assert redis.is_running

def test_front_container_is_running(host):
    front = host.docker("front")
    assert front.is_running

def test_bind_container_is_running(host):
    bind = host.docker("bind")
    assert bind.is_running

def test_elasticsearch_container_is_running(host):
    elasticsearch = host.docker("elasticsearch")
    assert elasticsearch.is_running

def test_kibana_container_is_running(host):
    kibana = host.docker("kibana")
    assert kibana.is_running

def test_fluentd_container_is_running(host):
    fluentd = host.docker("fluentd")
    assert fluentd.is_running

def test_curator_container_is_running(host):
    curator = host.docker("curator")
    assert curator.is_running

def test_rocketchat_container_is_running(host):
    rocketchat = host.docker("rocketchat")
    assert rocketchat.is_running

def test_mongo_container_is_running(host):
    mongo = host.docker("mongo")
    assert mongo.is_running

def test_prometheus_container_is_running(host):
    prometheus = host.docker("prometheus")
    assert prometheus.is_running

def test_alertmanager_container_is_running(host):
    alertmanager = host.docker("alertmanager")
    assert alertmanager.is_running

def test_nodeexporter_container_is_running(host):
    nodeexporter = host.docker("nodeexporter")
    assert nodeexporter.is_running

def test_cadvisor_container_is_running(host):
    cadvisor = host.docker("cadvisor")
    assert cadvisor.is_running

def test_grafana_container_is_running(host):
    grafana = host.docker("grafana")
    assert grafana.is_running

def test_pushgateway_container_is_running(host):
    pushgateway = host.docker("pushgateway")
    assert pushgateway.is_running

def test_gitlab_container_is_running(host):
    gitlab = host.docker("gitlab")
    assert gitlab.is_running

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
    assert oct(mail_dir.mode) == '0o755'
    mail_data_dir = host.file('/home/root/docker_compose/mail/data')
    assert mail_data_dir.exists
    assert oct(mail_data_dir.mode) == '0o750'
    es_data_dir = host.file('/home/root/docker_compose/logging/elasticsearch/data')
    assert es_data_dir.exists
    assert oct(es_data_dir.mode) == '0o777'