#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Main server

@author: jessica chambers
"""

import socket, sys

TIMEOUT = 3

def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    return value[adjusted_pos_a:pos_b]

def get_weather(my_string):
    pressure, temperature, humidity=[0,0,0],[0,0,0],[0,0,0]
    #my_string="{'pressure': 1037, 'temp': -0.23999999999995225, 'humidity': 80}, {'pressure': 1037, 'temp': -0.20999999999997954, 'humidity': 80}, {'pressure': 1040, 'temp': 4.32000000000005, 'humidity': 86}"
    i=0
    while i < 3:
        p=my_string.split('{')[i+1]
        pressure[i]=int(between(p, "'pressure': ",", 'temp': "))
        temperature[i]=round(float(between(p, ", 'temp': ",", 'humidity': ")),2)
        humidity[i]=int(between(p, ", 'humidity': ","}"))
        i=i+1
    return [pressure, temperature, humidity]

def get_height(my_string):
    height=[0,0,0]
    i=0
    while i < 3:
        p=my_string.split('{')[i+1]
        height[i]=between(p, "'height': ","}")
        i=i+1
    return height

def get_max_city(data):
    val=-1000
    city = -1
    i=0
    while i < len(data):
        if data[i] > val:
            val = data[i]
            city = i
        i=i+1
    if city > -1:
        if city==0:
            return 'Bordeaux has the highest '
        if city==1:
            return 'Le Havre has the highest '
        if city==2:
            return 'Marseille has the highest '
    else:
        return 'Error comparing cities'

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
    connection1.settimeout(TIMEOUT)
    
    try:
        print >>sys.stderr, 'first connection from', client_address1
        data=""

        # Receive the data in small chunks and retransmit it
        while True:
            data = data + str(connection1.recv(64))
            print >>sys.stderr, 'received data'
            
            if data.count("humidity")>=3:
                [pressure, temperature, humidity]=get_weather(data)
                #do stuff to the values
                avg_pressure=round(sum(pressure) / float(len(pressure)),2)
                print("Average air pressure = ",avg_pressure)
                avg_temperature=round(sum(temperature) / float(len(temperature)),2)
                print("Average temperature = ",avg_temperature)
                avg_humidity=round(sum(humidity) / float(len(humidity)),2)
                print("Average humidity = ",avg_humidity,"%")           
                data=""
            if data.count("height")>=3:
                tides = get_height(data)
                print(tides)
                print(get_max_city(tides), 'tide')
                data = ""
            if not data:
                print >>sys.stderr, 'no more data from', client_address1
                data=""
                break
    except socket.timeout:
        print >>sys.stderr, 'timeout on connection from', client_address1
    finally:
        # Clean up the connection
        connection1.close()