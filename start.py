import sched
import time

def main(schedule):
	# main program execution
	schedule.enter(7200, 1, main, (schedule,))


if __name__ == '__main__':
    # begin main program on schedule
    schedule = sched.scheduler(time.time, time.sleep)
    schedule.enter(1, 1, main, (schedule,))
    schedule.run()
