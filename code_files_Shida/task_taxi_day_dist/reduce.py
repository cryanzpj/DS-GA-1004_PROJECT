#!/usr/bin/python
# Edit by Shida Wu

import sys
from operator import itemgetter

taxi_day_dist = {}
total = 0
for line in sys.stdin:
	data = line.split('\t')
	key = data[0].strip()
	value = int(data[1])
	total += value
	if key != "pickup_datetime":
		if key not in taxi_day_dist:
			taxi_day_dist[key] = [value]
		else:
			taxi_day_dist[key].append(value)

for key, value in taxi_day_dist.items():
	taxi_day_dist[key] = sum(value) * 1.0 / total
sorted_taxi = sorted(taxi_day_dist.items(), key=itemgetter(0))
for key, val in sorted_taxi:
	print '%s\t%s' % (key, val)
