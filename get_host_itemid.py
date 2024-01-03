
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
    print("Please input host name.")
    sys.exit(1)
else:
    zabbix_name = argv[1]
    host_name_list = argv[2]

def print_and_write(file, text):
    # print(text)
    print(text, file=file)

def api_login(zabbixName):
    zabbix = ZabbixAPI(server=CONFIG['ZabbixServerInfo'][zabbixName]['URL'])
    zabbix.login(CONFIG['ZabbixServerInfo'][zabbixName]['user'],CONFIG['ZabbixServerInfo'][zabbixName]['password'])
    return zabbix

def getHostList(zabbixName,host_list):
    zabbix = api_login(zabbixName)
    getHosts = zabbix.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "filter": { "host": host_list }})
    return getHosts

def getItemList(zabbixName,hostIds):
    zabbix = api_login(zabbixName)
    getItems = zabbix.item.get({"output": "extend", "selectHosts": ["name", "hostid","proxy_hostid"], "hostids": hostIds, "filter": { 'type': '7', 'status': '0' }, "sortfield": "name"})
    # getItems = zabbix.item.get({"output": "extend", "selectHosts": "extend", "hostids": hostIds, "filter": { 'type': '7', 'status': '1' }, "sortfield": "name"})
    return getItems



host_list = []
file_path = host_name_list
with open(file_path, 'r') as file:

    for line in file:
        host = line.strip('\n')
        host_list.append(host)

getHostList = getHostList(zabbix_name,host_list)

hostIp = {}
for line in getHostList:
    hostIp[line.get('hostid')] = line.get('interfaces')[0].get('ip')


# 리스트를 10개씩 묶기
chunk_size = 10
result = [getHostList[i:i + chunk_size] for i in range(0, len(getHostList), chunk_size)]

for host_group in result:

    getHostIds = [hostid.get('hostid') for hostid in host_group]
    ItemList = getItemList(zabbix_name,getHostIds)
    for line in ItemList:
        print(f"{line.get('hosts')[0].get('name')}|{line.get('hostid')}|{hostIp[line.get('hostid')]}|{line.get('itemid')}|{line.get('name')}|{line.get('status')}|{line.get('value_type')}|{line.get('hosts')[0].get('proxy_hostid')}")
    # print(getHostIds)

    time.sleep(5)

# print(f"Total rquest search {len(host_list)}")
# print(f"Total result {len(getHostList)}")
