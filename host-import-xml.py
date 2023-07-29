from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import csv
import xml.dom.minidom
import sys
import datetime
import os.path
 
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

def prettify(elem, indent='  '):
    rough_string = tostring(elem, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent=indent)


root = Element('zabbix_export')
SubElement(root, 'version').text = '5.0'
SubElement(root, 'date').text = maketime
groups = SubElement(root, 'groups')
group = SubElement(groups, 'group')
SubElement(group, 'name').text = groupname


hosts = SubElement(root, 'hosts')

for line in data:
    host = SubElement(hosts, 'host')
    SubElement(host,'host').text = line[1]
    SubElement(host,'name').text = line[1]
    SubElement(host,'description').text = crm
    proxy = SubElement(host,'proxy')
    SubElement(proxy,'name').text = line[2]
    SubElement(host,'status').text = 'DISABLED'
    groups = SubElement(host, 'groups')
    group = SubElement(groups, 'group')
    SubElement(group, 'name').text = groupname
    interfaces = SubElement(host, 'interfaces')
    interface = SubElement(interfaces, 'interface')
    SubElement(interface,'type').text = line[3]
    SubElement(interface,'ip').text = line[4]
    SubElement(interface,'port').text = line[5]
    details = SubElement(interface,'details')
    SubElement(details,'community').text = line[6]
    SubElement(interface, 'interface_ref').text = line[7]
    SubElement(host,'inventory_mode').text = 'DISABLED'

f.close()

xml_string = prettify(root)

with open(xmlpath, 'w', encoding='utf-8') as f:
    f.write(xml_string)

print("Success make zabbix host import xml.")
print("Please check the xml.")
print(xmlpath)

