#!/usr/bin/python
"""
data acquistion module for ur-senselab project
"""

import serial
import time
import glob
import json
import serial

class JSON:
	def __init__(self, data):
		self.data = data 
	def normalizer(self):
		try:
			data = json.loads(self.data)
		except Exception as err:
			raise(err)

class DataFetcher:

	def __init__():
		self.port = ArduinoSerialPort().get_serial()
		self.BaudRate = 9600

	def normalizeData(self):
		pass

	def GetData(self):
		try:
			ard = serial.Serial(self.port, BaudRate)
		except Exception as err:
			print err

def main():
	pass


if __name__ == '__main__':
	main()



