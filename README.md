# ddns
脚本下一个文件 ddns_config.json
```json
{
    "access_key_id" : #阿里云的access_key_id ，在阿里云管理界面头像找
     "access_key_secret" : #同上
     "local_file_path":"public_ip.txt",#保存当前ip
     "domain_record_list":[
         ["**.com", "www"] ,
         ["**.com","@"], ...
        ] ,
    "type_key_word":"A", 
    "time_sleep": 600 # 检测时间间隔  单位s
}
```
