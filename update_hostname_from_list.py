
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

def changeHostName(zabbixName,host_id,host_change_name):
    zabbix = api_login(zabbixName)
    result = zabbix.host.update({"hostid": host_id, "host": host_change_name })
    return result

host_list = []

# 파일리스트 가져오기
file_path = host_name_list
with open(file_path, 'r') as file:
    for line in file:
        column = line.split(',')
        host = column[0]
        new_name = column[1]
        host_list.append(host)

hostList = getHostList(zabbix_name,host_list)
print(hostList)
# getHostIDs = [hostid.get('hostid') for hostid in hostList]

# print(f"Total rquest search {len(host_list)}")
# print(f"Total result {len(getHostList)}")
