#!/bin/bash
#################################################
# Avisha Kumar (ak754) & Tyler Sherman (tss86)  #
# ECE 5725: Embedded OS                         #
# 04/22/2020                                    #
# Lab 5: Final Project                          #
#################################################
# Use 'chmod +x launch.sh' to make executable

# Start PiGPIO daemon
# Daemon must be running for library to work
if pgrep pigpiod
then
    echo 'PiGPIO daemon running'
else
    sudo pigpiod
fi

# Launch rapid camera network stream
# Use absolute path
python3 ~/FinalProject/webStream.py &

# Launch PIR sensor
# Use absolute path
python3 ~/FinalProject/pir.py &

# Launch servo controller
# Use absolute path
python3 ~/FinalProject/FlaskWebServer/static/scripts/servoControl.py &

# Launch Motion program
# -c : full path & filename of config file
# -b : run in daemon mode
motion -b -c ~/FinalProject/Motion/motion.conf &

# Launch Flask WebServer
# Use absolute path
python3 ~/FinalProject/FlaskWebServer/website.py

#---------TERMINATION & CLEANUP---------#
# Kill the Motion program
if pgrep motion
then
    sudo service motion stop
    echo 'Motion program killed'
else
    echo 'Motion program not running'
fi
# Kill the python processes
if pgrep python
then
    killall python3
    killall python
    echo 'Python processes killed'
else
    echo 'Python not running'
fi
# Kill the PiGPIO daemon
if pgrep pigpiod
then
    sudo killall pigpiod
    echo 'PiGPIO daemon killed'
else
    echo 'PiGPIO daemon not running'
fi
    
    


