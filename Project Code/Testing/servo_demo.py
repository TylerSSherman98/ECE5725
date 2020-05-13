#!/usr/bin/env python
#################################################
# Avisha Kumar (ak754) & Tyler Sherman (tss86)  #
# ECE 5725: Embedded OS                         #
# 04/17/2020                                    #
# Lab 5: Final Project                          #
#################################################
# start daemon = sudo pigpiod
# stop daemon  = sudo killall pigpiod
import pygame
from pygame.locals import *
import os
import time
import pigpio # uses Broadcom Numbering system

# Define Constants
servo_pan  = 19       # GPIO19
servo_tilt = 18       # GPIO18
loc_tilt   = 0        # location of servo_tilt in duty cycle
loc_pan    = 0        # location of servo_pan in duty cycle
freq       = 50       # Hz
right      = 75000.0  # 7.5%
up         = 75000.0  # 7.5%
center     = 90000.0  # 9.0%
left       = 105000.0 # 10.5%
down       = 105000.0 # 10.5%
step       = 500.0

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

# Setup dispay
pygame.init()
pygame.mouse.set_visible(True)
white   = 255,255,255
black   = 0,0,0
green   = 0,255,0
red     = 255,0,0
screen  = pygame.display.set_mode((320,500))
my_font = pygame.font.Font(None, 50)
buttons = {'Up':(160,70), 'Down':(160,310), 'Left':(100,190), 'Right':(220,190), 'Quit':(100,430), 'Center':(240,430)}
screen.fill(black)
pygame.draw.rect(screen, green,(110,  20, 100, 100))
pygame.draw.rect(screen, green,(50,  140, 100, 100))
pygame.draw.rect(screen, green,(170, 140, 100, 100))
pygame.draw.rect(screen, green,(110, 260, 100, 100))
pygame.draw.rect(screen, red,  (50,  380, 100, 100))
pygame.draw.rect(screen, red,  (170, 380, 140, 100)) 
for my_text, text_pos in buttons.items():
    text_surface = my_font.render(my_text, True, white)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)
pygame.display.flip()

# Setup timer
start_time = time.time()
length     = 1000 # seconds
running    = True

# Setup & initialize PWM
pi = pigpio.pi()
pi.hardware_PWM(servo_tilt, freq, center)
pi.hardware_PWM(servo_pan,  freq, center)
loc_tilt = center
loc_pan = center

while (time.time() < start_time + length) and (running == True):
    # Touch event location & button press functionality
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            
            if y>20 and y<120 and x>110 and x<210:
                tilt_up()
            elif y>140 and y<240 and x>50 and x<150:
                pan_left()
            elif y>140 and y<240 and x>170 and x<270:
                pan_right()
            elif y>260 and y<360 and x>110 and x<210:
                tilt_down()
            elif y>380 and y<480 and x>50 and x<150:
                running = False
                print('Goodbye!')
            elif y>380 and y<480 and x>170 and x<310:
                center_servos()
                
# Stop and cleanup
pi.stop()