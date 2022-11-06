import os
import time
import threading

from gpiozero import CPUTemperature
from flask import Flask, render_template, Response, request,redirect
from dotenv import load_dotenv
import cv2 as cv

from motors import MotorMood
from camera import VideoCamera


load_dotenv()

mm = MotorMood()
pi_camera = VideoCamera() 
app = Flask(__name__,static_url_path='/static')

pi_camera.start()

os.system("rm -rf VideoFrames/*")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/motor_command',methods = ['POST'])
def motorCommand():
    
    motorSig = request.form.get('mc')
    speed = 0.3


    if motorSig == "V":
        mm.motorV()
        time.sleep(speed)
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
        time.sleep(speed)
        mm.motorS()




    return "1"


def gen(camera):
    # camera.start()


    while True:


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



@app.route('/temp')
def getTemp():
    cpu = CPUTemperature()
    return Response(str(cpu.temperature), status=200, mimetype='application/json')


@app.route('/StartRecord')
def StartRecord():
    

    t1 = threading.Thread(target=pi_camera.StartRecordVideo, args=())
    t1.start()

    t2 = threading.Thread(target=pi_camera.StopRecordVideo, args=())
    t2.start()
    
    return Response("Record is done",status=200)



    



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
