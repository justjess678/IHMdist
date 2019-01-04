#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Get City's Weather Info

Agent agregateur #1

@author: jessica chambers
"""

# Python program to find current 
# weather details of several cities
# using openweathermap api 

# import required modules 
import requests, json, string, datetime, time, sys, socket

def get_stats_city(api_key,city_name):
    
    #set up log file
    log = open("cities_weather.log","a+")
    out = str(datetime.datetime.now())
    out = out  + "\n"    
    log.write(out)
      
    # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
      
    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
      
    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 
      
    # json method of response object  
    # convert json format data into 
    # python format data 
    x = response.json() 
      
    # Now x contains list of nested dictionaries 
    # Check the value of "cod" key is equal to 
    # "404", means city is found otherwise, 
    # city is not found 
    if x["cod"] != "404": 
      
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
      
        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = y["temp"] - 273.15
      
        # store the value corresponding 
        # to the "pressure" key of y 
        current_pressure = y["pressure"] 
      
        # store the value corresponding 
        # to the "humidity" key of y 
        current_humidity = y["humidity"] 
        
        res = {'temp':y["temp"]- 273.15,'pressure':y["pressure"], 'humidity':y["humidity"]}
        # store the value of "weather" 
        # key in variable z 
        z = x["weather"] 
      
        # store the value corresponding  
        # to the "description" key at  
        # the 0th index of z 
        weather_description = z[0]["description"] 
      
        # print following values 
        out = city_name.upper() + "\n Temperature (in Celsius) = " + \
                        str(current_temperature) + \
              "\n atmospheric pressure (in hPa unit) = " + \
                        str(current_pressure) + \
              "\n humidity (in percentage) = " + str(current_humidity) + "\n"
        log.write(out)
        log.close()
        return res
      
    else: 
        out = "\n City Not Found "
        log.write(out)
        log.close()
            
#main
    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)

while(True):
    
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    
    #Toulouse weather info
    le_havre_info = get_stats_city("236dc0356af0cfcbe13dcf8cba1629e5","le havre")
    #Bordeaux weather info
    bordeaux_info = get_stats_city("ddb93c9878aa673d01095952d2761353","bordeaux")
    #Paris weather info
    marseille_info = get_stats_city("e418c8436cdee1933bcc58c81786747f","marseille")
    try:
        # Send data
        message = [marseille_info, bordeaux_info, le_havre_info]
        print >>sys.stderr, 'sending data to server'
        sock.sendall(str(message))
    
    finally:
        # Clean up the connection
        print >>sys.stderr, 'closing socket'
        sock.close()
        sock = socket.socket()
        
    #wait one minute
    time.sleep(60)