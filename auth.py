from zabbix_api import ZabbixAPI
import json
import sys
import logging

f = open("config.json", encoding="UTF-8")
CONFIG = json.loads(f.read())
f.close()


def login(zabbix_name):
    try:
        config = CONFIG['ZabbixServerInfo'][zabbix_name]
        zabbix_url = config['URL']
        zabbix = ZabbixAPI(server=zabbix_url)
        zabbix.login(config['user'],config['password'])

        if __name__ == "__main__":
            print(f"{zabbix_name}서버에 {config['user']}으로 로그인 하였습니다.")

        return zabbix

    except KeyError:
        print("서버 정보가 올바르지 않습니다.")

    except:
        print("로그인 실패")
        exit()

def logout(session):
    try:
       session.logout()
       print("로그아웃 완료")

    except:
        print("이미 로그아웃 되었습니다.")
        exit()

def main(argv):
    if len(argv) != 2:
        print("Usage: python3 auth.py <zabbix_name> ")
        sys.exit(1)

    zabbix_name = argv[1]
    session = login(zabbix_name)
    logout(session)

if __name__ == "__main__":
    argv = sys.argv
    main(argv)
