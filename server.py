#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Main server

@author: jessica chambers
"""

import socket
import sys

# Create a TCP/IP socket
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock1.bind(server_address)

# Listen for incoming connections
sock1.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection1, client_address1 = sock1.accept()
    
    try:
        print >>sys.stderr, 'first connection from', client_address1

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection1.recv(64)
            print >>sys.stderr, 'received "%s"' % str(data)
            if not data:
                print >>sys.stderr, 'no more data from', client_address1
                break
    finally:
        # Clean up the connection
        connection1.close()