#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

try:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    AUDIO_FILE = sys.argv[3]
    
except IndexError:
    sys.exit("Usage: python3 server.py IP port audio_file")

TRYING = b"SIP/2.0 100 Trying\r\n\r\n"
RINGING = b"SIP/2.0 180 Ringing\r\n\r\n"
OK = b"SIP/2.0 200 OK\r\n\r\n"
BAD_REQUEST = b"SIP/2.0 400 Bad Request\r\n\r\n"
METHOD_NOT_ALLOWED = b"SIP/2.0 405 Method Not Allowed\r\n\r\n"
    
class EchoHandler(socketserver.DatagramRequestHandler):

    
    def handle(self):
        while 1:
            line = self.rfile.read()
            lista = ["INVITE", "ACK", "BYE"]
            lista_line_decode = line.decode("utf-8").split(" ")
            method = lista_line_decode[0]
            if not line:
                break
            if method == lista[0]:
                self.wfile.write(TRYING + RINGING + OK)
                print("El cliente nos manda " + line.decode('utf-8'))
            elif method == lista[1]:
                print("El cliente nos manda " + line.decode('utf-8'))
                aEjecutar = "mp32rtp -i 127.0.0.1 -p 23032 < " + AUDIO_FILE
                print("Vamos a ejecutar: " + aEjecutar)
                os.system(aEjecutar)
            elif method == lista[2]:
                self.wfile.write(OK)
                print("El cliente nos manda " + line.decode('utf-8'))
            elif method != lista:
                self.wfile.write(METHOD_NOT_ALLOWED)
            elif self.error(lista_line_decode):
                self.wfile.write(BAD_REQUEST)

if __name__ == "__main__":

    serv = socketserver.UDPServer(('', 6001), EchoHandler)
    print("Listening...")
    serv.serve_forever()
