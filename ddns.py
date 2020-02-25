from json import load
from urllib.request import urlopen
import os
import time
import datetime
from xml.etree import ElementTree

from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest

class DDNS:
    def __init__(self,config):
        # self.access_key_id = 'LTAIWgr3IoUnlKEz'
        # self.access_key_secret = 'rETR0Cf1ZJdbc3qGeh6t6Q0eWWgT0E'
        # self.local_file_path = 'C:\\Users\\13194\\public_ip.txt'
        # # 域名，主机记录  DomainName, RRKeyWord
        # self.domain_record_list=[['dddqqq.club', 'www']] 
        # self.type_key_word='A'
        # self.time_sleep=600 #单位s

        self.access_key_id = config['access_key_id']
        self.access_key_secret =  config['access_key_secret']
        self.local_file_path =  config['local_file_path']
        # 域名，主机记录  DomainName, RRKeyWord
        self.domain_record_list= config['domain_record_list']
        self.type_key_word= config['type_key_word']
        self.time_sleep= config['time_sleep']#单位s

    #从文件中读取当前的 公网ip
    def get_current_ip(self):
        if os.path.exists(self.local_file_path):
            with open(self.local_file_path, 'r') as local_file:
                line = local_file.readline()
                return line.split(' ')[0]
        else:
            return None
    #获取公网ip
    def get_new_ip(self):
        new_ip = urlopen('http://ip.42.pl/raw').read()
        if new_ip is None:
            new_ip = load(urlopen('http://jsonip.com'))['ip']
        if new_ip is None:
            new_ip = load(urlopen('http://httpbin.org/ip'))['origin']
        if new_ip is None:
            new_ip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
        return str(new_ip,encoding='utf8')

    #将新的ip写入文件
    def write_new_ip(self,new_ip):
        with open(self.local_file_path, 'w') as local_file:
            now = datetime.datetime.now()
            current_time = now.strftime('%Y-%m-%d %H:%M:%S')
            local_file.write(str(new_ip) + ' ' + current_time)
    #更新
    def update_dns(self,new_ip):
        clt = client.AcsClient(self.access_key_id, self.access_key_secret, 'cn-hangzhou')
        for [DomainName, RRKeyWord] in self.domain_record_list:
            request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
            request.set_DomainName(DomainName)
            request.set_TypeKeyWord(self.type_key_word)
            request.set_RRKeyWord(RRKeyWord)
            request.set_accept_format('xml')

            response = clt.do_action(request)

            root = ElementTree.fromstring(response)
            record_id = root.find('DomainRecords/Record/RecordId').text

            request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
            request.add_query_param('RecordId', record_id)
            request.add_query_param('RR', RRKeyWord)
            request.add_query_param('Type', self.type_key_word)
            request.set_accept_format('xml')
            request.set_Value(new_ip)
            response = clt.do_action(request)
            print('Domain {0}.{1} update succeed. new ip address is  {2}.'.format(
                RRKeyWord, DomainName, new_ip))
    def run(self):
        while True:
            new_ip = self.get_new_ip()
            current_ip = self.get_current_ip()
            #当前ip 与 公网ip 不同
            if (current_ip is None and new_ip is not None) or (
                current_ip is not None and new_ip is not None and new_ip != current_ip):
                self.update_dns(new_ip)
                #将新的公网ip写入文件
                self.write_new_ip(new_ip)
            else:
                print('There is no change with ip')
                time.sleep(self.time_sleep)
def read_config():
    with open('ddns_config.json','r') as f:
        config = load(f)
        return config
if __name__ == '__main__':

    config = read_config()
    ddns = DDNS(config)
    # print(config['domain_record_list'])
    ddns.run()
