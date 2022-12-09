import os
import time
import threading

from flask import Flask, render_template, Response, request,redirect
import cv2 as cv

from motors import MotorMood
from camera import VideoCamera
# from MicRecorder import MicRecorder


mm = MotorMood()
pi_camera = VideoCamera() 
app = Flask(__name__,static_url_path='/static')


# t = threading.Thread(target=pi_camera.LoopFindMontion, args=())
# t.start()
# pi_camera.start()


MontionDetection = False

os.system("rm -rf VideoFrames/*")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route('/')
def index():



    return render_template('index.html',resolution=pi_camera.resolution) 




def gen(camera):
    camera.start()


    while True:

        if MontionDetection == True:
            frame = camera.FindMontion()
        else:
            frame = camera.get_frame()

   
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stopCamera',methods = ['POST'])
def stopCamera():
    pi_camera.stop()
    return "None"




@app.route('/LoginUser',methods = ['POST'])
def LoginUser():


    usernameForm = request.form.get('username')
    passwordForm = request.form.get('password')

    usernameDEnv = os.environ.get('Username')
    passwordDEnv = os.environ.get('Password')


    print(passwordForm==passwordDEnv and usernameForm==usernameDEnv)

    if passwordForm==passwordDEnv and usernameForm==usernameDEnv :
        return Response("correct",status=200, mimetype='application/json')
    else:
        return Response("no",status=200, mimetype='application/json')




@app.route('/StartRecord',methods = ['POST'])
def StartRecord():

    
    t = threading.Thread(target=pi_camera.StartRecordVideo, args=())
    t.start()

    t = threading.Thread(target=pi_camera.generate_frames, args=())
    t.start()

    t = threading.Thread(target=pi_camera.StopRecordVideo, args=())
    t.start()

    return Response("Record start",status=200)



@app.route('/EnableMontionDetection',methods = ['POST'])
def EnableMontionDetection():

    global MontionDetection
    MontionDetection = True

    return Response("Montion detection is turned on",status=200)


@app.route('/DisableMontionDetection',methods = ['POST'])
def DisableMontionDetection():

    global MontionDetection
    MontionDetection = False

    return  Response("Montion detection is turned off",status=200)


# @app.route('/audio')
# def AudioLink():
#     mic = MicRecorder()

#     sound = mic.GetAudioStream()

#     # mic.getAllAudioDevice()
    
#     return Response(sound)


@app.route("/config")
def ConfigPage():

    return render_template('configPage.html')


@app.route("/ApplyConfig" ,methods=['POST'])
def ApplyConfig():


    rez = request.form.get('rez')

    pi_camera.setCameraResolution(rez)

    # pi_camera.stop()
    # pi_camera.start()

    return Response("oh ok...")


@app.route('/motor_command',methods = ['POST'])
def motorCommand():
    
    motorSig = request.form.get('mc')


    if motorSig == "V":
        mm.motorV()
        time.sleep(0.3)
        mm.motorS()
    
    elif motorSig == "R":
        mm.motorR()
        time.sleep(0.1)
        mm.motorS()

    elif motorSig == "L":
        mm.motorL()
        time.sleep(0.1)
        mm.motorS()

    elif motorSig == "NAZ":
        mm.motorNAZ()
        time.sleep(0.3)
        mm.motorS()

    return "1"




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
