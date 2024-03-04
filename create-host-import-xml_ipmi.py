from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import csv
import xml.dom.minidom
import sys
import datetime
import os.path
 
now = datetime.datetime.now()
todaymonthdate = now.strftime('%m%d')
maketime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def print_usage():
    print("Usage: create-host-import-xml <CRM> <date>")
    print("  <CRM>: Work number")
    print("  <date>: Work date in the format mmdd (e.g., 1015)")

if len(sys.argv) != 3:
    print_usage()
    sys.exit(1)

crm = sys.argv[1]
workdate = sys.argv[2]

if not crm:
    print("Error: Please provide a CRM.")
    sys.exit(1)

if not workdate:
    print("Error: Please provide a work date in the format mmdd (e.g., 1015).")
    sys.exit(1)

if not workdate.isdigit() or len(workdate) != 4:
    print("Error: Invalid date format. Please use mmdd (e.g., 1015).")
    sys.exit(1)

groupname = workdate + '_' + '수용' + '_' + crm

csvfilename = crm[-4:]
csvpath = './' + csvfilename + '.csv' 
xmlpath = './' + crm + '.xml'
check_file = os.path.isfile(csvpath)

if not check_file:
    print("Please check csv file name or exists.")
    print("csv path must be")
    print(csvpath)
    sys.exit(1)


f = open(csvpath, 'r', encoding='utf-8')

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
    SubElement(host,'host').text = line[2]
    SubElement(host,'name').text = line[2]
    SubElement(host,'description').text = ''
    proxy = SubElement(host,'proxy')
    SubElement(host,'ipmi_username').text= line[9]
    SubElement(host,'ipmi_password').text= line[10]
    templates = SubElement(host, 'templates')
    template = SubElement(templates, 'template')
    SubElement(template, 'name').text = line[4]
    SubElement(proxy,'name').text = line[6]
    SubElement(host,'status').text = 'DISABLED'
    groups = SubElement(host, 'groups')
    group = SubElement(groups, 'group')
    SubElement(group, 'name').text = groupname
    group = SubElement(groups, 'group')
    SubElement(group, 'name').text = line[1]
    interfaces = SubElement(host, 'interfaces')
    interface = SubElement(interfaces, 'interface')
    SubElement(interface,'type').text = 'IPMI'
    SubElement(interface,'ip').text = line[3]
    SubElement(interface,'port').text = '623'
    # details = SubElement(interface,'details')
    # SubElement(details,'community').text = line[8]
    SubElement(interface, 'interface_ref').text = 'if1'
    SubElement(host,'inventory_mode').text = 'DISABLED'
    macros = SubElement(host, 'macros')
    macro = SubElement(macros, 'macro')
    SubElement(macro, 'macro').text='{$PASSWORD}'
    SubElement(macro, 'type').text='SECRET_TEXT'
    SubElement(macro, 'value').text=line[10]
    macro2 = SubElement(macros, 'macro')
    SubElement(macro2, 'macro').text='{$USER}'
    SubElement(macro2, 'value').text=line[9]


f.close()

xml_string = prettify(root)

with open(xmlpath, 'w', encoding='utf-8') as f:
    f.write(xml_string)

print("Success create zabbix host import xml.")
print("Please check the xml.")
print(f"Group name is {groupname}")
print(xmlpath)

