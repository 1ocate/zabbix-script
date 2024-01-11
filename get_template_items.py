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

def getItemList(session,template_id_to_name):
    templateids = list(template_id_to_name.keys())
    item_datas = session.item.get({ "selectTriggers": ["triggerid"], "expandExpression": "y", "selectApplications": "true", "output": ["hostid", "name", "key_", "delay", "history", "status"], "templateids":templateids })
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
                newItem.append('')
            else:
                newItem.append(item.get('applications')[0].get('applicationid'))
                # newItem.append(application_id_to_name[item.get('applications')[0].get('applicationid')])

            #newItem.append(item.get('applications')[0].get('applicationid'))
            newItem.append(item.get('name'))
            newItem.append(item.get('key_'))
            newItem.append(item.get('delay'))
            newItem.append(item.get('history'))
            if (len(item.get('triggers')) < 1 ):
                newItem.append('X')
                newItem.append('')
                newItem.append('')
                newItem.append('')
                newItem.append('')
                newItem.append('')
                newItem.append(status)
            else:
                newItem.append('O')
                newItem.append(item.get('triggers'))
                newItem.append(status)
            newItem_list.append(newItem)
    else:
        print("아이템을 찾을 수 없습니다.")
        exit()

    return newItem_list

def getTriggerList(session,template_id_to_name):
    priority = [
        "Not classified",
        "Information",
        "Warning",
        "Average",
        "High",
        "Disaster"
    ]
    templateids = list(template_id_to_name.keys())
    # item_datas = session.item.get({"output": ["itemids", "hostid", "name",  "key_", "status"], "templateids":templateids })
    #{'itemid': '26932', 'type': '12', 'snmp_oid': '', 'hostid': '10171', 'name': 'BB +1.8V SM', 'key_': 'bb_1.8v_sm', 'delay': '1m', 'history': '1w', 'trends': '365d', 'status': '0', 'value_type': '0', 'trapper_hosts': '', 'units': 'V', 'formula': '', 'logtimefmt': '', 'templateid': '0', 'valuemapid': '0', 'params': '', 'ipmi_sensor': 'BB +1.8V SM', 'authtype': '0', 'username': '', 'password': '', 'publickey': '', 'privatekey': '', 'flags': '0', 'interfaceid': '0', 'description': '', 'inventory_link': '0', 'lifetime': '30d', 'evaltype': '0', 'jmx_endpoint': '', 'master_itemid': '0', 'timeout': '3s', 'url': '', 'query_fields': [], 'posts': '', 'status_codes': '200', 'follow_redirects': '1', 'post_type': '0', 'http_proxy': '', 'headers': [], 'retrieve_mode': '0', 'request_method': '0', 'output_format': '0', 'ssl_cert_file': '', 'ssl_key_file': '', 'ssl_key_password': '', 'verify_peer': '0', 'verify_host': '0', 'allow_traps': '0', 'state': '0', 'error': '', 'applications': [{'applicationid': '743'}], 'triggers': [{'triggerid': '17117'}, {'triggerid': '17118'}], 'lastclock': '0', 'lastns': '0', 'lastvalue': '0', 'prevvalue': '0'}
    #triggers': [{'triggerid': '17117', 'expression': '{20124}<1.597 or {20124}>2.019', 'description': 'BB +1.8V SM Critical [{ITEM.VALUE}]', 'url': '', 'status': '0', 'value': '0', 'priority': '5', 'lastchange': '0', 'comments': '', 'error': '', 'templateid': '0', 'type': '0', 'state': '0', 'flags': '0', 'recovery_mode': '0', 'recovery_expression': '', 'correlation_mode': '0', 'correlation_tag': '', 'manual_close': '0', 'opdata': ''
    #item_datas = session.item.get({ "selectTriggers": ["expression","description","status","recovery_expression","priority" "selectApplications","opdata"], "expandExpression": "y", "selectApplications": "true", "output": ["hostid","name","key_","delay","history"], "templateids":templateids })
    trigger_datas = session.trigger.get({ "selectTriggers": ["triggerid"],  "expandExpression": "y", "expandDescription": "y", "output": ["expression","description","status","recovery_expression","priority", "opdata"], "templateids":templateids })
    result = {}

    # 정규식 패턴
    # pattern = r"\[(.*?)\]"

    for data in trigger_datas:
        expression = data.get('expression').replace('\n', '').replace('\r', '')
        result[data.get('triggerid')] = f"{data.get('description')}!{expression}!{data.get('recovery_expression')}!{priority[int(data.get('priority'))]}!{data.get('opdata')}!{data.get('status')}"
        # matches = re.findall(pattern, data.get('description'))
        # print(matches)
    return result

# 파일리스트 가져오기
file_path = template_list_file
with open(file_path, 'r') as file:
    lines = file.read().splitlines()
    template_list = [line for line in lines]

session = login(zabbix_name)
# application_id_to_name = getApplicationList(session,)
template_id_to_name = getTemplateList(session,template_list,'')
trigger_id_to_data = getTriggerList(session,template_id_to_name)
item_list = getItemList(session,template_id_to_name)

for item in item_list:
     if (len(item[7]) == 0):
        item[7] = ""
     else:
        item[7] = ", ".join([trigger_id_to_data[sub_dict['triggerid']] for sub_dict in item[7]])
     print('!'.join(map(str, item)))

