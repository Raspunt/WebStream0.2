import threading
import time
import datetime
import os


import sounddevice as sd
from scipy.io.wavfile import write

import numpy as np


myrecording = np.array([])
recordDone = False

fs = 44100  # Sample rate
seconds = 10  # Duration of recording

def RecordMicro():

    try:
        global myrecording
        myrecording = sd.rec(int(seconds * fs),
            samplerate=fs,
            channels=1)

        sd.wait()  
        write('static/Sounds/VideoSound.wav', fs, myrecording)  

        global recordDone  
        recordDone = True
    
    except KeyboardInterrupt:
        write('static/Sounds/VideoSound.wav', fs, myrecording)  
        print("Record is done asshole!,syka!,blyat!")
        print("length this record is", str(datetime.timedelta(seconds=seconds)))
        






t1 = threading.Thread(target=RecordMicro, args=())
t1.start()


