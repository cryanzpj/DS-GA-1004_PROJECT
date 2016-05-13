#!/usr/bin/python
# Edit by Shida Wu
# map function for yellow taxi

import sys

for line in sys.stdin:
	line = line.strip()
	line = line.split(",")
	if len(line) > 1:
		pickup_datetime = line[1]
		print '%s\t%i' % (pickup_datetime, 1)
	
