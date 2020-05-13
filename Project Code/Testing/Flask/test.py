# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import RPi.GPIO as GPIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

# Use Broadcom Numbering system
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN)

# PIR needs 30-60 seconds to initialize
for i in range(1):
    socketio.sleep(1)
    print(i)

# def randomNumberGenerator():
#     """
#     Generate a random number every 1 second and emit to a socketio instance (broadcast)
#     Ideally to be run in a separate thread?
#     """
#     #infinite loop of magical random numbers
#     print("Making random numbers")
#     while not thread_stop_event.isSet():
#         number = round(random()*100, 3)
#         print(number)
#         socketio.emit('newnumber', {'number': number}, namespace='/test')
#         socketio.sleep(1)
def pirMotionSensor():
    print("Polling motion sensor")
    while not thread_stop_event.isSet():
         pir = GPIO.input(PIR_PIN)
         if(pir==1):
             socketio.emit('motion', {'pir': 'Motion detected'}, namespace='/pir')
             socketio.sleep(1)
         else:
             socketio.emit('motion', {'pir': 'No motion detected'}, namespace='/pir')
             socketio.sleep(1)

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index2.html')

@socketio.on('connect', namespace='/pir')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(pirMotionSensor)

@socketio.on('disconnect', namespace='/pir')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8089, debug=False)