from zabbix_api import ZabbixAPI
from auth import login, logout
import sys

argv = sys.argv
if len(argv) < 2:
    print("Please input zabbix name.")
    sys.exit(1)
elif len(argv) < 3:
    print("Please input host name.")
    sys.exit(1)
else:
    zabbix_name = argv[1]
    host_name_list = argv[2]

def print_and_write(file, text):
    # print(text)
    print(text, file=file)

def getHostList(session,host_list):
    #템플릿이 적용된 대상만 확인
    getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "selectParentTemplates": [ "templateid" ], "output": ["host"], "filter": { "host": host_list }})
    if getHosts == []:
        getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "selectParentTemplates": [ "templateid" ], "output": ["host"], "filter": { "ip": host_list }})
    template_has_hosts = []
    ready_add_hosts = []
    result = {}

    for host in getHosts:
        if len(host.get('parentTemplates')) > 0:
            template_has_hosts.append(host)
        else: 
            ready_add_hosts.append(host)
    result['template_has_hosts'] = template_has_hosts
    result['ready_add_hosts'] = ready_add_hosts

    return result

search_list = []
file_path = host_name_list
with open(file_path, 'r') as file:

    for line in file:
        host = line.strip('\n')
        search_list.append(host)

session = login(zabbix_name)
host_list = getHostList(session,search_list)
template_has_hosts = host_list['template_has_hosts']

ready_add_hosts = []

for host in host_list['template_has_hosts']:
    if host not in template_has_hosts:
        ready_add_hosts.append(host)

if len(template_has_hosts) > 0:
    print("기 수용 대상")
    for line in template_has_hosts:
        if '_CRM' not in line:
            print(f"{line.get('host')}|{line.get('interfaces')[0].get('ip')}")
            # print(f"{line.get('interfaces')[0].get('ip')}")

if len(ready_add_hosts) > 0:
    print("수용 예정 대상")
    for line in ready_add_hosts:
        print(f"{line.get('host')}|{line.get('interfaces')[0].get('ip')}")

print(f"총 검색 대상 대수 {len(search_list)}")
print(f"총 검색 결과 수용 대수 {len(template_has_hosts)}")
print(f"총 검색 결과 수용 예정 {len(ready_add_hosts)}")

logout(session)
