#!/bin/bash
#################################################
# Avisha Kumar (ak754) & Tyler Sherman (tss86)  #
# ECE 5725: Embedded OS                         #
# 04/23/2020                                    #
# Lab 5: Final Project                          #
#################################################
# Use 'chmod +x launch.sh' to make executable

# Kill the Flask WebServer python3 process
kill $(ps aux | grep '[p]ython3 /home/pi/FinalProject/FlaskWebServer/website.py' | awk '{print $2}')
echo 'Flask WebServer shutdown'
    
    


