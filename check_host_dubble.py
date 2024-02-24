from zabbix_api import ZabbixAPI
from auth import login, logout
import sys
# 반복 출력할 내용
# from collections import Counter

# my_list = [1, 2, 3, 4, 2, 3, 5, 6, 6]  # 대상 리스트 (실제 데이터로 대체해야 함)
# counter = Counter(my_list)

# duplicates = [item for item, count in counter.items() if count > 1]
# print(duplicates)

argv = sys.argv
if len(argv) < 2:
    print("Please input zabbix name.")
    sys.exit(1)
# elif len(argv) < 3:
#     print("Please input host name.")
#     sys.exit(1)
else:
    zabbix_name = argv[1]
    # host_name_list = argv[2]

def print_and_write(file, text):
    # print(text)
    print(text, file=file)

def getHostList(session):
    getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "filter": { "available": "0" }})
    return getHosts

def getHostListWithTemplate(session,host_list):
    getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "selectParentTemplates": [ "templateid" ], "output": ["host", "status"], "filter": { "ip": host_list }})
    return getHosts

session = login(zabbix_name)
host_list = getHostList(session)
host_list_not_crm = []
for line in host_list:
    host = line.get('host')

    if '_CRM' not in host and 'jpt' not in host:
       host_list_not_crm.append(line.get('interfaces')[0].get('ip'))
    #host_list_not_crm.append(f"{line.get('host')}|{line.get('interfaces')[0].get('ip')}|{line.get('status')}")

host_list_with_template = getHostListWithTemplate(session,host_list_not_crm)
result_host_list = []
for line in host_list_with_template:
    if len(line.get('parentTemplates')) > 0:
        print(f"{line.get('host')}|{line.get('interfaces')[0].get('ip')}|{line.get('status')}")
        result_host_list.append(f"{line}")

print(f"총 검색 결과 갯수 {len(result_host_list)}")


logout(session)
