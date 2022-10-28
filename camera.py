import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np

class VideoCamera(object):

    cameraWorking = False

    def start(self,file_type  = ".jpg", photo_string= "stream_photo"):
        
        if self.cameraWorking == False:
            self.vs = PiVideoStream(resolution=(320, 240), framerate=10).start()
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

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):

        frame = self.vs.read()
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = jpeg
        return jpeg.tobytes()


    # def take_picture(self):
    #     frame = self.vs.read()
    #     ret, image = cv.imencode(self.file_type, frame)
    #     today_date = datetime.now().strftime("%m%d%Y-%H%M%S")
    #     cv.imwrite(str(self.photo_string + "_" + today_date + self.file_type), frame)
