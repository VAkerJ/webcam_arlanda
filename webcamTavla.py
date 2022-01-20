import cv2
import threading

from screencap import ScreenCapure
from sendToTavla import send_frame
from parameterTerminal import Input_Terminal

import numpy as np
#import logging
  

def camCycle(cam):
    cam.update()
    #cam.save_latest()

    frame = cam.get_frame()
    
    send_frame(frame)

def runUntillKey(n, onExit=lambda:None, whileRunning=lambda:None):
    if type(n) is int: n = [n]

    while True:
        k = cv2.waitKey(1)
        if k%256 in n:
            onExit()
            break

        whileRunning()

def closeProgram(cam):
    #term.kill()
    #x.put() # lär dig threading ordentligt bara
    cam.kill()
    
def test(get, sett):
    terminal = Input_Terminal()
    terminal.main(get, sett)



if __name__=='__main__':
    webcam = ScreenCapure()
    
    
    print("Press space to start")
    runUntillKey(32)

    x = threading.Thread(target=lambda:test(webcam.get_parameters, webcam.set_parameters))
    x.start()

    runUntillKey(27, lambda:closeProgram(webcam), lambda:camCycle(webcam))