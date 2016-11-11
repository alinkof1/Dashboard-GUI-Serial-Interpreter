#!/usr/bin/env python

# serial_invert.py
# 2016-03-18
# Public Domain
#
# :SMax   0A,`
# :SRPM    0 , 
# :SCtmp 23C ,-
# :SMtmp 496C ,9

import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html
import re #for text parsing

while(1):

	RXD=15

	pi = pigpio.pi()

	if not pi.connected:
	   exit(0)

	pigpio.exceptions = False # Ignore error if already set as bit bang read.

	pi.bb_serial_read_open(RXD, 9600) # Set baud rate here.

	pigpio.exceptions = True

	pi.bb_serial_invert(RXD, 1) # Invert line logic.

	stop = time.time() + 3.0

	while time.time() < stop:

	   (count, data) = pi.bb_serial_read(RXD)
	   if count:
		  with open("outputRead.txt", "a") as text_file:
				text_file.write("%s\n" % data)
				print(data)

	   time.sleep(0.2)

	pi.bb_serial_read_close(RXD)

	pi.stop()


	#parsing code
	with open("outputRead.txt", "r") as text:
			read_data = text.read()
	result = re.findall(r':S(.*?),', read_data)
	#print result

	currentMax = 0
	RPM = 0
	Ctmp = 0
	Mtmp = 0
	Code = 0
	Vlt = 0
	Min = 0
	Amps = 0
	iteration = 0

	for i,w in enumerate(result):
		if(re.findall(r'Max((\s+)*)', w)):  
			currentMax = re.sub(r'[^\d+((\.\d+)*)]', '', w)	#decimals? 
		if(re.findall(r'Amps((\s+)*)', w)):
			Amps = re.sub(r'[^\d+((\.\d+)*)]', '', w)		#decimals?
		if(re.findall(r'RPM((\s+)*)', w)):
			RPM = re.sub(r'[^\d+((\.\d+)*)]', '', w)		
		if(re.findall(r'Ctmp((\s+)*)', w)):
			Ctmp = re.sub(r'[^\d+((\.\d+)*)]', '', w)#re.sub(r'\D', '', w)			#decimals?
		if(re.findall(r'Mtmp((\s+)*)', w)):
			Mtmp = re.sub(r'[^\d+((\.\d+)*)]', '', w)		#decimals?
		if(re.findall(r'Code((\s+)*)', w)):
			Code = re.sub(r'\D', '', w)
		if(re.findall(r'Vlt((\s+)*)', w)):  		#decimals?
			Vlt = re.sub(r'[^\d+((\.\d+)*)]', '', w)
		if(re.findall(r'Min\s+', w)):
			Min = re.sub(r'[^\d+((\.\d+)*)]', '', w)
		iteration +=1			
	with open("log.txt", "w") as text:
		text.write("%d) Current Max: %s, Amps: %s, RPM: %s, Ctmp: %s, Mtmp: %s, Vlt: %s, Min: %s, Code: %s\n" %(iteration, currentMax, Amps, RPM, Ctmp, Mtmp, Vlt, Min, Code))
