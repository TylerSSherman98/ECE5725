#################################################
# Avisha Kumar (ak754) & Tyler Sherman (tss86)  #
# ECE 5725: Embedded OS                         #
# 04/22/2020                                    #
# Lab 5: Final Project                          #
#################################################
from flask import Flask, render_template, request, url_for, copy_current_request_context
from flask_basicauth import BasicAuth
from flask_socketio import SocketIO, emit
from time import sleep
from threading import Thread, Event
import os

app = Flask(__name__)

# Forces username:password login for all pages
app.config['SECRET_KEY'] = 'XXXXXXXXXXXXXX'  #redacted
app.config['DEBUG'] = False
app.config['BASIC_AUTH_USERNAME'] = 'XXXXX'  #redacted
app.config['BASIC_AUTH_PASSWORD'] = 'XXXXX'  #redacted
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

# Turn Flask app into a SocketIO app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

# Create thread for PIR sensor
thread = Thread()
thread_stop_event = Event()

# Function that asynchronously updates PIR status using named pipe
def pirSensor():
    # initial setup
    prevPirStatus = 0 
    setupCount = 0
    while not thread_stop_event.isSet():
         f = open("/home/pi/FinalProject/FlaskWebServer/static/scripts/pir.txt", "r")
         pirStatus = int(f.read()[0:1])
         f.close()
         # PIR detected motion --> changed to high
         if(prevPirStatus==0 and pirStatus==1):
             socketio.emit('pirStatus', {'pir': 'Detected'}, namespace='/pir')
             prevPirStatus = 1
         # PIR has no detected motion --> changed to low
         elif(prevPirStatus==1 and pirStatus==0 or pirStatus==0 and setupCount<=50):
             socketio.emit('pirStatus', {'pir': 'Clear'}, namespace='/pir')
             prevPirStatus = 0
             setupCount += 1
         socketio.sleep(1)

@app.route("/", methods=['GET', 'POST'])
def homepage():
   templateData = {
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

@socketio.on('connect', namespace='/pir')
def test_connect():
    # Need visibility of the global thread object
    global thread
    print('Client connected')
    #Start PIR sensor thread only if thread has not been started
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(pirSensor)

@socketio.on('disconnect', namespace='/pir')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8001, debug=False)
