#!/usr/bin/env python

from functools import wraps
from importlib import import_module
import os
from flask import Flask, request, render_template, flash, Response
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from detection import *
import logging

logging.basicConfig(filename='liveStreamLog.log',level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_opencv import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d4183ef28cea'

@app.route('/')
def index():
    """Home page."""
    logging.info('HIT')
    return render_template('index.html')

@app.route('/available.html')
# def waitOverhead():
#     return render_template("check_avail_wait.html")

def isAvailable():
    #get my status in room
    detectedPerson = detectPerson(0.3)
    print("Return code: " + str(detectedPerson))
    if(detectedPerson == -3):
        logging.info('REQ_AVAIL \tNO_STREAM')
        return Response('Sorry!<br>An admin user is in control of the stream.<br>Please wait until the stream is released.')
    if(detectedPerson == -1):
        logging.info('REQ_AVAIL \tCORRUPT_STREAM')
        return Response(b'There was an error reading the room state!')
    if(detectedPerson.find('person:') == -1):
        logging.info('REQ_AVAIL \tNO')
        return Response(b'Akhil is either not available right now, or he might be sleeping.')
    else:
        n = detectedPerson.find(':')
        logging.info('REQ_AVAIL \tYES')
        if(float(detectedPerson[n+1:detectedPerson.find('%')-1])>90):
            return Response(b'I\'m '+detectedPerson[n+1:detectedPerson.find('%')+1]+' sure that Akhil is available in his room right now!')
        else:
            return Response(b'Akhil is available in his room right now!')

'''''
sendDM
'''''

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    message = TextField('Message:', validators=[validators.required(), validators.Length(min=1, max=45)])

    def reset(self):
        blankData = MultiDict([ ('csrf', self.reset_csrf() ) ])
        self.process(blankData)

@app.route('/sendDM.html', methods=['GET','POST'])
def sendDM():
    form = ReusableForm(request.form)
    print form.errors
    if request.method == 'POST':
        name=request.form['name']
        message=request.form['message']

        if form.validate():
            logging.info('REQ_DM |' + name + ': ' + message)
            flash('Your message has been sent!\nIf everything works perfectly, Akhil should receive a direct ping on his wearable device.')
        else:
            flash('Error: All the form fields are required.')
    return render_template('sendDM.html', form=form)

'''''
STREAM
'''''

def check_auth(username, password):
    return username == 'admin' and password == 'admin'

def authenticate():
    logging.warning('AUTH_INCORRECT')
    #Sends a 401 response that enables basic authorisation
    return Response(
    'Verification Failed.\n'
    'Check your credentials!', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/stream.html')
@requires_auth
def stream():
    """Video streaming home page."""
    logging.warning('AUTH_CORRECT')
    return render_template('stream.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Feeds the src attribute of the img tag
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
