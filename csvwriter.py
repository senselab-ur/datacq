#!/usr/bin/python
"""
data acquistion module for ur-senselab project
@author: @vickydasta
@license: BSD
@senselab-ur
"""

import serial
import time
import glob
import json
import serial
import csv
import config
import sys
from time import strftime

"""@initialize"""

idle = 30 # set idle time here
try:
	import portdetect
except ImportError:
	print 'main module not loaded'
	sys.exit(0)

class JSON:
	def __init__(self, data):
		self.data = data
	def normalizer(self):
		jsondata = None
		try:
			jsondata = json.loads(self.data)
		except Exception as err:
			pass
		return jsondata

class DataFetcher:
	def __init__(self, port):
		self.BaudRate = 9600
		self.port = port

	def GetData(self):
		"""@bug"""
		data = None
		ard = None
		try:
			ard = serial.Serial(self.port, self.BaudRate)
		except Exception as err:
			print err
		try:
			data = ard.readline()
		except Exception:
			pass
		return data

def main():
	port = None
	data = None

	"""@get open serial port to connect to arduino"""
	try:
		port = portdetect.ArduinoSerialPort().get_serial()
	except Exception:
		print "[{}] unable to connect to arduino".format(strftime("%Y-%m-%d %H-%M-%S"))
	print "[{}] arduino detected on port {}".format(strftime("%Y-%m-%d %H-%M-%S"), port)

	"""@fetch data from arduino"""
	data = DataFetcher(port).GetData()

	"""@normalize data to collection"""
	json_obj = JSON(data)
	normal_data = json_obj.normalizer()
	if normal_data == None:
		print "[{}] unable to parse NoneType data".format(strftime("%Y-%m-%d %H-%M-%S"))
		pass

	"""@normalize data"""
	data1 = normal_data[u'data1'][0]
	data2 = normal_data[u'data2'][0]

	print "[{}] {} - {}".format(strftime("%Y-%m-%d %H-%M-%S"), data1, data2)
	print "[{}] updating data to csv file".format(strftime("%Y-%m-%d %H-%M-%S"))

	"""@write data to csv file"""
	try:
		csvfile = open('data.csv','a')
		csvobj = csv.writer(csvfile, delimiter=";")
		csvobj.writerow((strftime("%Y-%m-%d %H-%M-%S"), data1, data2))
	finally:
		csvfile.close()
	print "[{}] done saving data.".format(strftime("%Y-%m-%d %H-%M-%S"))

if __name__ == '__main__':
	print "[{}] intializing main() and idle for {} seconds".format(strftime("%Y-%m-%d %H-%M-%S"),idle)
	"""wait until the pigs fly"""
	while True:
		"""@call main function"""
		main()
		"""@sleep for 1 minutes"""
		time.sleep(idle)
