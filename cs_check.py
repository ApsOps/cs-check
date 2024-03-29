#!/usr/bin/env python2
import Queue
import socket
import threading
import time
from netaddr import IPNetwork
from struct import *

socket.setdefaulttimeout(0.05)

def extractInfo(txt):
    txt=txt.replace('\377', '')
    if txt.find('m') == 0:
        serv_name=txt.split('\0') [1]
        serv_map=txt.split('\0') [2]
        serv_engine=txt.split('\0') [3]
        serv_game=txt.split('\0') [4]
        players = unpack('bb',txt.split('\0')[5][:2])
        #if txt.split('\0')[9][:1] == '\0':
        #    protected = True
        #else:
        #    protected = False
        print ' Server IP appended '
        return serv_name+" -- "+serv_map+" ("+str(players[0])+"/"+str(players[1])+" players)"
    else:
        return ''

class ClientThread (threading.Thread):
    def run (self):
        global serverList
        ip = None
        while True:
            if not ipPool.empty():
                try:
                    ip = ipPool.get_nowait()
                except Exception,e:
                    break
            else:
                break
            if ip != None:
                found = False
                serverLine = ''+ip+'\t:\t'
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                try:
                    sock.connect((ip, 27015))
                except Exception,e:
                    sock.close()
                    print e
                    break
                sock.send('\377\377\377\377TSource Engine Query\0')
                while 1:
                    try:
                        text=sock.recv(1024)
                        print ' Message Received from '+ip
                    except Exception,e:
                        break
                    if not text:
                        break
                    found = True
                    info = extractInfo(text)
                    if info != '':
                        serverLine += info
                        break
                    else:
                        found = False
                        break
                if found:
                    serverList.append(serverLine)
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()

subnetList = [
                "172.16.1.0/24",
                "172.16.2.0/24",
                "172.16.3.0/24",
                "172.16.4.0/24",
                "172.16.5.0/24",
                "172.16.6.0/24",
                "172.16.7.0/24",
                "172.16.8.0/24",
                "172.16.9.0/24",
                "172.16.10.0/24",
                "172.16.11.0/24",
                "172.16.12.0/24",
                "172.16.13.0/24",
                "172.16.14.0/24",
                "172.16.15.0/24",
                "172.16.16.0/24",
                "172.16.17.0/24",
                "172.16.18.0/24",
                "172.16.19.0/24",
                "172.16.20.0/24",
                "172.17.1.0/24",
                "172.17.2.0/24",
                "172.17.3.0/24",
                "172.17.4.0/24",
                "172.17.5.0/24",
                "172.17.6.0/24",
                "172.17.7.0/24",
                "172.17.8.0/24",
                "172.17.9.0/24",
                "172.17.10.0/24",
                "172.17.11.0/24",
                "172.17.12.0/24",
                "172.17.13.0/24"
             ]
ipPool = Queue.Queue(0)
global serverList
serverList = []
fileName = "C:/xampp/htdocs/index.php"

def checkIPs():
    global serverList
    serverList = ["","<html><head><title>SIDS-PC</title><style>\nhtml {\nbackground: url(bg.jpg) no-repeat center center fixed;\n-webkit-background-size: cover;\n-moz-background-size: cover;\n-o-background-size: cover;\nbackground-size: cover;\n}\nbody {\nfont-family: 'Segoe UI', 'Gill Sans MT', Helvetica;\nfont-size: 16px;\nfont-weight: bold;\n}\n\ndiv {\nheight: auto;\nwidth: 500px;\npadding-top: 100px;\npadding-right: 500px;\npadding-bottom: 100px;\npadding-left: 350px;\n}</style></head><body><div><pre>(Auto updated every minute)",""]
    for subnet in subnetList:
        for ip in IPNetwork(subnet).iter_hosts():
            ipPool.put('%s' % ip)
    for x in xrange(100):
        ClientThread().start()
    while threading.activeCount() > 1:
        time.sleep(1)

while True:
    checkIPs()
    serverList.append("")
    serverList.append("Last updated at: "+time.strftime('%I:%M %p, %b %d, %Y'))
    serverList.append("</pre></div></body></html>")
    print time.strftime('%I:%M %p, %b %d, %Y'), '-- MARK --'
    f = open(fileName, "w")
    for s in serverList:
        f.write(s)
        f.write('\n')
    f.close()
    time.sleep(50)
