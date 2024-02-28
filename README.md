# Zabbix 업무용 스크립트

## 필수 패키지 설치
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
