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
from time import strftime

"""@initialize"""

jsondata = None
ard = None
data = None
idle = 30 # set idle time here

try:
	import portdetect
	import database
except ImportError:
	print 'main module not loaded'

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
	db_info = config.conf
	db = database.dbsetup(db_info['hostname'], db_info['username']. db_info['password'], db_info['db'])

	"""@database operation"""
	db_obj = db.connect()

	"""@database cursor (i have no idea what's cursor is)"""
	cur = db_obj.cursor()

	print 'connected to database'
except Exception as err:
	print "[{}] {}".format(strftime("%Y-%m-%d %H-%M-%S"), err)


query = """INSERT INTO ardu_data(date,data1,data2) VALUES (NOW(), {}, {});"""

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

	"""@execute INSERT command to MySQL database"""
	try:
		cur.execute(query.format(data1, data2))
		"""@commit changes"""
		db.commit()
		print "[{}] succesfully insert data to database".format(strftime("%Y-%m-%d %H-%M-%S"))
	except Exception as err:
		print "[{}] unable to insert data to database: ".format(strftime("%Y-%m-%d %H-%M-%S"), err)

if __name__ == '__main__':
	print "[{}] intializing main() and idle for {} seconds".format(strftime("%Y-%m-%d %H-%M-%S"),idle)
	"""wait until the pigs fly"""
	while True:
		"""@call main function"""
		main()
		"""@sleep for 1 minutes"""
		time.sleep(idle)
