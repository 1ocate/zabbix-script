from auth import login, logout
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

def getHostList(session,host_list):
    getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "filter": { "host": host_list }})
    return getHosts

def changeHostName(session,host_id,change_name,ori_name):
    result = session.host.update({"hostid": host_id, "host": change_name })
    print(f"{ori_name[change_name]} to change {change_name} done.")
    return result

host_list = []
new_name = {}
ori_name = {}

session = login(zabbix_name)

# 파일리스트 가져오기
file_path = host_name_list
with open(file_path, 'r') as file:
    lines = file.read().splitlines()
    for line in lines:
        column = line.split(',')
        host = column[0]
        change_name = column[1]
        host_list.append(host)
        new_name[host] = change_name
        ori_name[change_name] = host

# 주어진 host_list에서 zabbix host list 가져오기
zabbix_host_list = getHostList(session,host_list)
hostids = []
hostid_new_name = {}

for host in zabbix_host_list:
        hostids.append(host.get('hostid'))
        hostid_new_name[host.get('hostid')] = new_name[host.get('host')]

# host 이름 변경
for hostid in hostids:
    changeHostName(session,hostid,hostid_new_name[hostid],ori_name)

logout(session)
