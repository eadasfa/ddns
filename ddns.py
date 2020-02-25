from json import load
from urllib.request import urlopen

import os
import datetime
from xml.etree import ElementTree

from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest

access_key_id = ''
access_key_secret = ''

local_file_path = 'C:\\Users\\13194\\public_ip.txt'

if os.path.exists(local_file_path):

    with open(local_file_path, 'r') as local_file:
        line = local_file.readline()
        current_ip = line.split(' ')[0]
else:

    current_ip = None

new_ip = urlopen('http://ip.42.pl/raw').read()
if new_ip is None:
    new_ip = load(urlopen('http://jsonip.com'))['ip']
if new_ip is None:
    new_ip = load(urlopen('http://httpbin.org/ip'))['origin']
if new_ip is None:
    new_ip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
new_ip=str(new_ip,encoding='utf8')
# print('current_ip: '+ str(current_ip))
# print('new_ip: '+ str(new_ip))
# print(new_ip==current_ip)
if (current_ip is None and new_ip is not None) or (
        current_ip is not None and new_ip is not None and new_ip != current_ip):

    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')

    domain_record_list = [['***.club', 'www']]

    for [DomainName, RRKeyWord] in domain_record_list:

        request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_DomainName(DomainName)
        request.set_TypeKeyWord('A')
        request.set_RRKeyWord(RRKeyWord)
        request.set_accept_format('xml')

        response = clt.do_action(request)

        root = ElementTree.fromstring(response)
        record_id = root.find('DomainRecords/Record/RecordId').text

        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.add_query_param('RecordId', record_id)
        request.add_query_param('RR', RRKeyWord)
        request.add_query_param('Type', 'A')
        request.set_accept_format('xml')
        request.set_Value(new_ip)

        response = clt.do_action(request)

        print('domain {0}.{1} update succeed. new ip address is  {2}.'.format(
            RRKeyWord, DomainName, new_ip))

    with open(local_file_path, 'w') as local_file:
        now = datetime.datetime.now()
        current_time = now.strftime('%Y-%m-%d %H:%M:%S')
        local_file.write(str(new_ip) + ' ' + current_time)
