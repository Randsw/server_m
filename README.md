# Automatic server initialization

Install fully operational department server with firewall, dns server, mail server, ftp server, chat, gitlab, EFK stack for logging, Prometheus/Grafana for monitoring with Ansible and Docker-Compose.

**:warning: This version work only with Ubuntu Server/Dekstop**

## Contents

1. [Requirements](#requirements)
   * [Host](#host-setup)
   * [Ansible](#ansible)
   * [Docker](#docker)
     * [Docker-compose](#docker-compose)
2. [Usage](#usage)
   * [Network setup](#network-setup)
   * [Services-deploy](#services-deploy)
3. [Variables](#configuration)
   * [Host](#host-variables)
   * [Network](#network-vars)
   * [SSH](#ssh-vars)
   * [Iptables](#iptables-var)
   * [Docker](#docker-vars)
   * [DHCP](#dhcp-vars)
   * [Ftp](#ftp-vars)
   * [DNS](#dns-vars)
   * [Services deploy](#services-deploy-vars)
4. [Services configuration definition](#services-configuration-definition)
   * [FTP](#ftp-conf)
   * [DHCP](#dhcp-conf)
   * [DNS](#dns-conf)
   * [Services](#service-conf)
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
5. [Links to services manual](#links-manual)

## Requirements

### Host

* [Docker Engine](https://docs.docker.com/install/) version **17.05** or newer
* [Docker Compose](https://docs.docker.com/compose/install/) version **1.20.0** or newer
* 8 GB of RAM

*:information_source: Make sure your user has the [required permissions][linux-postinstall] to interact with the Docker daemon.*

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


[linux-postinstall]: https://docs.docker.com/install/linux/linux-postinstall/