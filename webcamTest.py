import cv2
import zmq
import base64
import numpy as np

def teststuff(img):
	#img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#img_blur = cv2.GaussianBlur(img_grey, (3,3), SigmaX=0, SigmaY=0)

	#cv2.imshow("test2", img_grey)
	#cv2.imshow("test2", img_grey)

	#sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
	#sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
	#sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)

	#edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)

	scale = 1
	delta = 0
	ddepth = cv2.CV_16S

	img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img_blur = cv2.GaussianBlur(img_grey, (3,3), 0)

	grad_x = cv2.Sobel(img_blur, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
	grad_y = cv2.Sobel(img_blur, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)

	abs_grad_x = cv2.convertScaleAbs(grad_x)
	abs_grad_y = cv2.convertScaleAbs(grad_y)

	grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

	cv2.imshow('grad', grad)

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

def sendTest(frame):
	#IP = 'localhost'
	#context = zmq.Context()
	#footage_socket = context.socket(zmq.PAIR)
	#footage_socket.connect('tcp://%s:5555'%IP)
	#print(IP)
#
	#frame_image = cv2.resize(img, (640, 480))
	#encoded, buffer = cv2.imencode('.jpg', frame_image)
	#jpg_as_text = base64.b64encode(buffer)
#
	##footage_socket.send(jpg_as_text)
	#footage_socket.send_string("testing")
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://130.229.141.168:5555")
	print(type(frame))
	print(np.shape(frame))
	print(frame[200:210,0])
	#frame = cv2.resize(frame, (640, 480))
	_, buffer = cv2.imencode('.jpg', frame)
	message = base64.b64encode(buffer)
	print(type(message))
	socket.send(message)

	message = socket.recv()
	print("Received reply [ {} ]". format(message))

	socket.close()
	context.term()


while True:
	ret, frame = cam.read()
	if not ret:
		print("failed to grab frame")
		break
	cv2.imshow("test", frame)

	teststuff(frame)

	k = cv2.waitKey(1)
	if k%256 == 27:
		# ESC pressed
		print("Escape hit, closing...")
		break
	elif k%256 == 32:
		# SPACE pressed
		img_name = "opencv_frame_{}.png".format(img_counter)
		cv2.imwrite(img_name, frame)
		print("{} written!".format(img_name))
		img_counter += 1
		try:
			sendTest(frame)
		except Exception as e:
			print(e)
			print("dfdsaasd")

cam.release()

cv2.destroyAllWindows()