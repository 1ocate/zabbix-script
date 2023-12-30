
from zabbix_api import ZabbixAPI
import sys
import json

f = open("config.json", encoding="UTF-8")
CONFIG = json.loads(f.read())
f.close()


argv = sys.argv
if len(sys.argv) != 4:
    print("Usage: python3 set_group_by_name.py <zabbix_name> <group_name> <host_list_file>")
    sys.exit(1)

zabbix_name = sys.argv[1]
group_name = sys.argv[2]
host_list_file = sys.argv[3]
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
    if getHosts == []:
        getHosts = zabbix.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "filter": { "ip": host_list }})
    return getHosts

def messUpdateHostId(zabbixName,groupName,hostids):
    global id, pw, f, host_list
    zabbix = api_login(zabbixName)
    getGroup = zabbix.hostgroup.get({ "output": ["groupids"],  "filter": { "name": groupName }})
    if getGroup == []:
        print("그룹을 찾을 수 없습니다.")
        exit()
    getGroupid = getGroup[0].get('groupid')
    updateHosts = zabbix.hostgroup.massadd({"groups": [ { "groupid": getGroupid }], "hosts": hostids})
    if updateHosts != {}:
        print(f"{zabbixName}의 {groupName} 업데이트가 완료 되었습니다.")
    else:
        print(f"{zabbixName}의 {groupName} 업데이트가 실패 되었습니다.")

host_list = []
file_path = host_list_file
with open(file_path, 'r') as file:
    for line in file:
        host = line.strip('\n')
        host_list.append(host)


getHostList = getHostList(zabbix_name,host_list)

getHostIds = []
for line in getHostList:
    form = {}
    form['hostid'] = line.get("hostid")
    getHostIds.append(form)

messUpdateHostId(zabbix_name,group_name,getHostIds)
# print(f"총 {len(result)}개")
