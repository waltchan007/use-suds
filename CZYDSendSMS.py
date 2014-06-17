# -*- coding: utf-8 -*-
'''
Created on 2014年6月13日

@author: waltChan
@note:   常州移动短信接口发短信测试程序
'''

import suds
from suds.client import Client
from suds.plugin import MessagePlugin

import hashlib
import sys
import time

class EnvelopeFixer(MessagePlugin):
    
    
    def marshalled(self, context):
        nsprefixe = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance', \
                              'xsd': 'http://www.w3.org/2001/XMLSchema', \
                              'soapenc': 'http://schemas.xmlsoap.org/soap/encoding/', \
                              'tns': 'http://tempuri.org/', \
                              'types': 'http://tempuri.org/encodedTypes', \
                              'soap': 'http://schemas.xmlsoap.org/soap/envelope/'
                              ''}
        
        root = context.envelope.getRoot()
        envelope = root.getChild("Envelope")
        envelope.remove(envelope.getChildren()[0])
        Body = envelope.getChild('Body')
        SendSms = envelope.getChild('Body').getChild('SendSms')
        
        envelope.remove(envelope.getAttribute('encodingStyle'))
        
        Body.prefix = None
        SendSms.prefix = None
        envelope.prefix = None
        
        SendSms.refitPrefixes()
        envelope.refitPrefixes()
        
        for prefix,namespace in nsprefixe.items():
            envelope.addPrefix(prefix,namespace)
        
        envelope.setPrefix('soap')
        envelope.getChildren()[0].setPrefix('soap')
        SendSms.getChildren()[0].set('xsi:type','xsd:string')
        SendSms.getChildren()[1].set('xsi:type','xsd:string')
        SendSms.getChildren()[2].set('xsi:type','xsd:string')
        SendSms.getChildren()[3].set('xsi:type','xsd:string')
        
        root = context.envelope.getRoot()
        return context

if __name__ == '__main__':
    url = 'http://www.cz10086.net/czmobile/WebService/SmsNowService.asmx?WSDL'
    usr = 'test'
    tmp = 'test'
    
    m = hashlib.md5()
    m.update(tmp)
    pwd = m.hexdigest()
    
#     if len(sys.argv) < 2:
#         print "mobile is null,please input mobile"
#         exit
#     mobile = sys.argv[1]
    mobiles = ('18607143299','1')
    
    if len(sys.argv) < 3:
        tmp = '短信接口测试短信,发送时间'+time.strftime('%Y-%m-%d %X',time.localtime())+',请记录收到短信的时间！'
    else:
        tmp = sys.argv[2]     
    msg = unicode(tmp,'utf-8')
    print 'begin'
    for mobile in mobiles: 
        try:
            client = Client(url, plugins=[EnvelopeFixer()] ,faults = False)
            tupleResult = client.service.SendSms(usr, pwd, mobile, msg)
        except suds.WebFault:
            raise
        print tupleResult
    print 'end'