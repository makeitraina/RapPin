import sched
import sys
import time

from logic.scraper import parse

def main(schedule, access_token):
	# main program execution
	parse(access_token)

	# run schedule
	schedule.enter(7200, 1, main, (schedule, access_token,))

def start():
	# check for pinterst access token
	if len(sys.argv) != 2:
		print('RapPin requires the access token as an argument')
		return

	access_token = sys.argv[1]

	# begin main program on schedule
	schedule = sched.scheduler(time.time, time.sleep)
	schedule.enter(1, 1, main, (schedule,access_token,))
	schedule.run()

if __name__ == '__main__':
	start()
