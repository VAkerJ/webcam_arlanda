import os
import zmq
import base64
import cv2
#import numpy as np

def send_file(name='/img/webcamscreencap.png', source=None, destination=None):
	if not source:
		source = os.path.dirname(os.path.abspath(__file__))
	if not destination:
		destination = 'arlanda/new_arlanda/arlanda/skit/'

	password = ""
	ip = ""
	os.system('sshpass -p "{}" scp -r {} pi@{}:{}'.format(password, source+name, ip, destination))

def send_frame(frame, verbose=False):
	ip = ""
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://{}:5555".format(ip))

	_, buffer = cv2.imencode('.jpg', frame)
	message = base64.b64encode(buffer)

	socket.send(message)

	message = socket.recv()
	if verbose:
		print("Received reply [ {} ]".format(message))

	socket.close()
	context.term()