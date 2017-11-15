# -*- coding: utf-8 -*-
import requests
from lxml import etree
import json
import hashlib
session1 = requests.Session()
session1_base_url='http://javhihi.com/'
session1_uri='movie?sort=published&page=1'
session1_url=session1_base_url+session1_uri
session1_headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'}
headers = {'Content-Type': 'application/json'}
r1 = session1.get(url=session1_url,headers=session1_headers)
html=str(r1.content)
selector = etree.HTML(html)
xp=selector.xpath("//div[@class='item-thumbnail']/a/@href")
for x in xp:
    r2=None
    url = session1_base_url+x
    r2=session1.get(url=url, headers=session1_headers)
    html2 = str(r2.content)
    selector2 = etree.HTML(html2)
    xp2 = selector2.xpath("//div[@class='btn-group']/ul/li/a/@href")
    tmp = xp2[2].split('/')
    for x in tmp:
        if x.find('mp4') != -1:
            #print x.split('?')[0]
            gid = hashlib.md5(x.split('?')[0]).hexdigest()[8:-8]
            #print gid
    addurl = {
        "jsonrpc": "2.0",
        "id": "Python",
        "method": "system.multicall",
        "params": [
            [
                {
                    "methodName": "aria2.addUri",
                    "params": [
                        [xp2[2]],
                        {
                            "dir": "Aria2Data",
                            "gid": gid
                        }
                    ]
                }
            ]
        ]
    }
    print requests.post(url='http://localhost:6800/jsonrpc', headers=headers, data=json.dumps(addurl)).text
    #print addurl
