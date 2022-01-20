from arncore import Pane, ImageBox
import time
import cv2
import zmq
import base64
import numpy as np


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
	pane = Pane()

	message = socket.recv() # Wait for next request from client
	img = base64.b64decode(message)
	npimg = np.fromstring(img, dtype=np.uint8)
	frame = cv2.imdecode(npimg, 1)

	img_box = ImageBox(file=frame, position=(0,0), size=(62,10))
	pane.add_pane(img_box)
	pane.draw()
	pane.render()
	time.sleep(0.001)
	