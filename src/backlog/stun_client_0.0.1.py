#!/usr/bin/python
#coding=utf-8

import socket, sys, struct, binascii, random

#stun attributes
MappedAddress    = '0001'
ResponseAddress  = '0002'
ChangeRequest    = '0003'
SourceAddress    = '0004'
ChangedAddress   = '0005'
Username         = '0006'
Password         = '0007'
MessageIntegrity = '0008'
ErrorCode        = '0009'
UnknownAttribute = '000A'
ReflectedFrom    = '000B'
XorOnly          = '0021'
XorMappedAddress = '8020'
ServerName       = '8022'
SecondaryAddress = '8050' # Non standard extention

#types for a stun message 
BindRequestMsg               = '0001'
BindResponseMsg              = '0101'
BindErrorResponseMsg         = '0111'
SharedSecretRequestMsg       = '0002'
SharedSecretResponseMsg      = '0102'
SharedSecretErrorResponseMsg = '0112'

dictAttrToVal ={'MappedAddress'   : MappedAddress,
                'ResponseAddress' : ResponseAddress,
                'ChangeRequest'   : ChangeRequest,
                'SourceAddress'   : SourceAddress,
                'ChangedAddress'  : ChangedAddress,
                'Username'        : Username,
                'Password'        : Password,
                'MessageIntegrity': MessageIntegrity,
                'ErrorCode'       : ErrorCode,
                'UnknownAttribute': UnknownAttribute,
                'ReflectedFrom'   : ReflectedFrom,
                'XorOnly'         : XorOnly,
                'XorMappedAddress': XorMappedAddress,
                'ServerName'      : ServerName,
                'SecondaryAddress': SecondaryAddress}

dictMsgTypeToVal = {'BindRequestMsg'              :BindRequestMsg,
                    'BindResponseMsg'             :BindResponseMsg,
                    'BindErrorResponseMsg'        :BindErrorResponseMsg,
                    'SharedSecretRequestMsg'      :SharedSecretRequestMsg,
                    'SharedSecretResponseMsg'     :SharedSecretResponseMsg,
                    'SharedSecretErrorResponseMsg':SharedSecretErrorResponseMsg}
           
Blocked = "Blocked"
OpenInternet = "Open Internet"
FullCone = "Full Cone"
SymmetricUDPFirewall = "Symmetric UDP Firewall"
RestricNAT = "Restric NAT"
RestricPortNAT = "Restric Port NAT"
SymmetricNAT = "Symmetric NAT"
ChangedAddressError = "Meet an error, when do Test1 on Changed IP and Port"

def GenTranID():
    a =''
    for i in range(32):
        a+=random.choice('0123456789ABCDEF')
    #return binascii.a2b_hex(a)
    return a

def Test(s, host, port, source_ip, source_port, send_data=""):
    retVal = {'Resp':False, 'ExternalIP':None, 'ExternalPort':None, 'SourceIP':None, 'SourcePort':None, 'ChangedIP':None, 'ChangedPort':None}
    
    str_len = "%#04d" % (len(send_data)/2)
    TranID = GenTranID()
    str_data = ''.join([BindRequestMsg, str_len, TranID, send_data])

    data = binascii.a2b_hex(str_data)
    recvCorr = False
    while not recvCorr:
        recieved = False
        count = 3
        while not recieved:
            print("sendto",(host, port))
            s.sendto(data,(host, port))
            try:
                buf, addr = s.recvfrom(2048)
                print("recvfrom",addr)
                recieved = True
            except Exception:
                recieved = False
                if count >0:
                    count-=1
                else:
                    retVal['Resp'] = False
                    return retVal
        
        MsgType = binascii.b2a_hex(buf[0:2])
        if dictValToMsgType[MsgType] == "BindResponseMsg" and TranID.upper() == binascii.b2a_hex(buf[4:20]).upper():
            recvCorr = True
            retVal['Resp'] = True
            len_message = int(binascii.b2a_hex(buf[2:4]), 16)
            len_remain = len_message
            base = 20
            while len_remain:
                attr_type = binascii.b2a_hex(buf[base:(base+2)])
                attr_len = int(binascii.b2a_hex(buf[(base+2):(base+4)]),16)
                if attr_type == MappedAddress:
                    port = int(binascii.b2a_hex(buf[base+6:base+8]), 16)
                    ip = "".join([str(int(binascii.b2a_hex(buf[base+8:base+9]), 16)),'.',
                    str(int(binascii.b2a_hex(buf[base+9:base+10]), 16)),'.',
                    str(int(binascii.b2a_hex(buf[base+10:base+11]), 16)),'.',
                    str(int(binascii.b2a_hex(buf[base+11:base+12]), 16))])
                    retVal['ExternalIP'] = ip
                    retVal['ExternalPort'] = port
                    
                if attr_type == SourceAddress:
                    port = int(binascii.b2a_hex(buf[base+6:base+8]), 16)
                    ip = "".join([str(int(binascii.b2a_hex(buf[base+8:base+9]), 16)),'.',
                    str(int(binascii.b2a_hex(buf[base+9:base+10]), 16)),'.',
                    str(int(binascii.b2a_hex(buf[base+10:base+11]), 16)),'.',
                    str(int(binascii.b2a_hex(buf[base+11:base+12]), 16))])
                    retVal['SourceIP'] = ip
                    retVal['SourcePort'] = port
                if attr_type == ChangedAddress:
                    port = int(binascii.b2a_hex(buf[base+6:base+8]), 16)
                    ip = "".join([str(int(binascii.b2a_hex(buf[base+8:base+9]), 16)),'.',
                    str(int(binascii.b2a_hex(buf[base+9:base+10]), 16)),'.',
                    str(int(binascii.b2a_hex(buf[base+10:base+11]), 16)),'.',
                    str(int(binascii.b2a_hex(buf[base+11:base+12]), 16))])
                    retVal['ChangedIP'] = ip
                    retVal['ChangedPort'] = port

                if attr_type == ServerName:
                    serverName = buf[(base+4):(base+4+attr_len)]
                base = base + 4 + attr_len
                len_remain = len_remain - (4+attr_len)
    #s.close()
    return retVal

def Initialize():
    items = list(dictAttrToVal.items())
    global dictValToAttr
    dictValToAttr = {}
    for i in range(len(items)):
        dictValToAttr.update({items[i][1]:items[i][0]})
    items = list(dictMsgTypeToVal.items())
    global dictValToMsgType
    dictValToMsgType = {}
    for i in range(len(items)):
        dictValToMsgType.update({items[i][1]:items[i][0]})
    

def GetNATType(s, source_ip, source_port):
    Initialize()
    
    
    host = "stun.ekiga.net" 
    port = 3478

    print("Do Test1")
    ret = Test(s, host, port, source_ip, source_port)
    print("Result:",ret)
    type = None
    exIP = ret['ExternalIP']
    exPort = ret['ExternalPort']
    changedIP = ret['ChangedIP']
    changedPort = ret['ChangedPort']
    
    if not ret['Resp']:
        type = Blocked
    else:
        if ret['ExternalIP'] == source_ip:
            changeRequest = ''.join([ChangeRequest,'0004',"00000006"])
            ret = Test(s, host, port, source_ip, source_port, changeRequest)
            if ret['Resp'] == True:
                type = OpenInternet
            else:
                type = SymmetricUDPFirewall
            
        else:
            changeRequest = ''.join([ChangeRequest,'0004',"00000006"])
            print("Do Test2")
            ret = Test(s, host, port, source_ip, source_port, changeRequest)
            print("Result:",ret)
            
            if ret['Resp'] == True:
                type = FullCone
            else:
                print("Do Test1")
                ret = Test(s, changedIP, changedPort, source_ip, source_port)
                print("Result:",ret)
                
                if not ret['Resp']:
                    type = ChangedAddressError
                else:
                    if exIP == ret['ExternalIP'] and exPort == ret['ExternalPort']:
                        changePortRequest = ''.join([ChangeRequest,'0004',"00000002"])
                        print("Do Test3")
                        ret = Test(s, changedIP, port, source_ip, source_port, changePortRequest)
                        print("Result:",ret)
                        if ret['Resp'] == True:
                            type = RestricNAT
                        else:
                            type = RestricPortNAT
                    else:
                        type = SymmetricNAT
    return (type, exIP, exPort)
    

if __name__ == '__main__':
    socket.setdefaulttimeout(2)
    source_ip = socket.gethostbyname(socket.gethostname())
    source_port = 54320
    
    count = 1
    
    while 1:
        #global s
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((source_ip, source_port))
        
        NatType, exIP, exPort = GetNATType(s, source_ip, source_port)
        print("NAT Type:", NatType)
        print("External IP:", exIP)
        print("External Port:", exPort)
        import time
        time.sleep(60)
    
    
    '''Initialize()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((source_ip, source_port))
    
    print Test(s, "stun.ekiga.net" , 3478, source_ip, source_port)
    
    s.settimeout(60)
    #s.sendto('a', ('202.108.174.66', 23434))
    while 1:
        try:
            buf, addr = s.recvfrom(2048)
            print buf
            print addr
            s.sendto(buf, addr)
        except Exception:
            print "Time Out"'''
    

    s.close()