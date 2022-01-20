#client.py
import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)
ip = ""
socket.connect("tcp://{}:5555".format(ip))
for request in range(10):
 
	print("Sending request {} …".format(request))
	socket.send(b"Hello")
	message = socket.recv()
	print("Received reply {} [ {} ]". format(request, message))
socket.close()
context.term()