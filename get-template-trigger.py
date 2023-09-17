from zabbix_api import ZabbixAPI
f=open("./account.txt","r")
lines=f.readlines()
api = ZabbixAPI(server=lines[0].strip())
id=lines[1].strip()
pw=lines[2].strip()
print(pw)
f.close()

def login(api, id, pw):
    api.login(id,pw)
    return api

local = login(api,id,pw)

trigger_params = {
    "selectHosts": ["hostid", "host"],
    "output": ["triggerid", "description", "status"],
}

trigger_data = local.trigger.get(trigger_params)
trigger_list = []

for trigger in trigger_data:
    trigger_row = [
        trigger['hosts'][0]['hostid'],
        trigger['hosts'][0]['host'],
        trigger['triggerid'],
        trigger['description'],
        trigger['status']
    ]
    trigger_list.append(trigger_row)

filtered_trigger_list = [
    [trigger[1], trigger[3], trigger[4]]
    for trigger in trigger_list
]

trigger_names = [
    trigger[1]
    for trigger in trigger_list
]

hostid_host = {
    trigger[1]: trigger[0]
    for trigger in trigger_list
}

for trigger_name in trigger_names:
    for trigger in trigger_list:
        if trigger[1] == trigger_name:
            print([trigger[2], trigger[3], trigger[4]])
