from zabbix_api import ZabbixAPI
from auth import login, logout
import sys

argv = sys.argv
if len(argv) < 2:
    print("Usage: python3 get_all_host.py <zabbix_name>")
    sys.exit(1)
else:
    zabbix_name = argv[1]

def print_and_write(file, text):
    # print(text)
    print(text, file=file)

def getHostList(session):
    #템플릿이 적용된 대상만 확인
    getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "selectParentTemplates": [ "templateid" ], "output": ["host", "proxy_hostid", "status"] })
    if getHosts == []:
        getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "selectParentTemplates": [ "templateid" ], "output": ["host", "proxy_hostid",  "status"]})

    return getHosts

def getProxy(session):
    getProxys = session.proxy.get({"output": ["proxyid", "host"]})
    return getProxys

session = login(zabbix_name)
proxys = getProxy(session)
proxy_name = {}

for line in proxys:
    proxy_id = line.get('proxyid')
    proxy_host = line.get('host')
    proxy_name[proxy_id] = proxy_host

host_list = getHostList(session)

if len(host_list) > 0:
    host_not_CRM_count = 0
    for line in host_list:
        host_name = line.get('host')
        if '_CRM' not in host_name:
            host_not_CRM_count = host_not_CRM_count + 1
            interfaces = line.get('interfaces')
            template = line.get('parentTemplates')
            status = line.get('status')
            proxy_hostid = line.get('proxy_hostid')
            if int(proxy_hostid) > 0:
                proxy_host_name = proxy_name[proxy_hostid]
            else:
                proxy_host_name = "No Proxy"

            flag_status = 'O' 
            if status == '1':
                flag_status = 'X'

            flag_template = 'O'
            if len(template) == 0:
                flag_template = 'X'

            for index in interfaces:
                print(f"{index.get('ip')}|{zabbix_name}|{flag_template}|{flag_status}|{proxy_host_name}")


print(f"총 검색 결과 수용 대수 {len(host_list)}")
print(f"데이터 보존 호스트(_CRM이 호스트명에 포함 된 대상) 제외  {host_not_CRM_count}")

logout(session)
