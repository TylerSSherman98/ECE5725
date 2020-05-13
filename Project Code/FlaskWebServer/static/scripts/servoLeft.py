#!/usr/bin/env python
#################################################
# Avisha Kumar (ak754) & Tyler Sherman (tss86)  #
# ECE 5725: Embedded OS                         #
# 04/23/2020                                    #
# Lab 5: Final Project                          #
#################################################
import subprocess

cmd = 'echo l > ~/FinalProject/FlaskWebServer/static/scripts/servoFifo'
print subprocess.check_output(cmd, shell=True)
