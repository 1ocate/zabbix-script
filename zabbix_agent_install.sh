#!/bin/bash

# 경로 변수 설정
AGENT_CONF="/etc/zabbix/zabbix_agent2.conf"
AGENT_D_DIR="/etc/zabbix/zabbix_agent2.d"
SECRET_PSK_FILE="$AGENT_D_DIR/secret.psk"

# Zabbix repository 추가 및 Zabbix Agent 2 설치
rpm -Uvh https://repo.zabbix.com/zabbix/6.4/rhel/7/x86_64/zabbix-release-6.4-1.el7.noarch.rpm
yum install -y zabbix-agent2 zabbix-agent2-plugin-*


# PSK 파일 생성
# openssl rand -hex 32 > "$SECRET_PSK_FILE"
echo "b88b7f7c1df48ecf51d66b8dd19fa5429f3781a6518c680810232e57d29d2212" > "$SECRET_PSK_FILE"
chmod 640 "$SECRET_PSK_FILE"
chown zabbix.zabbix "$SECRET_PSK_FILE"


# 설정 파일 수정
sed -i 's/Server=127.0.0.1/Server=0.0.0.0\/0/g' "$AGENT_CONF"
sed -i 's/ServerActive=127.0.0.1/ServerActive=0.0.0.0\/0/g' "$AGENT_CONF"
sed -i 's/Hostname=Zabbix server/# Hostname=Zabbix server/g' "$AGENT_CONF"
sed -i 's/# HostnameItem=system.hostname/HostnameItem=system.hostname/g' "$AGENT_CONF"

# 보안 설정 추가
cat <<EOL >> "$AGENT_CONF"

# Connection encryption
TLSConnect=psk
TLSAccept=psk
TLSPSKFile=/etc/zabbix/zabbix_agent2.d/secret.psk
TLSPSKIdentity=bluekey
EOL

# Zabbix Agent 2 시작 및 자동 시작 설정
systemctl enable zabbix-agent2
systemctl start zabbix-agent2

tail -f /var/log/zabbix/zabbix_agent2.log

