import serial
import portdetect
import json

def main():
	try:
		ard = serial.Serial(portdetect.ArduinoSerialPort().get_serial(),9600)
	except:
		pass

	try:
		print json.loads(ard.readline())
	except:
		pass 
	return json.loads(ard.readline())

if __name__ == '__main__':
	main()
