#!/usr/bin/python

import sys
import numpy as np
current_key = None
current_trip_count = 0.0
# current_passenger_count = 0
# current_trip_distance = 0
# current_fare_amount = 0
# current_surcharge = 0
# current_tip_amount = 0
# current_tolls_amount = 0
# current_total_amount = 0

current_value_list = np.zeros(7)

for line in sys.stdin:
	key, value = line.strip().split("\t")
	value = value.split(',')
	value_list = []
	for v in value:
		value_list = np.append(value_list, float(v))
		#value_list.append(float(v))
	#passenger_count, trip_distance, fare_amount, surcharge, tip_amount, tolls_amount, total_amount = value_list
		#value_list = np.array(value_list)

	if key == current_key:
		# current_passenger_count += passenger_count
		# current_trip_distance += trip_distance
		# current_fare_amount += fare_amount
		# current_surcharge += surcharge
		# current_tip_amount += tip_amount
		# current_tolls_amount += tolls_amount
		# current_total_amount += total_amount
		current_trip_count +=1.
		current_value_list = current_value_list + value_list
	else:
		if current_key:
			current_value_list = current_value_list/current_trip_count
			tip_rate = current_value_list[4]/current_value_list[2]
			surcharge_rate = current_value_list[3]/current_value_list[2]
			mile_per_dollar = current_value_list[1]/current_value_list[6]
			value_string = '\t'
			for v in current_value_list:
				a = '%.4f,'%(v)
				value_string = value_string+a
			temp_string = '%.4f,%.4f,%.4f,%f' % (tip_rate, surcharge_rate, mile_per_dollar, current_trip_count)
			value_string = value_string+temp_string
			print current_key+value_string

		current_key = key
		current_value_list = value_list
		current_trip_count = 1 

current_value_list = current_value_list/current_trip_count
tip_rate = current_value_list[4]/current_value_list[2]
surcharge_rate = current_value_list[3]/current_value_list[2]
mile_per_dollar = current_value_list[1]/current_value_list[6]
value_string = '\t'
for v in current_value_list:
	a = '%.4f,'%(v)
	value_string = value_string+a

temp_string = '%.4f,%.4f,%.4f,%f' % (tip_rate, surcharge_rate, mile_per_dollar, current_trip_count)
value_string = value_string+temp_string
print current_key+value_string
