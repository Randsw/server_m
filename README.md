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
|ansible_host| -             | Host IP address or domain name|
|ansible_user| -             | OS User     |
|ansible_ssh_private_key_file| -           | Path to SSH private key
|ansible_python_interpreter| /usr/bin/python3 | Path to Python3

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
|sshd_use_pam| no  |  PAM authentication
|sshd_password_authentication| no | Password_authentication
|sshd_challenge_response_authentication| no | [RedHat Explanation][RedHat-ssh]
|sshd_permitroot_login| no | SSH root login

### Iptables Variables
Находятся в файле `inventories/prod_server/host_vars/dep7server.yml` в разделе **#Firewall config**
| Name       | Default Value | Description |
|------------|---------------|-------------|

[linux-postinstall]: https://docs.docker.com/install/linux/linux-postinstall/
[ansible-vault]:  https://docs.ansible.com/ansible/latest/user_guide/vault.html
[netplan-config]: https://netplan.io/examples/
[RedHat-ssh]: https://access.redhat.com/solutions/336773