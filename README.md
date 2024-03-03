# Zabbix 업무용 스크립트

## 준비

### 실행 환경 
* python =< 3.10.12
* pip =<  22.0.2

### 필수 패키지 설치
```bash
# pip 또는 pip3
$ pip3 install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt
```

### 접속정보 작성
config.json.exmple 내용을 참조하여 config.json 파일 생성

```json
{
  "ZabbixServerInfo": {
    "zabbix_name": {
      "user": "",
      "password": "",
      "URL": ""
    }
  }
}
```
exmple: 2개의 Zabbix 접속 정보 local, stage 등록
```json
{
  "ZabbixServerInfo": {
    "local": {
      "user": "local-user",
      "password": "local-password",
      "URL": "http://zabbix.local/zabbix/"
    },
    "stage": {
      "user": "stage-user",
      "password": "stage-password",
      "URL": "http://zabbix.local/zabbix/"
    }
  }
}
```
### Zabbix 접속 확인
#### auth.py

```bash
# python 또는 python3
# 로그인 실패. 접속 정보 확인
$ python3 auth.py local
로그인 실패

# 로그인 성공
# python 또는 python3
$ python3 auth.py local
local서버에 Admin으로 로그인 하였습니다.
로그아웃 완료
```
## 실행

### Zabbix에 수용 여부 확인
#### get_host.py
```bash
# 수용 확인 할  호스트 리스트 작성
$ cat api_test_list
TEST_HOST_HP_G7
TEST_SERVER
TEST_HOST_10.10.10.10

# 사용법
# <zabbix_name> = 수용 확인 대상 Zabbix Server
# <host_list_file> = 수용 확인 할 호스트 리스트 파일 이름
# python 또는 python3
$ python3 get_host.py
Usage: python3 get_host.py <zabbix_name> <host_list_file>

$ python3 get_host.py STAGE api_test_list
기 수용 대상
TEST_SERVER|10.4.224.35
수용 예정 대상
TEST_HOST_HP_G7|10.9.224.110
TEST_HOST_10.10.10.10|10.4.224.29
총 검색 대상 대수 3
총 검색 결과 기 수용 대수 (템플릿 적용) 1
총 검색 결과 수용 예정 (템플릿 미적용) 2
로그아웃 완료
```
### Zabbix에 수용된 전체 대상 확인
#### get_all_host.py
```bash
# 사용법
# <zabbix_name> = 수용 확인 대상 Zabbix Server
# python 또는 python3
❯ python3 get_all_host.py
Usage: python3 get_all_host.py <zabbix_name>

$ python3 get_all_host STAGE
IP|수용 대상|템플릿 적용|활성화
10.9.152.69|STAGE|O|X|Zabbix_proxy
10.9.152.70|STAGE|O|X|Zabbix_proxy
10.9.152.71|STAGE|O|X|Zabbix_proxy
10.9.152.72|STAGE|O|X|Zabbix_proxy
10.9.152.73|STAGE|O|X|Zabbix_proxy
10.9.152.74|STAGE|O|X|Zabbix_proxy
10.9.152.75|STAGE|O|X|Zabbix_proxy
10.9.152.76|STAGE|O|X|Zabbix_proxy
10.9.152.77|STAGE|O|X|Zabbix_proxy
10.9.152.78|STAGE|O|X|Zabbix_proxy
10.9.152.79|STAGE|O|X|Zabbix_proxy
10.9.152.81|STAGE|O|X|Zabbix_proxy
10.3.198.34|STAGE|O|X|No Proxy
10.3.198.37|STAGE|O|X|No Proxy
10.3.198.113|STAGE|O|X|No Proxy
총 검색 결과 수용 대수 365
로그아웃 완료
```

### Zabbix 템플릿 확인
#### get_template_from_list.py
```bash
$ cat template_list
Template App Zabbix Server

# 사용법
# <zabbix_name> = 수용 확인 대상 Zabbix Server
# <template_list_file> = 가져올 템플릿 리스트
# python 또는 python3
$ python3 get_template_from_list
Usage: python3 get_template_from_list.py <zabbix_name> <template_list_file>

$ python3 get_template_from_list.py local template_list
Template App Zabbix Server@Zabbix server@Zabbix server: LLD queue@X@zabbix[lld_queue]@1m@1w@활성@X@@@@@
Template App Zabbix Server@Zabbix server@Zabbix server: Preprocessing queue@X@zabbix[preprocessing_queue]@1m@1w@활성@X@@@@@
Template App Zabbix Server@Zabbix server@Zabbix server: Utilization of alert manager internal processes, in %@X@zabbix[process,alert manager,avg,busy]@1m@1w@활성@O@@Zabbix server: Utilization of alert manager processes over 75%@{Template App Zabbix Server:zabbix[process,alert manager,avg,busy].avg(10m)}>75@{Template App Zabbix Server:zabbix[process,alert manager,avg,busy].avg(10m)}<65@Average@@활성
Template App Zabbix Server@Zabbix server@Zabbix server: Utilization of alert syncer internal processes, in %@X@zabbix[process,alert syncer,avg,busy]@1m@1w@활성@O@@Zabbix server: Utilization of alert syncer processes over 75%@{Template App Zabbix Server:zabbix[process,alert syncer,avg,busy].avg(10m)}>75@{Template App Zabbix Server:zabbix[process,alert syncer,avg,busy].avg(10m)}<65@Average@@활성
```

### Zabbix 수용 대상 중 Zabbix에 등록된 호스트명, Agent에서 가져오는 호스트명 다른 대상 확인
* 10분 이상 큐 발생 및 Active 아이템 수집 불가 대상 확인

#### check_host_dubble.py

```bash
# 사용법
# <zabbix_name> = 확인 대상 Zabbix Server
# python 또는 python3
$ python3 check_host_dubble.py
Usage: python3 check_host_dubble.py <zabbix_name>

$ python3 check_host_dubble.py STAGE
로그아웃 완료
host_name|agent_host_name
p-mon-grafana-01_Testtest|p-mon-grafana-01_10.4.224.29
p-mon-grafana-01_10.4.224.29_test|p-mon-grafana-01_10.4.224.29

```
### Zabbix 호스트 그룹에서 호스트 이름, IP 가져오기
#### get_group_host.py
```bash
# 사용법
# <zabbix_name> = 호스트 그룹이 존재하는 Zabbix Server
# <group_name> = Zabbix 호스트 그룹 이름
# python 또는 python3
$ python3 get_group_host.py
Usage: python3 get_group_host.py <zabbix_name> <group_name>

$ python3 get_group_host.py STAGE api_test
TEST_HOST_HP_G7|10.9.224.110
TEST_SERVER|10.4.224.35
TEST_HOST_10.10.10.10|10.4.224.29
```

### Zabbix 호스트 그룹 묶기
#### set_group_by_name.py
```bash
# 그룹으로 묶을 호스트 작성
$ cat api_test_list
TEST_HOST_HP_G7
TEST_SERVER
TEST_HOST_10.10.10.10

# 사용법
# <zabbix_name> = 호스트 그룹이 존재하는 Zabbix Server
# <group_name> = Zabbix 호스트 그룹 이름
# <host_list_file> = 그룹으로 묶을 호스트 작성
# python 또는 python3
$ python3 set_group_by_name.py
Usage: python3 set_group_by_name.py <zabbix_name> <group_name> <host_list_file>

$ python3 set_group_by_name.py STAGE set_group_test api_test_list
그룹을 찾을 수 없습니다.
set_group_test 그룹을 생성할까요?y
set_group_test 그룹이 생성되었습니다.
STAGE의 set_group_test 업데이트가 완료 되었습니다.
로그아웃 완료
```

