#################################################
# Avisha Kumar (ak754) & Tyler Sherman (tss86)  #
# ECE 5725: Embedded OS                         #
# 04/22/2020                                    #
# Lab 5: Final Project                          #
#################################################
from flask import Flask, render_template, request
from flask_basicauth import BasicAuth
import datetime
import RPi.GPIO as GPIO
import time
import os

app = Flask(__name__)

# Forces username:password login for all pages
app.config['SECRET_KEY'] = '2bbe2c121de7627518bd2e214cc82ff5'
app.config['BASIC_AUTH_USERNAME'] = 'pi'
app.config['BASIC_AUTH_PASSWORD'] = 'awesome20'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

# Use Broadcom Numbering system
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN)

# PIR needs 30-60 seconds to initialize
for i in range(1):
    time.sleep(1)
    print(i)

@app.route("/", methods=['GET', 'POST'])
def homepage():
   senPIRsts = GPIO.input(PIR_PIN)
   templateData = {
      'senPIR' : senPIRsts 
   }   
   
   # Respond to button presses
   if request.method == 'POST':
      if request.form['form'] == 'Shutdown':
           os.system('exec ~/FinalProject/FlaskWebServer/static/scripts/shutdown.sh')
      if request.form['form'] == 'left':
           os.system('python ~/FinalProject/FlaskWebServer/static/scripts/servoLeft.py')
      if request.form['form'] == 'right':
           os.system('python ~/FinalProject/FlaskWebServer/static/scripts/servoRight.py')
      if request.form['form'] == 'up':
           os.system('python ~/FinalProject/FlaskWebServer/static/scripts/servoUp.py')
      if request.form['form'] == 'down':
           os.system('python ~/FinalProject/FlaskWebServer/static/scripts/servoDown.py')
      if request.form['form'] == 'center':
           os.system('python ~/FinalProject/FlaskWebServer/static/scripts/servoCenter.py')
      return render_template('index.html', **templateData, scrollToAnchor='servo')
           
   return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8001, debug=False, threaded=True)
