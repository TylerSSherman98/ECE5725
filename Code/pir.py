#!/usr/bin/env python
#################################################
# Avisha Kumar (ak754) & Tyler Sherman (tss86)  #
# ECE 5725: Embedded OS                         #
# 04/20/2020                                    #
# Lab 5: Final Project                          #
#################################################
import RPi.GPIO as GPIO
import time
import subprocess

# Use Broadcom Numbering system
GPIO.setmode(GPIO.BCM)

PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN)

# Define a threaded callback function to run in another thread when events are detected
def MOTION(PIR_PIN):
    if GPIO.input(PIR_PIN): # GPIO23 == high
        msg = 'echo 1 > /home/pi/FinalProject/FlaskWebServer/static/scripts/pir.txt'
        subprocess.check_output(msg, shell=True)
        email = 'mutt -e "set content_type="text/html"" tss86@cornell.edu -s "ALERT - Motion Detected!" < /home/pi/FinalProject/FlaskWebServer/static/scripts/text.html'
        subprocess.check_output(email, shell=True)
        #print("Motion detected!")
    else:                   # GPIO23 == low
        msg = 'echo 0 > /home/pi/FinalProject/FlaskWebServer/static/scripts/pir.txt'
        subprocess.check_output(msg, shell=True)
        #print("End of motion detection event")

# PIR needs 30-60 seconds to initialize
for i in range(30):
    time.sleep(1)
    print(i)

try:
    # When a change edge is detected on GPIO23, regardless of whatever else
    # is happening in the program, the function MOTION will be run
    GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, callback=MOTION)
    while 1:
        time.sleep(100)

except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
