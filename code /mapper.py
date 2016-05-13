#!/usr/bin/python

import sys
import os
from datetime import datetime



def RepresentsFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def get_key(line):
	pickup_location = str(line[-2])
	drop_location  = str(line[-1])
	pickup_time = line[1]
	if len(pickup_time)>6:
		pickup_time = pickup_time[:-6].replace('-', ' ')
		pickup_time = pickup_time.split(' ')
		pickup_time = ','.join(pickup_time)
	key = ','.join([pickup_location, drop_location,pickup_time])
	return key

def get_value(line):
	### get passenger count 
	passenger_count = line[3]
	if not RepresentsFloat(passenger_count):
		passenger_count = 0.
	else:
		passenger_count = float(passenger_count)

	### get trip distance
	trip_distance = line[4]
	if not RepresentsFloat(trip_distance):
		trip_distance = 0.
	else:
		trip_distance = float(trip_distance)

	### get fare amount
	fare_amount = line[12]
	if not RepresentsFloat(fare_amount):
		fare_amount = 0.
	else:
		fare_amount = float(fare_amount)

	### get surcharge
	surcharge = line[13]
	if not RepresentsFloat(surcharge):
		surcharge = 0.
	else:
		surcharge = float(surcharge)

	### get tip amount
	tip_amount = line[15]
	if not RepresentsFloat(tip_amount):
		tip_amount = 0.
	else:
		tip_amount = float(tip_amount)

	### get tolls amount
	tolls_amount = line[16]
	if not RepresentsFloat(tolls_amount):
		tolls_amount = 0.
	else:
		tolls_amount = float(tolls_amount)

	### get total amount
	total_amount = line[-3]
	if not RepresentsFloat(total_amount):
		total_amount = 0.
	else:
		total_amount = float(total_amount)

	return [passenger_count, trip_distance, fare_amount, surcharge, tip_amount, tolls_amount, total_amount]

n = 0
time = datetime.now()
os.system('echo ' + str(time)+ ' : '+str(n) + ' >> ./mapper_logger.txt')


for line in sys.stdin:
	n+=1
	l = line.strip().split(',')
	if len(l[0]) >3 :
		continue		
	else:
		key = get_key(l)
		if n%10000000 == 0:
			time_diff = datetime.now() - time
			time = datetime.now()			
			os.system('echo ' + str(time_diff)+ ' '+ ','.join(key) + ' : '+str(n) + ' >> ./mapper_logger.txt ')		  		
		value = get_value(l)
		value_string = ''
		for v in value:
			a = '%.2f,'%(v)
			value_string = value_string+a

		value_string = value_string[:-2]
		print '%s\t%s'%(key, value_string)




