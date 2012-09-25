import threading
import serial

class SerialThread (threading.Thread):
	def __init__(self,lock):
		threading.Thread.__init__(self)
		self.lock=lock
		self.running = True
		self.current_rpm=0
		
	def __exit__(self):
		self.stop()
		
	def getBikeRpm(self):
		self.lock.acquire()
		rval = self.current_rpm
		self.lock.release()
		return rval
		
	def stop (self):
		self.running = False
		
	def run (self):
		ser = serial.Serial('/dev/tty.usbmodem12341', 9600)
		while self.running:
			value = ser.readline()
			v = value.decode("utf-8").rstrip('\r\n')
			if "R" in v:
				self.lock.acquire()
				self.current_rpm = v.strip("R")
				self.lock.release()