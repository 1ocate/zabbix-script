
from zabbix_api import ZabbixAPI
from auth import login, logout
import math
import time
import sys
import json

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
    getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "filter": { "host": host_list }})
    if getHosts == []:
        getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "filter": { "ip": host_list }})
    return getHosts

search_list = []
file_path = host_name_list
with open(file_path, 'r') as file:

    for line in file:
        host = line.strip('\n')
        search_list.append(host)

session = login(zabbix_name)
host_list = getHostList(session,search_list)

for line in host_list:
    print(f"{line.get('host')}|{line.get('interfaces')[0].get('ip')}")
    # print(f"{line.get('interfaces')[0].get('ip')}")

print(f"총 검색 대상 갯수 {len(search_list)}")
print(f"총 검색 결과 갯수 {len(host_list)}")
