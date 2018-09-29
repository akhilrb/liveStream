#!/usr/bin/env python

from functools import wraps
from importlib import import_module
import os
from flask import Flask, request, render_template, Response
from detection import *

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera_opencv import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
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

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/available.html')
# def waitOverhead():
#     return render_template("check_avail_wait.html")

def isAvailable():
    """get my status in room"""
    detectedPerson = detectPerson(0.3)
    print("Return code: " + str(detectedPerson))
    if(detectedPerson == -3):
        return Response(b'Sorry!. An admin user is in control of the stream. Please wait until the stream is released.')
    if(detectedPerson == -1):
        return Response(b'There was an error reading the room state!')
    n = detectedPerson.find(':')
    if(n == -1):
        return Response(b'Akhil is either not available right now, or he might be sleeping.')
    else:
        if(float(detectedPerson[n+1:detectedPerson.find('%')-1])>70):
            return Response(b'I\'m '+detectedPerson[n+1:detectedPerson.find('%')+1]+' sure that Akhil is available right now!')
        else:
            return Response(b'Akhil is available right now!')

@app.route('/stream.html')
@requires_auth
def stream():
    """Video streaming home page."""
    return render_template('stream.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
