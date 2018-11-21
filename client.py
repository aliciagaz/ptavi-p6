#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

try:
    METHOD = sys.argv[1]
    RECEIVER = sys.argv[2][:sys.argv[2].find("@")]
    IP = sys.argv[2][sys.argv[2].find("@")+1: sys.argv[2].rfind(":")]
    PORT = int(sys.argv[2][sys.argv[2].rfind(":")+1:])
    LINE = (METHOD + " sip:" + RECEIVER + "@" + IP + " SIP/2.0\r\n")
    
except IndexError:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP, PORT))

    print("Enviando: " + LINE)
    if METHOD == "INVITE" or METHOD == "BYE":
        my_socket.send(bytes(METHOD + " sip:" + RECEIVER + " SIP/2.0\r\n" , 'utf-8') +
                       b'\r\n')
    data = my_socket.recv(1024)

    print('Recibido -- ', data.decode('utf-8'))
    RECIVE = data.decode('utf-8').split(" ")
    for element in RECIVE:
        if element == "200" and METHOD != "BYE":
            my_socket.send(bytes("ACK sip:" + RECEIVER.split(":")[0] + 
                                 " SIP/2.0\r\n", 'utf-8') + b'\r\n')

    print("Terminando socket...")

print("Fin.")