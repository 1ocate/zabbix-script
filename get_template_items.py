from auth import login, logout
import math
import time
import sys
import re

argv = sys.argv
if len(argv) < 2:
    print("Please input zabbix name.")
    sys.exit(1)
elif len(argv) < 3:
    print("Please input host name.")
    sys.exit(1)
else:
    zabbix_name = argv[1]
    template_list_file = argv[2]

def print_and_write(file, text):
    print(text)
    print(text, file=file)


def getTemplateList(sesison,templateName,outputFile):
    templateDatas = sesison.template.get({ "output": ["name", "templateid"],  "filter": { "name": templateName }})
    result = {}
    for data in templateDatas:
        result[data.get('templateid')] = data.get('name')

    return result


def getApplicationList(sesison, applicationids):
    application_datas = sesison.application.get({ "output": ["applicationid", "name"], "filter": { "applicationid": applicationids }})
    result = {}
    for data in application_datas:
        result[data.get('applicationid')] = data.get('name')

    return result

def getItemList(session,template_id_to_name,discovery):
    templateids = list(template_id_to_name.keys())
    # discovery값이 'y'면 prototype
    if discovery == 'y':
        item_datas = session.itemprototype.get({ "selectTriggers": ["triggerid"], "expandExpression": "y", "selectApplications": ["name"], "output": ["hostid", "name", "key_", "delay", "history", "status"], "templateids":templateids })
    else:
        item_datas = session.item.get({ "selectTriggers": ["triggerid"], "expandExpression": "y", "selectApplications": ["name"], "output": ["hostid", "name", "key_", "delay", "history", "status"], "templateids":templateids })
    newItem_list= []
    if len(item_datas) != 0:
        for item in item_datas:
            status = ''
            if item.get('status') == '0':
                status = '활성'
            elif item.get('status') == '1':
                status = '비활성'
            newItem = []
            newItem.append(template_id_to_name[item.get('hostid')]) # 
            if (len(item.get('applications')) < 1 ):
                newItem.append('None')
            else:
                newItem.append(item.get('applications')[0].get('name'))

            newItem.append(item.get('name'))

            # discovery값이 'y'면 prototype
            if discovery == 'y':
                newItem.append("O")
            else:
                newItem.append("X")

            newItem.append(item.get('key_'))
            newItem.append(item.get('delay'))
            newItem.append(item.get('history'))
            if (len(item.get('triggers')) < 1 ):
                newItem.append(status)
                newItem.append('X')
                newItem.append('')
                newItem.append('')
                newItem.append('')
                newItem.append('')
                newItem.append('')
            else:
                newItem.append(status)
                newItem.append('O')
                newItem.append(item.get('triggers'))
            newItem_list.append(newItem)
    else:
        print("아이템을 찾을 수 없습니다.")
        exit()

    return newItem_list

def getTriggerList(session,template_id_to_name,discovery):
    priority = [
        "Not classified",
        "Information",
        "Warning",
        "Average",
        "High",
        "Disaster"
    ]
    templateids = list(template_id_to_name.keys())
    params = { "selectTriggers": ["triggerid"],  "expandExpression": "y", "expandDescription": "y", "output": ["expression","description","status","recovery_expression","priority", "opdata"], "templateids":templateids }

    # discovery값이 'y'면 prototype
    if discovery == 'y':
        trigger_datas = session.triggerprototype.get(params)
    else:
        trigger_datas = session.trigger.get(params)
    result = {}

    # 정규식 패턴
    # pattern = r"\[(.*?)\]"

    for data in trigger_datas:
        expression = data.get('expression').replace('\n', '').replace('\r', '')
        status = ''
        if data.get('status') == '0':
            status = '활성'
        elif data.get('status') == '1':
            status = '비활성'
        result[data.get('triggerid')] = f"{data.get('description')}@{expression}@{data.get('recovery_expression')}@{priority[int(data.get('priority'))]}@{data.get('opdata')}@{status}"
        # matches = re.findall(pattern, data.get('description'))
        # print(matches)
    return result

def process_item_list(item_list, trigger_id_to_data):
    for item in item_list:
        item[9] = f"\n{item[0]}@@@@@@@@@".join([trigger_id_to_data[sub_dict['triggerid']] for sub_dict in item[9]])
        item[9] = item[9] if item[9] else ""
        print('@'.join(map(str, item)))

# 파일리스트 가져오기
file_path = template_list_file
with open(file_path, 'r') as file:
    lines = file.read().splitlines()
    template_list = [line for line in lines]

session = login(zabbix_name)
# application_id_to_name = getApplicationList(session,)
template_id_to_name = getTemplateList(session,template_list,'')
trigger_id_to_data = getTriggerList(session,template_id_to_name,'')
triggerprototype_id_to_data = getTriggerList(session,template_id_to_name,'y')
item_list = getItemList(session,template_id_to_name,'')
itemprototype_list = getItemList(session,template_id_to_name,'y')

# 결과 출력 
process_item_list(item_list, trigger_id_to_data)
process_item_list(itemprototype_list, triggerprototype_id_to_data)

