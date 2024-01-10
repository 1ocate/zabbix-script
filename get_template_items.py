from auth import login, logout
import math
import time
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


def getApplicationList(sesison):
    application_datas = sesison.application.get({ "output": ["applicationid", "name"]})
    result = {}
    result = {}
    for data in application_datas:
        result[data.get('applicationid')] = data.get('name')

    return result
def getItemList(session,template_id_to_name,application_id_to_name):
    templateids = list(template_id_to_name.keys())
    # item_datas = session.item.get({"output": ["itemids", "hostid", "name",  "key_", "status"], "templateids":templateids })
    #{'itemid': '26932', 'type': '12', 'snmp_oid': '', 'hostid': '10171', 'name': 'BB +1.8V SM', 'key_': 'bb_1.8v_sm', 'delay': '1m', 'history': '1w', 'trends': '365d', 'status': '0', 'value_type': '0', 'trapper_hosts': '', 'units': 'V', 'formula': '', 'logtimefmt': '', 'templateid': '0', 'valuemapid': '0', 'params': '', 'ipmi_sensor': 'BB +1.8V SM', 'authtype': '0', 'username': '', 'password': '', 'publickey': '', 'privatekey': '', 'flags': '0', 'interfaceid': '0', 'description': '', 'inventory_link': '0', 'lifetime': '30d', 'evaltype': '0', 'jmx_endpoint': '', 'master_itemid': '0', 'timeout': '3s', 'url': '', 'query_fields': [], 'posts': '', 'status_codes': '200', 'follow_redirects': '1', 'post_type': '0', 'http_proxy': '', 'headers': [], 'retrieve_mode': '0', 'request_method': '0', 'output_format': '0', 'ssl_cert_file': '', 'ssl_key_file': '', 'ssl_key_password': '', 'verify_peer': '0', 'verify_host': '0', 'allow_traps': '0', 'state': '0', 'error': '', 'applications': [{'applicationid': '743'}], 'triggers': [{'triggerid': '17117'}, {'triggerid': '17118'}], 'lastclock': '0', 'lastns': '0', 'lastvalue': '0', 'prevvalue': '0'}
    #triggers': [{'triggerid': '17117', 'expression': '{20124}<1.597 or {20124}>2.019', 'description': 'BB +1.8V SM Critical [{ITEM.VALUE}]', 'url': '', 'status': '0', 'value': '0', 'priority': '5', 'lastchange': '0', 'comments': '', 'error': '', 'templateid': '0', 'type': '0', 'state': '0', 'flags': '0', 'recovery_mode': '0', 'recovery_expression': '', 'correlation_mode': '0', 'correlation_tag': '', 'manual_close': '0', 'opdata': ''
    #item_datas = session.item.get({ "selectTriggers": ["expression","description","status","recovery_expression","priority" "selectApplications","opdata"], "expandExpression": "y", "selectApplications": "true", "output": ["hostid","name","key_","delay","history"], "templateids":templateids })
    item_datas = session.item.get({ "selectTriggers": ["triggerid"], "expandExpression": "y", "selectApplications": "true", "output": ["hostid","name","key_","delay","history","status"], "templateids":templateids })
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
            newItem.append(application_id_to_name[item.get('applications')[0].get('applicationid')])
            #newItem.append(item.get('applications')[0].get('applicationid'))
            newItem.append(item.get('name'))
            newItem.append(item.get('key_'))
            newItem.append(item.get('delay'))
            newItem.append(item.get('history'))
            newItem.append(item.get('triggers'))
            newItem.append(status)
            newItem_list.append(newItem)
    else:
        print("아이템을 찾을 수 없습니다.")
        exit()

    return newItem_list
# 파일리스트 가져오기
file_path = template_list_file
with open(file_path, 'r') as file:
    lines = file.read().splitlines()
    template_list = [line for line in lines]

session = login(zabbix_name)
template_id_to_name = getTemplateList(session,template_list,'')
application_id_to_name = getApplicationList(session)
item_list = getItemList(session,template_id_to_name,application_id_to_name)
for item in item_list:
     if (len(item[6]) == 0):
        item[6] = ""
     else:
         item[6] = ", ".join([sub_dict['triggerid'] for sub_dict in item[6]])

     print('|'.join(map(str, item)))
    # if (len(item[6]) > 0):
    #     for trigger in item[6]:
    #         print(trigger)     
    

# def generateItemList(location, templateName, fileName):
#     itemList = getItemlist(location, templateName, outputFile ='')
#     print(f"{fileName}:{location}, item 총 {len(itemList)}개 ")
#     return itemList

# def generateDiffItemList(itemList, fileName):
#     print(f"{fileName}과 비교대상 중 누락 또는 활성 상태가 다른 아이템 총 {len(itemList)}개 ")
#     if (len(itemList) > 0):
#         outputFile = open(f'./item/{fileName}-diff-item-list', 'w')
#         for item in itemList:
#             print_and_write(outputFile,item)
#         outputFile.close()
#     print(f"\n")



# template_names = getCommonTemplateName(origin,target)
# originItemList = generateItemList(origin,template_names,"origin")

# targetItemList = generateItemList(target,template_names,"target")
# originItemList.sort
# targetItemList.sort
# # origin에는 있지만 target에는 없는 요소 찾기
# not_in_target = [item for item in originItemList if item not in targetItemList]
# # not_in_target = [item for item in originItemList if all(item_part not in targetItemList for item_part in [item[0], item[2], item[3], item[4]])]

# # target에는 있지만 origin에는 없는 요소 찾기
# not_in_origin = [item for item in targetItemList if item not in originItemList]

# report_file = open(f'./item/report_template_{origin}.log', 'w')
# needActiveItem = []
# needDisableItem = []
# for template in template_names:

#     not_in_target_templates = [item for item in originItemList if template in item]
#     not_in_origin_templates = [item for item in targetItemList if template in item]

#     not_in_target_templates_item = []
#     not_in_origin_templates_item = []

#     for not_in_target_row in not_in_target_templates:
#         row = []
#         row.append(not_in_target_row[2])
#         row.append(not_in_target_row[3])
#         row.append(not_in_target_row[4])
#         not_in_target_templates_item.append(row)

#     for not_in_origin_row in not_in_origin_templates:
#         row = []
#         row.append(not_in_origin_row[2])
#         row.append(not_in_origin_row[3])
#         row.append(not_in_origin_row[4])
#         not_in_origin_templates_item.append(row)

#     not_in_target_template = [item for item in not_in_target_templates_item ]
#     not_in_target_template_name = []
#     for item in not_in_target_template:
#         not_in_target_template_name.append(item[0])

#     not_in_origin_template = [item for item in not_in_origin_templates_item ]
#     not_in_origin_template_name = []
#     for item in not_in_origin_template:
#         not_in_origin_template_name.append(item[0])
#     not_in_target_template_name.sort()
#     not_in_origin_template_name.sort()
#     # exit()

#     if len(not_in_target_template_name) > 0 or len(not_in_origin_template_name) > 0:
#         print_and_write(report_file,f'----------------{template}---------------------')

#         if len(not_in_target_template_name) > 0:
#             print_and_write(report_file,f'\n 복사본 {target} 아이템 {len(not_in_target_template_name)}개')
#             print_and_write(report_file, '--------------------------------------------')

#             for item in not_in_target_templates:
#                 row = []
#                 itemIdStatus = []
#                 if item[2] in not_in_target_template_name:
#                     row.append(item[1])
#                     row.append(item[2])
#                     row.append(item[3])
#                     row.append(item[4])
#                     itemIdStatus.append(item[1])
#                     itemIdStatus.append(item[4])
#                     if item[4] == '활성':
#                        needActiveItem.append(itemIdStatus)
#                     elif item[4] == '비활성':
#                        needDisableItem.append(itemIdStatus)

#                     # 활성화 해야할 아이템 리스트 생성
#                     print_and_write(report_file,row)

#         if len(not_in_origin_template_name) > 0:
#             print_and_write(report_file,f'\n 원본 {origin} 아이템 {len(not_in_origin_template_name)}개')
#             print_and_write(report_file, '--------------------------------------------')

#             for item in not_in_origin_templates:
#                 row = [] 

#                 if item[2] in not_in_origin_template_name:
#                     # row.append(item[1])
#                     row.append(item[2])
#                     row.append(item[3])
#                     row.append(item[4])
#                     # 활성화 해야할 아이템 리스트 생성
#                     print_and_write(report_file,row)

#         print_and_write(report_file,'\n')
# report_file.close()

# # generateDiffItemList(not_in_origin, "\norigin")
# # generateDiffItemList(not_in_target, "target")

# endTime = time.time() - startTime
# print(f"{endTime} 초 소요")
# print(len(needActiveItem))
# print(len(needDisableItem))
