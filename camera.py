import threading
from datetime import datetime
import time
import os

import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import numpy as np
import glob

class VideoCamera(object):

    cameraWorking = False
    RecordVideo = False
    countOfFrames = 0

    fps = 30

    





    def start(self,file_type  = ".jpg", photo_string= "stream_photo"):
        
        if self.cameraWorking == False:
            self.vs = PiVideoStream(resolution=(640, 480), framerate=self.fps).start()
            # self.vs = PiVideoStream().start()
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
        self.previous_frame = jpeg

        return jpeg.tobytes()
    

    def StartRecordVideo(self):
        self.RecordVideo = True
      

    
   

        


    def StopRecordVideo(self):
        timer = 0
        while self.RecordVideo == True:
            timer += 1
            time.sleep(1)

            if timer == 10:
                self.RecordVideo = False
                os.system('rm -rf video.mp4')
                os.system("ffmpeg -framerate 10 -i VideoFrames/img%d.jpg -c:v libx264 -r 30 video.mp4")
                os.system('rm -rf VideoFrame/*')
                os.system('mv video.mp4 VideoFrames/')
                




    
        

    # def take_picture(self):
    #     frame = self.vs.read()
    #     ret, image = cv.imencode(self.file_type, frame)
    #     today_date = datetime.now().strftime("%m%d%Y-%H%M%S")
    #     cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)
