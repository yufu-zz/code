#! /usr/bin/env python

import lcm
from laser_t import laser_t

def handler(channel, data):
	msg = laser_t.decode(data)
	print("Number of ranges " + str(msg.radstep)) 


if __name__ == '__main__':
	lc = lcm.LCM()
	subscription = lc.subscribe("LASER", handler)

	try:
		while True:
			lc.handle()
	except KeyboardInterrupt:
		pass
	lc.unsubscribe(subscription)
