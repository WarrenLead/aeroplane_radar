# Fpvradar - Plane Radar - WL Version 2023
# run "cat /dev/serial0" to check gps is working
# run 'sudo gpsmon' or 'sudo cgps -s' to check gpsd is working (in terminal)
# run 'xgps' to check/view satellites (in terminal pups up in a gui)
# see also https://maker.pro/raspberry-pi/tutorial/how-to-use-a-gps-receiver-with-raspberry-pi-4
# also comment out whatever print statements you like

import requests
import geopy.distance
import time
import sys
from gps import *
from time import sleep
from gpiozero import Buzzer
from datetime import datetime
from guizero import App, Drawing, Text

#This code is released under the terms of the unlicense: https://unlicense.org/
#Author github.com/lexfp

# Disclaimer: This code is not pretty. It is written like a script since that is what it is. 
DUMP1090_URL = 'http://192.168.1.174/dump1090/data/aircraft.json'
UNKNOWN = 'Unknown'
LATITUDE = 'lat'
LONGTITUDE = 'lon'
BUZZER_PIN = 17
# seconds between each check
INTERVAL_SECONDS = 3
# set this to false if you don't want a long beep on initial gps lock
initialGPSLockBeep=True 
# I keep this value large so I know the app is running since it will always beep once.
# you can set the value lower to have a quieter system and a 3rd perimeter
OUTER_PERIMETER_ALARM_MILES = 5
# middle perimeter trigger sets of 2 beeps
MIDDLE_PERIMETER_ALARM_MILES = 2
# inner perimeter trigger sets of 3 beeps
INNER_PERIMETER_ALARM_MILES = 1
# upper limit of altitude at which you want to monitor aircraft
ALTITUDE_ALARM_FEET = 10000
running = True
gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
buzzer = Buzzer(BUZZER_PIN)
lastKnownLat=UNKNOWN
lastKnownLon=UNKNOWN
# the number of iterations we should try to reuse the last known position 
# set this to -1 if you plan on relocating the unit to a location with poor GPS 
# reception once initial position is established and you don't plan on moving around
# then it will never need the GPS coordinates again if they are not available
LAST_KNOWN_POSITION_REUSE_TIMES = 3
lastKnownPosReuse=0
failedGPSTries=0
    
#draw radar screen
aa = App()
d = Drawing(aa, width="500", height="500")
d.oval(0, 0, 500, 500, color="grey", outline=True, outline_color="black")
d.oval(50, 50, 450, 450, color="grey", outline=True, outline_color="black")
d.oval(100, 100, 400, 400, color="grey", outline=True, outline_color="black")
d.oval(150, 150, 350, 350, color="grey", outline=True, outline_color="black")
d.oval(200, 200, 300, 300, color="grey", outline=True, outline_color="black")
d.line(0, 250, 500, 250, color="red", width=1)
d.line(250, 0, 250, 500, color="red", width=1)
d.text(235, 1, "N 5", font="times new roman", size=14)
d.text(240, 480, "S", font="times new roman", size=14)
d.text(490, 240, "E", font="times new roman", size=14)
d.text(1, 240, "W", font="times new roman", size=14)
d.text(253, 51, "4", font="times new roman", size=14)
d.text(252, 101, "3", font="times new roman", size=14)
d.text(252, 151, "2", font="times new roman", size=14)
d.text(252, 201, "1", font="times new roman", size=14)
d.oval(245, 245, 255, 255, color="red", outline=True)#US
#d.text(160, 350, "Nothing at the moment", size=12)
last_id=16
aa.update()

def getPositionData(gps):
    nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    global lastKnownLat
    global lastKnownLon
    global lastKnownPosReuse
    if nx['class'] == 'TPV':
        lastKnownLat = getattr(nx, LATITUDE, UNKNOWN)
        lastKnownLon = getattr(nx, LONGTITUDE, UNKNOWN)
        lastKnownPosReuse=0 #reset counter since we refreshed coords
        #print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
        return (lastKnownLat, lastKnownLon)
    else:
        print ("Non TPV GPS class encountered: "+nx['class'])
        if LAST_KNOWN_POSITION_REUSE_TIMES < 0:
            return (lastKnownLat, lastKnownLon)
        elif lastKnownPosReuse < LAST_KNOWN_POSITION_REUSE_TIMES:
            lastKnownPosReuse += 1
            return (lastKnownLat, lastKnownLon)
        else:
            return(UNKNOWN,UNKNOWN)

def plotter(homecoords, planecoords, id):
    #Lat +/- .07 = 5 miles - Long +/- .086 = 5 miles @ -32
    a = (homecoords[0],homecoords[1]) #-32.78074, 152.08868 # Home
    b = (planecoords[0], planecoords[1]) #-32.77074, 152.09868 # Home
    ee = 3490
    e = 2919
    x = int(abs((a[1] - b[1]) * e - 250))
    y = int(abs((a[0] - b[0]) * ee + 250))
    #print (x, y)
    if id > 16:
        d.delete(id)
    id = d.oval(x-5, y-5, x+5, y+5, color="white", outline=True)#PLANE
    #print(id)
    aa.update()

def buzz(wait=0.1):
    buzzer.on()
    sleep(wait)
    buzzer.off()
    sleep(0.2)

def checkRadar():
    global failedGPSTries
    global gpsd
    global oldpos
    homecoords = getPositionData(gpsd)
    print ("Running... Time: " + str(datetime.now())[:-7] + " Home Coords: " + str(homecoords))
    if (homecoords[0] == UNKNOWN) or (homecoords[1] == UNKNOWN):
        #print "Cannot determine GPS position yet...try #"+str(failedGPSTries)
        #sleep(1)
        failedGPSTries += 1
        if failedGPSTries > 10:
            print ("Too many failed GPS tries, initializing new GPS object...")
            failedGPSTries = 0
            gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        return
    global initialGPSLockBeep
    if initialGPSLockBeep == True:
        initialGPSLockBeep=False
        buzz(1)
        sleep(5)
    r = requests.get(DUMP1090_URL)
    #print(r)
    try:
        airplanes = r.json()
        #print(airplanes)
    except:
        #print 'Error while getting airplane data'
        return
    outerAlarmTriggered = False
    middleAlarmTriggered = False
    innerAlarmTriggered = False
    for airplane in airplanes['aircraft']:
        #print(airplane)
        try:
            altitude = airplane['altitude']
            print('Alt: ' + str(altitude) + ' Flight: ' + airplane['flight'])
            planecoords = (airplane[LATITUDE], airplane[LONGTITUDE])
            #print(planecoords)
            distanceToPlane = geopy.distance.distance(homecoords, planecoords).miles
            #print("Dist:" + str(distanceToPlane))
            #print("- - - - - - - - - -")
            if isinstance(altitude, str):
                altitude = 0
            if altitude < ALTITUDE_ALARM_FEET:
                print ("Low flying < " + str(ALTITUDE_ALARM_FEET) + " feet detected... Dist: " + str(int(distanceToPlane)) + " " + str(planecoords))
                if distanceToPlane < INNER_PERIMETER_ALARM_MILES:
                    #print ('Inner alarm triggered by '+airplane['flight']+' at '+str(datetime.now())+' with distance '+str(distanceToPlane))
                    print ('Inner alarm triggered by '+airplane['flight']+' distance '+str(distanceToPlane) + str(planecoords))
                    plotter(homecoords, planecoords, id)
                    innerAlarmTriggered = True
                elif distanceToPlane < MIDDLE_PERIMETER_ALARM_MILES:
                    print ('Middle alarm triggered by '+airplane['flight']+' distance '+str(distanceToPlane) + str(planecoords))
                    plotter(homecoords, planecoords, id)
                    middleAlarmTriggered = True
                elif distanceToPlane < OUTER_PERIMETER_ALARM_MILES:
                    print ('Outer alarm triggered by '+airplane['flight']+' distance '+str(distanceToPlane) + str(planecoords))
                    plotter(homecoords, planecoords, id)
                    outerAlarmTriggered = True
                    
        except KeyError:
            pass
    if innerAlarmTriggered:
        print("Inner Alarm")
        buzz()
        buzz()
        buzz()
    elif middleAlarmTriggered:
        print("Middle Alarm")
        buzz()
        buzz()
    elif outerAlarmTriggered:
        print("Outer Alarm")
        buzz()



try:
    print ("Application started!")
    while running:
        checkRadar()
        sys.stdout.flush()
        time.sleep(INTERVAL_SECONDS)

except (ValueError):
    #sometimes we get errors parsing json
    pass

except (KeyboardInterrupt):
    running = False
    print ("Applications closed!")

#except:
 #   print ("Caught generic exception - continuing")
  #  sys.stdout.flush()
    #pass
