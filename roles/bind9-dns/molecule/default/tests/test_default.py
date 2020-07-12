import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_git_is_installed(host):
    cmd = host.run('docker exec bind service named status')
    assert cmd.rc == 0
    assert cmd.stdout.find(u'running') > -1

#def test_git_is_installed(host):
#    cmd = host.run('docker exec bind service named status')
#    assert cmd.rc == 0
#    assert cmd.stdout.find(u'running') > -1