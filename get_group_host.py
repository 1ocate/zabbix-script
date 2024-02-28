
from zabbix_api import ZabbixAPI
import math
import time
import sys
import json

f = open("config.json", encoding="UTF-8")
CONFIG = json.loads(f.read())
f.close()

argv = sys.argv
if len(argv) < 2:
    print("Please input zabbix name.")
    sys.exit(1)
elif len(argv) < 3:
    print("Please group name.")
    sys.exit(1)
else:
    zabbix_name = argv[1]
    group_name = argv[2]

def print_and_write(file, text):
    # print(text)
    print(text, file=file)

def api_login(zabbixName):
    zabbix = ZabbixAPI(server=CONFIG['ZabbixServerInfo'][zabbixName]['URL'])
    zabbix.login(CONFIG['ZabbixServerInfo'][zabbixName]['user'],CONFIG['ZabbixServerInfo'][zabbixName]['password'])
    return zabbix

def getHostList(zabbixName,groupName):
    zabbix = api_login(zabbixName)
    getGroup = zabbix.hostgroup.get({ "output": ["groupids"],  "filter": { "name": groupName }})
    if getGroup == []:
        print("그룹을 찾을 수 없습니다.")
        exit()
    getGroupid = getGroup[0].get('groupid')
    getHosts = zabbix.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "groupids":getGroupid })
    return getHosts

result = getHostList(zabbix_name,group_name)

for line in result:
    #print(f"{line.get('host')}")
    print(f"{line.get('host')}|{line.get('interfaces')[0].get('ip')}")
