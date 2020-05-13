#################################################
# Avisha Kumar (ak754) & Tyler Sherman (tss86)  #
# ECE 5725: Embedded OS                         #
# 04/09/2020                                    #
# Lab 5: Final Project                          #
#################################################
import RPi.GPIO as GPIO
import time
import subprocess

'''
Motion Library command line options
  -c : full path & filename of config file
  -h : show help screen
  -b : run in daemon mode
  -n : run in non-daemon mode
  -m : start in pause mode
'''
# Start motion in non-daemon mode
cmd = 'motion -n -c ~/FinalProject/Motion/motion.conf'
print subprocess.check_output(cmd, shell=True)