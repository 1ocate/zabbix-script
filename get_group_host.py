from zabbix_api import ZabbixAPI
from auth import login, logout
import sys

argv = sys.argv
if len(argv) < 2:
    print("Usage: python3 get_group_host.py <zabbix_name> <group_name>")
    sys.exit(1)
else:
    zabbix_name = argv[1]
    group_name = argv[2]

session = login(zabbix_name)

def print_and_write(file, text):
    # print(text)
    print(text, file=file)

def getHostList(session,groupName):
    getGroup = session.hostgroup.get({ "output": ["groupids"],  "filter": { "name": groupName }})
    if getGroup == []:
        print("그룹을 찾을 수 없습니다.")
        exit()
    getGroupid = getGroup[0].get('groupid')
    getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "groupids":getGroupid })
    return getHosts

result = getHostList(zabbix_name,group_name)

for line in result:
    #print(f"{line.get('host')}")
    print(f"{line.get('host')}|{line.get('interfaces')[0].get('ip')}")

logout(session)
