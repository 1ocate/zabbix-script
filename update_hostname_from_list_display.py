from auth import login, logout
from set_group_by_name import messUpdateHostId
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

def getHostList(session,host_list,flag=None):
    if flag == "display":
        getHosts = session.host.get({"selectInterfaces": ["ip", "details"], "output": ["host", "name"], "filter": { "name": host_list }})
    else: 
        getHosts = session.host.get({"selectInterfaces": ["ip", "details"], "output": ["host"], "filter": { "host": host_list }})
    return getHosts

def changeHostName(session,host_id,ori_name,change_name,display_name):
    #print(f"{ori_name[change_name]}, {change_name}, {display_name}") 
    change_host_name = session.host.update({"hostid": host_id, "host": change_name })
    print(f"{ori_name[change_name]} to change {change_name} done.")
    if change_name != display_name:
        print("표시명 변경을 진행합니다.")
        change_display_name = session.host.update({"hostid": host_id, "name": display_name })
        print(f"{change_name} to display_name change {display_name} done.")


host_list = []
new_host_list = []
display_host_list = []
new_name = {}
ori_name = {}
host_display_name = {}

session = login(zabbix_name)

# 파일리스트 가져오기
file_path = host_name_list
with open(file_path, 'r') as file:
    lines = file.read().splitlines()
    for line in lines:
        column = line.split(',')
        host = column[0]
        change_name = column[1]
        display_name = column[2]
        if host == None or change_name == None or display_name == None:
            print("변경될 항목중 빠진 항목이 있습니다.")
            print(f"{line}")
            sys.exit(1)
        host_list.append(host)
        new_host_list.append(change_name)
        display_host_list.append(display_name)
        new_name[host] = change_name
        host_display_name[host] = display_name
        ori_name[change_name] = host

# 주어진 host_list에서 zabbix host list 가져오기
zabbix_host_list = getHostList(session,host_list)
exsist_host_list = getHostList(session,new_host_list)
display_host_list = getHostList(session,display_host_list,"display")

# print(display_host_list)
# exit()
exsist_hostids = []
if len(exsist_host_list) > 0 :
    for line in exsist_host_list:
        form = {}
        form['hostid'] = line.get("hostid")
        exsist_hostids.append(form)

# if len(display_host_list) > 0 :
#     for line in display_host_list:
#         form = {}
#         form['hostid'] = line.get("hostid")
#         exsist_hostids.append(form)

if len(exsist_hostids) > 0 :
    messUpdateHostId(session,"duplicate_hosts",exsist_hostids,zabbix_name)
    print("변경 될 호스트 이름의 호스트가 존재 합니다. 삭제하고 진행하세요.")
    sys.exit()
else:
    print("호스트 이름 변경을 진행합니다.")

hostids = []
hostid_new_name = {}
hostid_display_name = {}

for host in zabbix_host_list:
        hostids.append(host.get('hostid'))
        hostid_new_name[host.get('hostid')] = new_name[host.get('host')]
        hostid_display_name[host.get('hostid')] = host_display_name[host.get('host')]

# host 이름 변경
for hostid in hostids:
    changeHostName(session,hostid,ori_name,hostid_new_name[hostid],hostid_display_name[hostid])

logout(session)
