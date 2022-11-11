import threading
from datetime import datetime
import time
import os

import cv2 as cv
from imutils.video import VideoStream,FPS
import imutils
import numpy as np
import glob

from sshSender import sshSender


class VideoCamera(object):

    cameraWorking = False
    RecordVideo = False

    countOfFrames = 0
    MoveDetect = False
    RecordRunning = False


    
    def start(self,file_type  = ".jpg", photo_string= "stream_photo"):
        
        if self.cameraWorking == False:
            # self.vs = WebcamVideoStream(src=2,resolution=(640, 480), framerate=self.fps).start()
            self.vs = VideoStream(src=0,framerate=10,resolution=(320, 240)).start()

            


            self.file_type = file_type
            self.photo_string = photo_string
            time.sleep(2.0)
            self.cameraWorking = True
     
        else:
            print('camera already working !!!')
            
        
    
    def stop(self):
        self.vs.stop()
        self.cameraWorking = False 

    def __del__(self):
        self.vs.stop() 
        self.cameraWorking = False 


    def get_frame(self):

        frame = self.vs.read()

        if self.RecordVideo == True:
            self.countOfFrames += 1
            cv.imwrite(f'VideoFrames/img{self.countOfFrames}.jpg',frame)


        ret, jpeg = cv.imencode(self.file_type, frame)

        return jpeg.tobytes()
    

    def generate_frames(self):


        while self.RecordVideo == True:

            frame = self.vs.read()

            self.countOfFrames += 1
            cv.imwrite(f'VideoFrames/img{self.countOfFrames}.jpg',frame)




    def StartRecordVideo(self):
        self.RecordVideo = True
      

    
   

    def StopRecordVideo(self):
        timer = 0
        while self.RecordVideo == True:
            timer += 1
            time.sleep(1)

            if timer == 10:
                self.RecordVideo = False
                self.countOfFrames = 0

                
                os.system('rm -rf video.mp4')
                os.system("ffmpeg -framerate 60 -i VideoFrames/img%d.jpg -c:v libx264 -r 30 video.mp4")

                sender = sshSender()
                lenfiles =  len(sender.ListFilesRemoteDir('/home/serv/share/CameraVideos/')) + 1
                os.system(f'mv video.mp4 VideoFrames/video{lenfiles}.mp4')

                for filename in os.listdir('VideoFrames/'):
                    if filename.endswith(".mp4"):
                        sender.Send(f'VideoFrames/{filename}','/home/serv/share/CameraVideos/')

                os.system('rm -rf VideoFrames/*')
                self.RecordRunning = False


    SaveImage = False
    def FindMontion(self):

        frame1 = self.vs.read() 
        frame2 = self.vs.read()

        if self.SaveImage == False:
            cv.imwrite('frame.jpg',frame2)
            self.SaveImage = True
        else:
            self.SaveImage = False
        
        frame2 = cv.imread('frame.jpg')


        diff = cv.absdiff(frame1, frame2) 

        diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY) 
        blur = cv.GaussianBlur(diff_gray, (5, 5), 0) 

        _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY) 
        dilated = cv.dilate(thresh, None, iterations=3) 

        contours, _ = cv.findContours( dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 

        
        for contour in contours:
            (x, y, w, h) = cv.boundingRect(contour)
            if cv.contourArea(contour) < 900:
                self.MoveDetect = False
                continue
            cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # cv.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv.FONT_HERSHEY_SIMPLEX,
            #             1, (255, 0, 0), 3)
            
            self.MoveDetect = True

        ret, jpeg = cv.imencode(self.file_type, frame1)
        # cv.imshow("output", frame1)

        if self.MoveDetect == True and self.RecordRunning == False:
            self.RecordRunning = True
            
            t = threading.Thread(target=self.StartRecordVideo, args=())
            t.start()

            t = threading.Thread(target=self.generate_frames, args=())
            t.start()

            t = threading.Thread(target=self.StopRecordVideo, args=())
            t.start()


        return jpeg.tobytes()


    def LoopFindMontion(self):

        while True:
            self.FindMontion()



