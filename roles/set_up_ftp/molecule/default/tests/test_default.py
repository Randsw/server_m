import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_vsftpd_config_exists(host):
    ftp_conf = host.file('/etc/vsftpd.conf')
    assert ftp_conf.exists


def test_vsftpd_is_running(host):
    assert host.service('vsftpd').is_running

def test_ftp_users(host):
    ftp_user = host.file('/etc/group')
    users = ['Rand', 'chistov', 'Bychkov', 'Chernov', 
             'Chernyshova', 'Dmitriev', 'Kuritsyn', 
             'Lantsov', 'Makhaev_A', 'Shevtsev',
             'Dolotkazina', 'Ann', 'Antonovich', 
             'Pavel', 'solovyev', 'Emelyanov',
             'DSBobrus', 'Alimov', 'dep4', 'klimov',
             'Petr', 'Shutov', 'KavUpdate']
    assert ftp_user.contains('ftp_users')
    for user in users:
        assert ftp_user.contains(user)
