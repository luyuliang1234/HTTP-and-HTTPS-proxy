import socket as s
from socket import SHUT_RDWR
import threading as th
import time
def rec(conn,data):
    try:
        target=data.split(' ')[1].split(":")
        remote_ip=s.gethostbyname(target[0])
        remote_port=int(target[1])
        print(target[0])
        t=s.socket(s.AF_INET,s.SOCK_STREAM)
        t.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
        conn.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
        t.settimeout(30)
        conn.settimeout(30)
        t.connect((remote_ip,remote_port))
    except:
        conn.shutdown(SHUT_RDWR)
        conn.close()
        return
    conn.send(b'HTTP/1.1 200 Connection Established\r\n\r\n')
    a=th.Thread(target=proxy,args=(conn,t))
    a.start()
    temp=b'1'
    while temp:
        try:
            temp=conn.recv(2048)
            t.send(temp)
        except:
            break
    try:
        t.shutdown(SHUT_RDWR)
        conn.shutdown(SHUT_RDWR)
        t.close()
        conn.close()
    except:
        return
def proxy(conn,t):
    temp=b'1'
    while temp:
        try:
            temp=t.recv(2048)
            conn.send(temp)
        except:
            break
    try:
        t.shutdown(SHUT_RDWR)
        conn.shutdown(SHUT_RDWR)
        t.close()
        conn.close()
    except:
        return
p=s.socket(s.AF_INET,s.SOCK_STREAM)
p.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
port=1234
p.bind(('',port))
p.listen(256)
while True:
    conn,addr=p.accept()
    conn.settimeout(3)
    print(addr)
    try:
       # print(len(th.enumerate()))
        data=conn.recv(1024)
        if data.decode().split(' ')[0]=='CONNECT':
            t=th.Thread(target=rec,args=(conn,data.decode()))
            t.start()
        elif data.decode().split(' ')[0]=='GET':
            back=b'HTTP/1.1 302 Moved Temporarily\r\nLocation:'
            back+=data.decode().split(' ')[1].replace('http','https').encode()+b'\r\n\r\n'
            print(back)
            conn.send(back)
    except:
        pass
