from zabbix_api import ZabbixAPI
from auth import login, logout
from collections import Counter
import sys,time


def print_and_write(file, text):
    # print(text)
    print(text, file=file)

def get_duplicate_hostids(session):
    all_host_ips = []
    all_host_datas = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip"], "output": ["host","hostid"]})
    if len(all_host_datas) > 0:
        for line in all_host_datas:
            host_name = line.get('host')
            if '_CRM' not in host_name and 'Zabbix' not in host_name:
                interfaces = line.get('interfaces')
                # print(interfaces)
                for index in interfaces:
                    all_host_ips.append(index.get('ip'))

    counter = Counter(all_host_ips)

    duplicate_host_ips = [item for item, count in counter.items() if count > 1]
    duplicate_host_datas = getHostListWithTemplate(session,duplicate_host_ips)
    duplcate_hostids = [data.get('hostid') for data in duplicate_host_datas]
    # print(duplcate_hostids)
    return duplcate_hostids

def getHostListWithTemplate(session,host_list):
    template_has_hosts = []
    getHosts = session.host.get({"selectHosts": ["host"], "selectInterfaces": ["ip", "details"], "selectParentTemplates": [ "templateid" ], "output": ["host", "status"], "filter": { "ip": host_list  }})
    for host in getHosts:
        if len(host.get('parentTemplates')) > 0:
            template_has_hosts.append(host)
    return template_has_hosts

def getItemData(session, hostids):
    if len(hostids) < 1:
        getItemData = []
    else:
        getItemData = session.item.get({"selectHosts":["host"], "output": ["itemid","host"], "filter": { "name":"Host name of Zabbix agent running", "hostid":hostids}})
    return getItemData

def getHistoryData(session,itemids):
    getHistoryData = session.history.get({"output": ["itemid","value"], "history": 1, "itemids": itemids, "sortfield": ["clock","itemid"], "sortorder": "DESC", "limit": len(itemids)})
    return getHistoryData

def search(zabbix_name, chunk_size = 30):

    session = login(zabbix_name)
    duplcate_hostids = get_duplicate_hostids(session)
    itemDatas = getItemData(session, duplcate_hostids)
    host_and_itemid = {}
    itemids = []

    search_results = []
    if len(itemDatas) > 0:
        for data in itemDatas:
            host = data.get('hosts')[0].get('host')
            itemid = data.get('itemid')
            host_and_itemid[itemid] = host
            itemids.append(itemid)

        itemidsGroups = [itemids[i:i+chunk_size] for i in range(0, len(itemids), chunk_size)]

        for itemidsGroup in itemidsGroups:
            historyDatas = getHistoryData(session,itemidsGroup)
            for data in historyDatas:
                itemid = data.get('itemid')
                agent_host_name = data.get('value')

                if host_and_itemid[itemid] != agent_host_name:
                    result = {}
                    result['host_name'] = host_and_itemid[itemid]
                    result['agent_host_name'] = agent_host_name
                    if result not in search_results:
                        search_results.append(result)

            time.sleep(3)
    logout(session)
    return search_results


if __name__ == "__main__":

    argv = sys.argv
    if len(argv) != 2:
        print("Usage: python3 check_host_dubble.py <zabbix_name> ")
        sys.exit(1)
    else:
        zabbix_name = argv[1]

    result = search(zabbix_name, 20)
    print("host_name|agent_host_name")
    for line in result:
        print(f"{line['host_name']}|{line['agent_host_name']}")

