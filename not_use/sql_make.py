from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import csv
import xml.dom.minidom
import sys
import datetime
import os.path

def printSql(data):
    sql = []
    for line in data:
        sql.append(f"select '{line[4]}' as 'ip'")

    for index, line in enumerate(sql):
        if index == 0:
            print(f"    {line}")
        else:
            print(f"    union all {line}")

if len(sys.argv) != 2:
    print("Please input CRM.")
    sys.exit(1)

now = datetime.datetime.now()
todaymonthdate = now.strftime('%m%d')
maketime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


crm = sys.argv[1]
groupname = todaymonthdate + '_' + crm


csvpath = './' + crm + '.csv'
xmlpath = './' + crm + '.xml'
check_file = os.path.isfile(csvpath)

if not check_file:
    print("Please check csv file name or exists.")
    print("csv path must be")
    print(csvpath)
    sys.exit(1)

f = open(crm+'.csv', 'r', encoding='utf-8')
data = csv.reader(f)

print(f"with test as (")
printSql(data)
print(f") ")

f.close()
# with open(xmlpath, 'w', encoding='utf-8') as f:
#     f.write(xml_string)

# print("Success make zabbix host import xml.")
# print("Please check the xml.")
# print(xmlpath)

