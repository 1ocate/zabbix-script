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

def remove_first_bracket(sentence):
    # 대괄호 안의 문자 또는 공백을 찾는 정규식 패턴
    pattern = r'\[.*?\]'
    # 정규식 패턴과 매치되는 부분을 찾아 첫 번째 대괄호를 제거
    match = re.search(pattern, sentence)

    if match:
        # 매치된 부분을 제거하고 결과 반환
        modified_sentence = sentence[:match.start()] + sentence[match.end():]
        result = modified_sentence.strip()
        return result
    else:
        # 대괄호가 없을 경우 원래 문장 반환
        return sentence

def getTemplateList(sesison,templateName,outputFile):
    templateDatas = sesison.template.get({ "output": ["name", "templateid"],  "filter": { "name": templateName }})
    result = {}
    for data in templateDatas:
        result[data.get('templateid')] = data.get('name')

    return result

def getDiscoveryList(sesison,template_id_to_name):
    templateids = list(template_id_to_name.keys())
    discoveryDatas = sesison.discoveryrule.get({ "output": ["hostid", "name", "key_", "delay", "history", "status"],  "hostids":templateids })
    newItem_list= []
    for discovery in discoveryDatas:
        status = ''
        if discovery.get('status') == '0':
            status = '활성'
        elif discovery.get('status') == '1':
            status = '비활성'
        newItem = []
        newItem.append(template_id_to_name[discovery.get('hostid')])
        newItem.append('discovery')
        newItem.append(discovery.get('name'))
        newItem.append(discovery.get(''))
        newItem.append(discovery.get('key_'))
        newItem.append(discovery.get('delay'))
        newItem.append(discovery.get('history'))
        newItem.append(status)
        newItem.append('X')
        newItem.append('')
        newItem.append('')
        newItem.append('')
        newItem.append('')
        newItem.append('')
        newItem_list.append(newItem)
        # result[data.get('hostid')] = data.get('name')
    # result[data.get('triggerid')] = f"{code}@{description}@{expression}@{recovery_expression}@{priority[int(data.get('priority'))]}@{data.get('opdata')}@{status}"
    return newItem_list


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
        item_datas = session.itemprototype.get({ "selectTriggers": ["triggerid"], "expandExpression": "y", "selectApplications": ["name"], "output": ["templateid", "hostid", "name", "key_", "delay", "history", "status"], "templateids":templateids })
    else:
        item_datas = session.item.get({ "selectTriggers": ["triggerid"], "expandExpression": "y", "selectApplications": ["name"], "output": ["templateid", "hostid", "name", "key_", "delay", "history", "status"], "templateids":templateids })
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
            template_id = (item.get('templateid'))
            item_name = item.get('name')
            if template_id != "0":
                item_name = f"{template_id_to_name[item.get('templateid')]}: {item_name}"

            newItem.append(item_name)

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
    pattern = r"\[(.*?)\]"

    for data in trigger_datas:
        expression = data.get('expression').replace('\n', '').replace('\r', '')
        recovery_expression = data.get('recovery_expression').replace('\n', '').replace('\r', '')
        description = remove_first_bracket(data.get('description'))
        status = ''
        code = ''
        if data.get('status') == '0':
            status = '활성'
        elif data.get('status') == '1':
            status = '비활성'
        matches = re.findall(pattern, data.get('description'))
        if len(matches) > 0:
            code = matches[0]

        result[data.get('triggerid')] = f"{code}@{description}@{expression}@{recovery_expression}@{priority[int(data.get('priority'))]}@{data.get('opdata')}@{status}"
    return result

def process_item_list(item_list, trigger_id_to_data):
    for item in item_list:
        # item[9] = f"\n{item[0]}@@@@@@@@@".join([trigger_id_to_data[sub_dict['triggerid']] for sub_dict in item[9]])
        if trigger_id_to_data !="":
            item[9] = f"\n{item[0]}@{item[1]}@{item[2]}@{item[3]}@{item[4]}@{item[5]}@{item[6]}@{item[7]}@{item[8]}@".join([trigger_id_to_data[sub_dict['triggerid']] for sub_dict in item[9]])
            item[9] = item[9] if item[9] else ""

        print('@'.join(map(str, item)))

# 파일리스트 가져오기
file_path = template_list_file
with open(file_path, 'r') as file:

    lines = file.read().splitlines()
    if len(lines) > 1:
        template_list = [line for line in lines]
    else: 
        template_list = lines

session = login(zabbix_name)
# application_id_to_name = getApplicationList(session,)
template_id_to_name = getTemplateList(session,template_list,'')
trigger_id_to_data = getTriggerList(session,template_id_to_name,'')
triggerprototype_id_to_data = getTriggerList(session,template_id_to_name,'y')
item_list = getItemList(session,template_id_to_name,'')
itemprototype_list = getItemList(session,template_id_to_name,'y')
discovery_list = getDiscoveryList(session,template_id_to_name)
# 결과 출력 
process_item_list(item_list, trigger_id_to_data)
process_item_list(itemprototype_list, triggerprototype_id_to_data)
process_item_list(discovery_list,'')
