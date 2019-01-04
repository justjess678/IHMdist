#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
French cities tide times

Agent agregateur #2

@author: jess
"""
import requests, datetime, sys, socket, time

def get_city_tide(coords):
    
    #set up log file
    log = open("cities_tides.log","a+")
    out = str(datetime.datetime.now())
    out = out  + "\n"    
    log.write(out)

    api_key = "8e83d75b-4891-4757-8de4-3526f7ff4608"
    # base_url variable to store url 
    base_url = "https://www.worldtides.info/api?"
    now_epoch = int(datetime.datetime.now().strftime("%s"))
    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "heightS&key=" + api_key + coords + "&start=" + str(now_epoch)
    response = requests.get(complete_url) 
    x = response.json()
    if x["status"] != "404":
        res = {'height':x["heights"][0]["height"]}
        out = x["station"].upper() + "\n Height = " + \
                        str(x["heights"][0]["height"]) + "\n"
        log.write(out)
        log.close()
        return res
    else:
        out = "\n City Not Found "
        log.write(out)
        log.close()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)

print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

while(True):
    
    marseille_coords="&lat=43.299999&lon=5.366700"
    marseille_height = get_city_tide(marseille_coords)
    
    bordeaux_coords="&lat=44.667&lon=-1.167"
    bordeaux_height = get_city_tide(bordeaux_coords)
    
    le_havre_coords="&lat=49.483299&lon=0.116700"
    le_havre_height = get_city_tide(le_havre_coords)
    
    try:
        # Send data
        message = [marseille_height, bordeaux_height, le_havre_height]
        print >>sys.stderr, 'sending data to server'
        sock.sendall(str(message))
    
    finally:
        # Clean up the connection
        print >>sys.stderr, 'closing socket'
        sock.close()
        sock = socket.socket()
        
    #wait one minute
    time.sleep(60)