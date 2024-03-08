
from auth import login, logout
import math
import time
import sys
import json


def getHostList(session,host_list):
    getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "filter": { "host": host_list }})
    if getHosts == []:
        getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "output": ["host"], "filter": { "ip": host_list }})
    return getHosts

def createHostGroup(session,groupName):
    createApi = session.hostgroup.create({"name":groupName})
    createdGroupid  = createApi['groupids'][0]
    if createdGroupid != None:
        print(f"{groupName} 그룹이 생성되었습니다.")
    return createdGroupid

def messUpdateHostId(session,groupName,hostids,zabbix_name):
    getGroup = session.hostgroup.get({ "output": ["groupids"],  "filter": { "name": groupName }})
    if getGroup == []:
        print("그룹을 찾을 수 없습니다.")
        answer = input(f"{groupName} 그룹을 생성할까요?")
        if answer == 'Y' or answer == 'y':
            getGroupid = createHostGroup(session,groupName)
        else:
            print("그룹 적용을 중지 합니다.")
            exit()
    else:
        getGroupid = getGroup[0].get('groupid')
    updateHosts = session.hostgroup.massadd({"groups": [ { "groupid": getGroupid }], "hosts": hostids})
    if updateHosts != {}:
        print(f"{zabbix_name}의 {groupName} 업데이트가 완료 되었습니다.")
    else:
        print(f"{zabbix_name}의 {groupName} 업데이트가 실패 되었습니다.")

def main():
    argv = sys.argv
    if len(sys.argv) != 4:
        print("Usage: python3 set_group_by_name.py <zabbix_name> <group_name> <host_list_file>")
        sys.exit(1)

    zabbix_name = argv[1]
    group_name = argv[2]
    host_list_file = sys.argv[3]

    host_list = []
    file_path = host_list_file
    with open(file_path, 'r') as file:
        for line in file:
            host = line.strip('\n')
            host_list.append(host)


    session = login(zabbix_name)
    hostList = getHostList(session,host_list)

    hostIds = []
    for line in hostList:
        form = {}
        form['hostid'] = line.get("hostid")
        hostIds.append(form)

    messUpdateHostId(session,group_name,hostIds,zabbix_name)
    # print(f"총 {len(result)}개")

    # 로그아웃
    logout(session)

if __name__ == "__main__":
    main()
