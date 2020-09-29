# Automatic server initialization

Install fully operational department server with firewall, dns server, mail server, ftp server, chat, gitlab, EFK stack for logging, Prometheus/Grafana for monitoring with Ansible and Docker-Compose.

:warning: **This version work only with Ubuntu Server/Dekstop**

## Contents

1. [Requirements](#requirements)
   * [Host](#host-setup)
   * [Ansible](#ansible)
   * [Docker](#docker)
2. [General principles](#general-principles)
   * [Configure](#configure-principles)
   * [Deploy](#deploy-principles)
3. [Usage](#usage)
   * [Network setup](#network-setup)
   * [Services-deploy](#services-deploy)
4. [Variables](#configuration)
   * [Host Variables](#host-variables)
   * [Network Variables](#network-vars)
   * [SSH Variables](#ssh-vars)
   * [Iptables Variables](#iptables-var)
   * [Docker Variables](#docker-vars)
   * [DHCP Variables](#dhcp-vars)
   * [Ftp Variables](#ftp-vars)
   * [DNS Variables](#dns-vars)
   * [Services deploy Variables](#services-deploy-vars)
5. [Services configuration definition](#services-configuration-definition)
   * [FTP Config](#ftp-conf)
   * [DHCP Config](#dhcp-conf)
   * [DNS Config](#dns-conf)
   * [Services Config](#service-conf)
      * [EFK - Logging](#efk-conf)
        * [Elasticsearch](#elasticsearch-conf)
        * [Fluentd](#fluentd-conf)
        * [Kibana](#kibana-conf)
        * [Curator](#curator-conf)
      * [Rocketchat](#rocketchat-conf)
      * [Monitoring](#monitoring-conf)
        * [Prometheus](#prometheus-conf)
        * [Grafana](#grafana-conf)
        * [Alertmanager](#alertmanager-conf)
        * [Node exporter](#node-exporter-conf)
        * [Cadvisor](#cadvisor-conf)
      * [Mail](#mail-conf)
        * [Nginx - Reverse Proxy](#nginx-reverse-proxy)
        * [Admin panel](#admin-panel-conf)
      * [Gitlab](#gitlab-conf)
6. [Links to services manual](#links-manual)

## Requirements

### Host

* 4 Processor core
* 8 GB of RAM

:exclamation: *Make sure your user has the [required permissions][linux-postinstall] to interact with the Docker daemon.*

The services exposes the following ports by default:

* 53(udp/tcp): DNS port
* 80:          Standart HTTP port
* 443:         Standart HTTPs port
* 25:          SMTP port
* 110:         POP3 port
* 143:         IMAP port
* 465:         SMTPS port
* 587:         STARTTLS port
* 993:         IMAPS port
* 995:         POP3 port

### Ansible

* [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) verison **2.8** or newer

### Docker

* [Docker Engine](https://docs.docker.com/install/) version **17.05** or newer
* [Docker Compose](https://docs.docker.com/compose/install/) version **1.20.0** or newer

## General Principles

### Configure

Для автоматизации настройки и развертывания программного обеспечения необходимого для работы сервера используется **Ansible**. Все задачи в **Ansible** делятся на роли(roles) по своей функциональности. Роли затем объединяются в плэйбуки(playbook). Для развертывания сервера применяются две роли:

* `dep7server_prepare` - отвечает за настройку параметров сетевого подключения
* `dep7server_playbook` - отвечает за настройки и развертывание сервисов

Для настройки необходимых служб и демонов необходимы права пользователя root, соответственно все плейбуки выполняются от имени пользователя root хоста. Что бы не вводить пароль суперпользователя при каждом запуске роли и для безопасного хранения пароля используется механизм [Ansible Vault][ansible-vault]. Зашифрованный пароль суперпользвателя хоста хранится в файле `dep7server_vault.yml`

В файле `inverntories/prod_server/hosts.yml` находятся общие переменные хоста которые нужно задать:
| Name       | Default Value | Description |
|------------|---------------|-------------|
|`ansible_host`| -             | Host IP address or domain name|
|`ansible_user`| -             | OS User     |
|`ansible_ssh_private_key_file`| -           | Path to SSH private key
|`ansible_python_interpreter`| /usr/bin/python3 | Path to Python3

В своей работе Ansible использует SSH соединение. По умолчанию настройки SSH сервера хоста позволяеют установить соединение с правами суперпользователя при введении пароля. Такая практика считается небезопасной. Необходимо настроить SSH сервер хоста на отклонение соединения по паролю и с правами суперпользователя и осуществления соединения только по ключу. Для этого в плейбуке `dep7server_playbook` происходит настройка SSH сервера. Публичный ключ находится в папке `roles/copy_ssh_key/files`

Подробное описание переменных используемых при настройке и развертывании сервисов сервера приведено в соответсвующих разделах.

### Deploy

Для развертывания сервисов используется **Docker**. Все сервисы сервера разворачиваются в своих контейнерах. Кроме **Gitlab** все контейнеры разделяют философию:
> Один процесс - один контейнер.

Файл развертывания сервисов генерится с помощью **Ansible** из шаблона.

## Usage

### Network setup

По умолчанию утилитой отвечающей за сетевые подключения в ОС семейства Ubuntu является **Netplan**. Задать настройки сетевого подлкючения необходимо при установке системы. В случае необходимости смены настроек сетевого подключения при конфигурации сервера используется Ansible роль `dep7server_prepare`.  

Настройки сети задаются в файле `inventories/prod_server/host_vars/dep7server.yml` в разделе **Network configuration**

В утилите **Netplan** конфигурация задается в JSON формате. Для задания конфигурации ознакомьтесь с [инструкцией][netplan-config].

Выполните плэйбук для установки настроек сетевого подключения:

```console
ansible-playbook dep7server_prepare.yml -i inventories/prod_server/hosts.yml --ask-pass --ask-vault-pass
```

### Service deploy

Развертывание сервисов производится при выполнение плейбука `dep7server_playbook`.

```console
ansible-playbook dep7server_playbook.yml -i inventories/prod_server/hosts.yml --ask-pass --ask-vault-pass
```

На целевом хосте производися скачиваение заданных контейнеров с сервисами, настройка конфигурационных файлов и папок для данных. Также производится настройка SSH сервера для доступа только заданных непривилегированных пользователей только ключу. Поэтому ключ `--ask-pass` при последующих запусках необходимо убрать.
После успешного выполнения плэйбука можно приступать к использованию сервисов.

## Variables

### Host Variables

[См. выше](#configure-principles)

### Network Variables

[См. выше](#configure-principles)

### SSH Variables

Находятся в файле `inventories/prod_server/host_vars/dep7server.yml` в разделе **#ssh config**
| Name       | Default Value | Description |
|------------|---------------|-------------|
|`sshd_use_pam`| no  |  PAM authentication
|`sshd_password_authentication`| no | Password_authentication
|`sshd_challenge_response_authentication`| no | [RedHat Explanation][RedHat-ssh]
|`sshd_permitroot_login`| no | SSH root login

### Iptables Variables

Находятся в файле `inventories/prod_server/host_vars/dep7server.yml` в разделе **#Firewall config**
| Name       | Default Value | Description |
|------------|---------------|-------------|
|`firewall_allowed_tcp_ports`| - | List of allowed input tcp port|
|`firewall_allowed_udp_ports`| - | List of allowed input udp port|

### Docker Variables

Переменная `docker_users` содержит список имен пользователей от имени которых можно запускать Docker. Подробнее [см.](https://docs.docker.com/engine/install/ubuntu/)

### DHCP Variables

Находятся в файле `inventories/prod_server/host_vars/dep7server.yml` в разделе **#DHCP settings**

| Name       | Default Value | Description |
|------------|---------------|-------------|
|`def_lease_time`| 600         | The amount of time in minutes or        seconds a network device can use an IP Address in a network.|
|`max_lease_time`| 7200         |The maximum lease time defines the longest lease that the server can allocate.|
|`subnet`        | 192.168.1.0  | DHCP network subnet|
|`subnet_net_mask`| 255.255.255.0| DHCP network subnet mask|
|`start_address` | 192.168.1.110| DHCP start address|
|`end_address`   | 192.168.1.220| DHCP end address|
|`router_address`| 192.168.1.1  | Getaway address in DHCP network|
|`dns_address`   | 192.168.1.1  | DNS address in DHCP network|

### FTP Variables

Находятся в файле `inventories/prod_server/host_vars/dep7server.yml` в разделе **#ftp ssl cert**

| Name       | Default Value | Description |
|------------|---------------|-------------|
|`rsa_cert_file`:       | -    | path to ftp cert file|
|`rsa_private_key_file`:| -    | path to ftp private key file|

Список пользователей разделенных по правам доступа находится в зашифрованном с помощью [Ansible Vault][ansible-vault] виде в файле `role/set_up_ftp/var/main.yml` в виде:

```console
group1:
  - name: User
    password: Pass
    ....

group2:
  - name: User2
    password: Pass2
```

### DNS Variables

Находятся в файле `inventories/prod_server/host_vars/dep7server.yml` в разделе **# DNS Server settings**

| Name                       | Default Value        | Description |
|----------------------------|----------------------|-------------|
|`bind_conf_dir`             | -                    | Path to folder with bind config on *host*|
|`bind_config`               | -                    | Path to bind config file on *host*
|`bind_zone_dir_docker`      | -                    | Path to bind zone file in *docker container*|
|`bind_dir_docker`           | -                    | Path to folder with bind config in *docker container*|
|`bind_log`                  | -                    | Path to bind log file in *docker container*
|`bind_zone_file_mode`       | -                    | Zone file permission
|`bind_allow_query`          | [`any`]              | A list of hosts that are allowed to query this DNS server. Set to ['any'] to allow all hosts
|`bind_listen_ipv4`          | any                  | Listen ipv4 address
|`bind_listen_ipv6`          | any                  | Listen ipv6 address
|`bind_acls`                 | -                    | A list of hosts that are allowed to query this DNS server. Set to ['any'] to allow all hosts
|`bind_forwarders`           | 8.8.8.8              | A list of name servers to forward DNS requests to.|
|`bind_recursion`            | no                   | Allow recursion
|`bind_query_log`            | -                    | A dict with fields file (e.g. data/query.log), versions, size, when defined this will turn on the query log|
|`bind_other_logs`           | -                    | A list of logging channels to configure, with a separate dict for each domain, with relevant details|
|`bind_check_names`          | -                    | Check host names for compliance with RFC 952 and RFC 1123 and take the defined action
|`bind_zone_master_server_ip`| -                    | (Required) The IP address of the master DNS server. If host ip is different that this address DNS server configured as **slave**|
|`bind_zone_minimum_ttl`     | -                    | Minimum TTL field in the SOA record.
|`bind_zone_ttl`             | -                    | Time to Live field in the SOA record.
|`bind_zone_time_to_refresh` | -                    | Time to refresh field in the SOA record.
|`bind_zone_time_to_retry`   | -                    | Time to retry field in the SOA record.
|`bind_zone_time_to_expire`  | -                    | Time to expire field in the SOA record.
|`bind_zone_domains`         | -                    | A list of domains to configure, with a separate dict for each domain, with relevant details|
| `- allow_update`           | `['none']`           | A list of hosts that are allowed to dynamically update this DNS zone. |
| `- also_notify`            | -                    | A list of servers that will receive a notification when the master zone file is reloaded.|
| `- create_forward_zones`   | -                    | When initialized and set to `false`, creation of forward zones will be skipped (resulting in a reverse only zone)|
| `- create_reverse_zones`   | -                    | When initialized and set to `false`, creation of reverse zones will be skipped (resulting in a forward only zone)|
| `- delegate`               | `[]`                 | Zone delegation. See below this table for examples.|
| `- hostmaster_email`       | `hostmaster`         | The e-mail address of the system administrator for the zone|
| `- hosts`                  | `[]`                 | Host definitions. See below this table for examples.|
| `- ipv6_networks`          | `[]`                 | A list of the IPv6 networks that are part of the domain, in CIDR notation (e.g. 2001:db8::/48) |
| `- mail_servers`           | `[]`                 | A list of dicts (with fields `name` and `preference`) specifying the mail servers for this domain.|
| `- name_servers`           | `[ansible_hostname]` | A list of the DNS servers for this domain.|
| `- name`                   | `example.com`        | The domain name |
| `- networks`               | `['10.0.2']`         | A list of the networks that are part of the domain |
| `- other_name_servers`     | `[]`                 | A list of the DNS servers outside of this domain.|
| `- services`               | `[]`                 | A list of services to be advertised by SRV records|
| `- text`                   | `[]`                 | A list of dicts with fields `name` and `text`, specifying TXT records. `text` can be a list or string.|
| `- naptr`                  | `[]`                 | A list of dicts with fields `name`, `order`, `pref`, `flags`, `service`, `regex` and `replacement` specifying NAPTR records.|

### Service deploy Variables

Находятся в файле `inventories/prod_server/host_vars/dep7server.yml` в разделе **#Service config**

| Name                       | Default Value        | Description |
|----------------------------|----------------------|-------------|
|`docker_subnet`             | 172.19.0.0/16        | Subnet used for docker containers |
|`keep_logs_day`             | 2                    | A number of days to keep logs |
|`chat_admin_name`           | admin                | Rocketchat admin name|
|`chat_admin_pass`           | changeme             | Rocketchat admin password|
|`chat_admin_mail`           | -                    | Rocketchat admin email|
|`elastic_pass`              | changeme             | Elasticsearch password -user - 'elastic'|
|`ELK_VERISON`               | 7.8.0                | ELK/EFK stack version|
|`gitlab_external_url`       | -                    | Gitlab external URL|
|`SECRET_KEY`                |                      | Mail server Secret Key. Must be change at every setup and randomly generated|
|`domain`                    | -                    | Mail domain
|`hostnames`                 | -                    | Mail server hostname
|`sitename`                  | -                    | Sitename - Displayed at admin panel
|`website`                   | -                    | Website - Displayed at admin panel
|`mail_admin_name`           | -                    | mail admin name - first part of email **example**@example.com
|`mail_admin_mailhost`       | -                    | mail admin mail domain - second part of email example@**example.com**
|`mail_admin_pass`           | -                    | mail admin password

## Services configuration definition

### FTP Config

FTP сервер сконфигурирован для работы в пассивном режиме. Доступ по имени пользователя и паролю.

[linux-postinstall]: https://docs.docker.com/install/linux/linux-postinstall/
[ansible-vault]:  https://docs.ansible.com/ansible/latest/user_guide/vault.html
[netplan-config]: https://netplan.io/examples/
[RedHat-ssh]: https://access.redhat.com/solutions/336773
