# aeroplane_radar
For use with Raspberry Pi, uses Dump1090 with SDR Dongle to alert you of approaching low flying aircraft. Useful for model plane flyers and FPV drone flyers to alert that there is full size aeroplane in the area. A sound beeps when a low flying aircaft approaches and it is displayed on a radar screen like guizero or OLED screen on Raspberry Pi if used in the field.

Loosly based on Lexfp's fvpradar https://github.com/lexfp/fpvradar for initial code ideas, this one is updated for Raspberry Pi Bullseye with Phython3 and newer libraires.

This is a work in progress. 

Currently I am developing using one Raspberry Pi which is running Dump1090 with a RadarBox Flightstick feeding ADS-B and MLAT data to RadarBox, FlightAware, FlightRadar24 & Plane Finder. I am using a 2nd Raspberry Pi with at GPS Module, buzzer and OLED screen to write the code and test.  I have been using guizero to test the radar screen out on the desktop. Eventually I plan to put it all on a Raspberry Pi Zero 2 W with a separate SDR dongle, GPS receiver module and small 128x64 OLED screen for field use. In the field you can usually hear them before you see them so the radar screen is just a bit of and extra feature to give you an idea of which way the plane is heading.
