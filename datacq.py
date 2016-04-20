#!/usr/bin/python
"""
data acquistion module for ur-senselab project
"""

import serial
import time
import glob
import json
import serial
from time import strftime

try:
	import portdetect
	import database 
except ImportError:
	print 'main module not loaded'

class JSON:

	def __init__(self, data):
		self.data = data 
	def normalizer(self):
		try:
			data = json.loads(self.data)
		except Exception as err:
			raise(err)
		return data 

class DataFetcher:

	def __init__(self, port):
		self.BaudRate = 9600
		self.port = port

	def GetData(self):
		try:
			ard = serial.Serial(self.port, self.BaudRate)
		except Exception as err:
			print err
		try:
			data = ard.readline()
		except Exception as err_reading_data:
			print err_reading_data
		
		return data

"""
@database connection
"""

try:
	"""@database object"""
	db = database.dbsetup('localhost','root','anakamak','pi_data')
	
	"""@database operation"""
	db_obj = db.connect()
	
	"""@database cursor (i have no idea what's cursor is)""" 
	cur = db_obj.cursor()

	print 'connected to database'
except Exception as err:
	print "[{}] {}".format(strftime("%Y-%m-%d %H-%M-%S"), err)


query = """INSERT INTO ardu_data(`date`,`data1`,`data2`) VALUES (NOW(), {}, {});""" 
	
def main():

	"""@get open serial port to connect to arduino"""
	try:
		port = portdetect.ArduinoSerialPort().get_serial()
	except Exception:
		print "[{}] unable to connect to arduino".format(strftime("%Y-%m-%d %H-%M-%S")) 
		pass
	print "[{}] arduino detected on port {}".format(strftime("%Y-%m-%d %H-%M-%S"), port) 
	
	"""@fetch data from arduino"""
	data = DataFetcher(port).GetData()
	
	"""@normalize data to collection"""
	json_obj = JSON(data)
	normal_data = json_obj.normalizer()

	"""@normalize data"""
	data1 = normal_data[u'data1'][0]
	data2 = normal_data[u'data2'][0]
	print data1, data2
	print "[{}] {} - {}".format(strftime("%Y-%m-%d %H-%M-%S"), data1, data2)

	"""@execute INSERT command to MySQL database"""
	try:
		cur.execute(query.format(data1, data2))
		"""@commit changes"""
		db.commit()
		print "[{}] succesfully insert data to database".format(strftime("%Y-%m-%d %H-%M-%S")) 
	except Exception as err:
		print "[{}] unable to insert data to database: ".format(strftime("%Y-%m-%d %H-%M-%S"), err)
	
if __name__ == '__main__':
	"""@call main function"""
	main()
	"""@sleep for 1 minutes"""
	time.sleep(60)



