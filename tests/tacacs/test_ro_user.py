import pytest

pytestmark = [
    pytest.mark.disable_loganalyzer,
    pytest.mark.topology('any'),
    pytest.mark.device_type('vs')
]

def test_ro_user(localhost, duthosts, rand_one_dut_hostname, creds, test_tacacs):
    duthost = duthosts[rand_one_dut_hostname]

    dutip = duthost.host.options['inventory_manager'].get_host(duthost.hostname).vars['ansible_host']
    res = localhost.shell("sshpass -p {} ssh "\
                          "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "\
                          "{}@{} cat /etc/passwd".format(
            creds['tacacs_ro_user_passwd'], creds['tacacs_ro_user'], dutip))

    for l in res['stdout_lines']:
        fds = l.split(':')
        if fds[0] == "test":
            assert fds[4] == "remote_user"

def test_ro_user_docker_ps(localhost, duthosts, rand_one_dut_hostname, creds, test_tacacs):
    duthost = duthosts[rand_one_dut_hostname]

    # Run as readonly use the command `sudo docker ps`
    dutip = duthost.host.options['inventory_manager'].get_host(duthost.hostname).vars['ansible_host']
    res = localhost.shell("sshpass -p {} ssh "\
                          "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "\
                          "{}@{} sudo docker ps".format(
            creds['tacacs_ro_user_passwd'], creds['tacacs_ro_user'], dutip))

    # Verify that the command is allowed
    stdout = res['stdout_lines']
    assert len(stdout) >= 1
    assert stdout[0].startwith('CONTAINER ID')

def test_ro_user_docker_ps_all(localhost, duthosts, rand_one_dut_hostname, creds, test_tacacs):
    duthost = duthosts[rand_one_dut_hostname]

    # Run as readonly use the command `sudo docker ps -a`
    dutip = duthost.host.options['inventory_manager'].get_host(duthost.hostname).vars['ansible_host']
    res = localhost.shell("sshpass -p {} ssh "\
                          "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "\
                          "{}@{} sudo docker ps -a".format(
            creds['tacacs_ro_user_passwd'], creds['tacacs_ro_user'], dutip))

    # Verify that the command is allowed
    stdout = res['stdout_lines']
    assert len(stdout) >= 1
    assert stdout[0].startwith('CONTAINER ID')

def test_ro_user_ipv6(localhost, duthosts, rand_one_dut_hostname, creds, test_tacacs_v6):
    duthost = duthosts[rand_one_dut_hostname]

    dutip = duthost.host.options['inventory_manager'].get_host(duthost.hostname).vars['ansible_host']
    res = localhost.shell("sshpass -p {} ssh "\
                          "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "\
                          "{}@{} cat /etc/passwd".format(
            creds['tacacs_ro_user_passwd'], creds['tacacs_ro_user'], dutip))

    for l in res['stdout_lines']:
        fds = l.split(':')
        if fds[0] == "test":
            assert fds[4] == "remote_user"
