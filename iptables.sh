#!/bin/bash
sudo /sbin/iptables -F
sudo /sbin/iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo /sbin/iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# utiliza DNS
sudo /sbin/iptables -A OUTPUT -p udp --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
sudo /sbin/iptables -A INPUT  -p udp --sport 53 -m state --state ESTABLISHED     -j ACCEPT
sudo /sbin/iptables -A OUTPUT -p tcp --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
sudo /sbin/iptables -A INPUT  -p tcp --sport 53 -m state --state ESTABLISHED     -j ACCEPT


# responda aos pings que vêm da nemo.alunos.di.fc.ul.pt
sudo /sbin/iptables -A INPUT -s nemo.alunos.di.fc.ul.pt -p icmp -j -m state --state NEW,ESTABLISHED ACCEPT


# aceita ligações de qualquer um
sudo /sbin/iptables -A INPUT -p tcp --dport 5000 -m state --state NEW,ESTABLISHED -j ACCEPT


# aceita ligações SSH da sua rede local
sudo /sbin/iptables -A INPUT -s 10.101.148.182/23 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
sudo /sbin/iptables -A INPUT -s 10.101.0.0/24 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
sudo /sbin/iptables -A INPUT -s 127.0.0.0/8 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
sudo /sbin/iptables -A INPUT -p tcp --dport 22 -m state --state ESTABLISHED -j ACCEPT
sudo /sbin/iptables -A OUTPUT -p tcp --sport 22 -m state --state NEW,ESTABLISHED -j ACCEPT


# máquinas obrigatórias
sudo /sbin/iptables -A INPUT -d "10.101.85.6, 10.101.85.138, 10.101.85.18,10.121.53.14, 10.121.53.15, 10.101.53.16, 10.121.72.23, 10.101.148.1, 10.101.85.134" -j ACCEPT
sudo /sbin/iptables -A OUTPUT -s "10.101.85.6, 10.101.85.138, 10.101.85.18,10.121.53.14, 10.121.53.15, 10.101.53.16, 10.121.72.23, 10.101.148.1, 10.101.85.134" -j ACCEPT


# ssl
sudo /sbin/iptables -A INPUT  -p tcp -m multiport --dports 21,80,443 -m state --state NEW,ESTABLISHED -j ACCEPT
sudo /sbin/iptables -A OUTPUT  -p tcp -m multiport --dports 21,80,443 -m state --state NEW,ESTABLISHED -j ACCEPT

sudo /sbin/iptables -A INPUT -i lo -j ACCEPT
sudo /sbin/iptables -A OUTPUT -o lo -j ACCEPT
sudo /sbin/iptables -A INPUT -j DROP
sudo /sbin/iptables -A OUTPUT -j DROP
