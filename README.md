# ddns
> 该脚本主要是根据 <https://www.chiphell.com/thread-1711001-1-1.html> 修改而来

脚本同目录下一个文件 ddns_config.json
```json
{
    "//": "阿里云的access_key_id ，在阿里云管理界面头像找",
    "access_key_id" :"adgasgas",
    "//":"同上",
    "access_key_secret" :"dasgagasgasgasgasgasdg",
    "//":"保存当前ip",
    "local_file_path":"public_ip.txt",
    "domain_record_list":[
         ["**.com", "www"] ,
         ["**.com","@"],
        ] ,
   "//":"检测时间间隔  单位s",
   "type_key_word":"A", 
   "time_sleep": 600 
}
```
## 打包命令
```shell
pyinstaller -F --hidden-import=queue ddns.py
```
