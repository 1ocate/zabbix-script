# Zabbix 업무용 스크립트

## 접속 정보 등록

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
