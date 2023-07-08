# Aeroplane Radar
For use with Raspberry Pi, uses Dump1090 with SDR Dongle to alert you of approaching low flying aircraft. Useful for model plane flyers and FPV drone flyers to alert that there is full size aeroplane in the area. A sound beeps when a low flying aircaft approaches and it is displayed on a radar screen like guizero or OLED screen on Raspberry Pi if used in the field.

Loosly based on Lexfp's fvpradar https://github.com/lexfp/fpvradar (beeper) for initial code ideas, this one is updated for Raspberry Pi Bullseye with Phython3 and newer libraires.

This is a work in progress. 

Currently I am developing using one Raspberry Pi which is running Dump1090 with a RadarBox Flightstick feeding ADS-B and MLAT data to RadarBox, FlightAware, FlightRadar24 & Plane Finder. I am using a 2nd Raspberry Pi with at GPS Module, buzzer and OLED screen to write the code and test.  I have been using guizero to test the radar screen out on the desktop. Eventually I plan to put it all on a Raspberry Pi Zero 2 W with a separate SDR dongle, GPS receiver module and small 128x64 OLED screen for field use. In the field you can usually hear them before you see them so the radar screen is just a bit of and extra feature to give you an idea of which way the plane is heading.

# Required components:

1) Raspberry pi - 4B or Zero 2
2) GPS module - Neo 6M (https://maker.pro/raspberry-pi/tutorial/how-to-use-a-gps-receiver-with-raspberry-pi-4)
3) Buzzer - https://www.circuitbasics.com/how-to-use-buzzers-with-raspberry-pi/
4) SDR Dongle (e.g. radarbox, flightaware, rtl-sdr) I am using RadarBox Flightstick at the moment for testing
5) micro usb to USB adapter or HUB (if using pi zero since it doesn't have full size usb ports) 
6) 5v voltage regulator for external battery power
7) Antenna 
8) Case

# Installation

1) Setup Rasberry Pi
2) Install Piaware see https://flightaware.com/adsb/piaware/build or  Dump1090 see http://www.satsignal.eu/raspberry-pi/dump1090.html 
I am using this one because I already installed it before https://forum.flightradar24.com/forum/radar-forums/flightradar24-feeding-data-to-flightradar24/9949-how-to-install-dump1090-mutability-on-rpi 
You do need to set up the feeder to Flightaware or FR24 we only want Dump1090 for our own use.
3) Setup the GPS and Buzzer ans per instructions above
4) Install the following libraries
  sudo apt-get update  
  sudo apt-get install python-requests  
  sudo apt install python-gpiozero  
  sudo apt install python-geopy
  sudo pip3 install guizero 
  sudo apt install git
6) Clone this repo into the home directory,  aerplane_radar.py
7) edit setup options as required, eg. GPIO for buzzer etc.

more to come... 
