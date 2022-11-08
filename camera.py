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


    





    def start(self,file_type  = ".jpg", photo_string= "stream_photo"):
        
        if self.cameraWorking == False:
            # self.vs = WebcamVideoStream(src=2,resolution=(640, 480), framerate=self.fps).start()
            self.vs = VideoStream(src=0,framerate=30).start()

            


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





    
        

    # def take_picture(self):
    #     frame = self.vs.read()
    #     ret, image = cv.imencode(self.file_type, frame)
    #     today_date = datetime.now().strftime("%m%d%Y-%H%M%S")
    #     cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)
