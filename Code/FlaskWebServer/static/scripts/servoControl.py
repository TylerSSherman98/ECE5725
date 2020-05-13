#!/usr/bin/env python
#################################################
# Avisha Kumar (ak754) & Tyler Sherman (tss86)  #
# ECE 5725: Embedded OS                         #
# 04/23/2020                                    #
# Lab 5: Final Project                          #
#################################################
# start daemon = sudo pigpiod
# stop daemon  = sudo killall pigpiod
import os
import errno
import time
import pigpio # uses Broadcom Numbering system

# Named Pipe
FIFO = '/home/pi/FinalProject/FlaskWebServer/static/scripts/servoFifo'
try:
    os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

# Define Constants
servo_pan  = 19       # GPIO19
servo_tilt = 18       # GPIO18
loc_tilt   = 0        # location of servo_tilt in duty cycle
loc_pan    = 0        # location of servo_pan in duty cycle
freq       = 50       # Hz
right      = 75000  # 7.5%
up         = 75000  # 7.5%
center     = 90000  # 9.0%
left       = 105000 # 10.5%
down       = 105000 # 10.5%
step       = 500

#------------------SERVO FUNCTIONS------------------------#
def pan_left():
    global loc_pan
    if loc_pan <= left - step:
        loc_pan += step
        pi.hardware_PWM(servo_pan, freq, loc_pan)
        print('servo_pan location = '+str(loc_pan))
    else:
        print('ERROR: servo_pan already left')
    time.sleep(0.1)
def pan_right():
    global loc_pan
    if loc_pan >= right + step:
        loc_pan -= step
        pi.hardware_PWM(servo_pan, freq, loc_pan)
        print('servo_pan location = '+str(loc_pan))
    else:
        print('ERROR: servo_pan already right')
    time.sleep(0.1)
def tilt_up():
    global loc_tilt
    if loc_tilt >= up + step:
        loc_tilt -= step
        pi.hardware_PWM(servo_tilt, freq, loc_tilt)
        print('servo_tilt location  = '+str(loc_tilt))
    else:
        print('ERROR: servo_tilt already up')
    time.sleep(0.1)
def tilt_down():
    global loc_tilt
    if loc_tilt <= down - step:
        loc_tilt += step
        pi.hardware_PWM(servo_tilt, freq, loc_tilt)
        print('servo_tilt location  = '+str(loc_tilt))
    else:
        print('ERROR: servo_tilt already down')
    time.sleep(0.1)
def center_servos():
    global loc_pan
    global loc_tilt
    pi.hardware_PWM(servo_pan, freq, center)
    pi.hardware_PWM(servo_tilt,  freq, center)
    loc_pan = center
    loc_tilt = center
    print('centering servos')
#---------------------------------------------------------#

# Setup & initialize PWM
pi = pigpio.pi()
pi.hardware_PWM(servo_tilt, freq, center)
pi.hardware_PWM(servo_pan,  freq, center)
loc_tilt = center
loc_pan = center

# Normally, opening the FIFO blocks until the other end is opened also  
# This way, once the pipe is closed, the code will attempt to re-open it, which will block until another writer opens the pipe
running = True
while running:
    #print("Opening FIFO...")
    with open(FIFO) as fifo:
        #print("FIFO opened")
        while True:
            cmd = (fifo.read())[0:1]
            if cmd == 'u':
                tilt_up()
            elif cmd == 'l':
                pan_left()
            elif cmd == 'c':
                center_servos()
            elif cmd == 'r':
                pan_right()
            elif cmd == 'd':
                tilt_down()
            elif cmd == 'q':
                running = False
                break

            # closes FIFO to limit CPU usafe
            if len(cmd) == 0:
                #print("Writer closed")
                break
            #print('Read: "{0}"'.format(data))

# Stop & cleanup
pi.stop()

