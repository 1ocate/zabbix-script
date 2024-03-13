from zabbix_api import ZabbixAPI
from auth import login, logout
import sys

argv = sys.argv
if len(argv) != 3:
    print("Usage: python3 get_host.py <zabbix_name> <host_list_file>")
    sys.exit(1)
else:
    zabbix_name = argv[1]
    host_name_list = argv[2]

def print_and_write(file, text):
    # print(text)
    print(text, file=file)

def get_host_data(session,host_list):
    #템플릿이 적용된 대상만 확인
    getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "selectParentTemplates": [ "templateid" ], "output": ["host"], "filter": { "host": host_list }})
    if getHosts == []:
        getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "selectParentTemplates": [ "templateid" ], "output": ["host"], "filter": { "ip": host_list }})
    template_has_hosts = []
    no_template_has_host = []
    result = {}

    for host in getHosts:
        if len(host.get('parentTemplates')) > 0:
            template_has_hosts.append(host)
        else:
            no_template_has_host.append(host)

    result['template_has_hosts'] = template_has_hosts
    result['no_template_has_host'] = no_template_has_host
    return result

search_list = []
file_path = host_name_list
with open(file_path, 'r') as file:

    for line in file:
        host = line.strip('\n')
        search_list.append(host)

session = login(zabbix_name)
host_list = get_host_data(session,search_list)
template_has_hosts = host_list['template_has_hosts']

ready_add_hosts = []
for host in host_list['no_template_has_host']:
    if host not in template_has_hosts:
        ready_add_hosts.append(host)

if len(template_has_hosts) > 0:
    print("기 수용 대상")
    for line in template_has_hosts:
        host_name = line.get('host')
        interfaces = line.get('interfaces')
        if '_CRM' not in host_name:
            for index in interfaces:
                print(f"{host_name}|{index.get('ip')}")

if len(ready_add_hosts) > 0:
    print("수용 예정 대상")
    for line in ready_add_hosts:
        print(f"{line.get('host')}|{line.get('interfaces')[0].get('ip')}")

print(f"총 검색 대상 대수 {len(search_list)}")
print(f"총 검색 결과 기 수용 대수 (템플릿 적용) {len(template_has_hosts)}")
print(f"총 검색 결과 수용 예정 (템플릿 미적용) {len(ready_add_hosts)}")

logout(session)
