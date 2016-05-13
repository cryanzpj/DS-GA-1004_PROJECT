#!/usr/bin/python
# Edit by Shida Wu

import sys
from operator import itemgetter

# init hours
hours = {0:[0, 5], 1:[5, 10], 2:[10,15.5],3:[15.5, 20], 4:[20, 24]}
taxi_dist = {0:[], 1:[], 2:[], 3:[], 4:[]}

for line in sys.stdin:
        data = line.split('\t')
        datetime = data[0]
        if "Date" not in datetime:
                clock = map(int, datetime.split(" ")[1].split(":")[:-1])
                if clock[0] >= 0 and clock[0] < 5:
                        hour_index = 0
                elif clock[0] >= 5 and clock[0] < 10:
                        hour_index = 1
                elif clock[0] >= 10 and clock[0] <= 14:
                        hour_index = 2
                elif clock[0] >= 15 and clock[0] < 16:
                        if clock[1] < 30:
                                hour_index = 2
                        else:
                                hour_index = 3
                elif clock[0] >= 16 and clock[0] < 20:
                        hour_index = 3
                else:
                        hour_index = 4
                taxi_dist[hour_index].append(int(data[1]))

sorted_dist = sorted(taxi_dist.items(), key=itemgetter(0))
for key, values in sorted_dist:
        print '%s\t%i' % (','.join([str(hours[key][i]) for i in range(2)]), sum(values))


