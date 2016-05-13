#!/usr/bin/python
# Edit by Shida Wu

import sys
from operator import itemgetter

uber_day_dist = {}
total = 0
for line in sys.stdin:
	data = line.split('\t')
	key = data[0].strip()
	value = int(data[1])
	total += value
	if key != "pickup_datetime":
		if key not in uber_day_dist:
			uber_day_dist[key] = [value]
		else:
			uber_day_dist[key].append(value)

for key, value in uber_day_dist.items():
	uber_day_dist[key] = sum(value) * 1.0 / total
sorted_uber = sorted(uber_day_dist.items(), key=itemgetter(0))
for key, val in sorted_uber:
	print '%s\t%s' % (key, val)
