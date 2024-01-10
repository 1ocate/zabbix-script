
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
    getHosts = zabbix.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "filter": { "ip": host_list }})
    return getHosts


host_list = []
file_path = host_name_list
with open(file_path, 'r') as file:

    for line in file:
        host = line.strip('\n')
        host_list.append(host)

getHostList = getHostList(zabbix_name,host_list)

for line in getHostList:
    # print(f"{line.get('host')}|{line.get('interfaces')[0].get('ip')}")
    print(f"{line.get('interfaces')[0].get('ip')}")

print(f"Total rquest search {len(host_list)}")
print(f"Total result {len(getHostList)}")
