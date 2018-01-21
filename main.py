from datetime import datetime
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import EmailAlert

camera = PiCamera()
GPIO.setmode(GPIO.BCM)


#set GPIO Pins
TRIGGER = 23
ECHO = 24
THRESHOLD_DISTANCE = 20

#set GPIO direction (IN / OUT)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)


    # save StartTime
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()

    #Duration
    TimeElapsed = StopTime - StartTime


    distance = (TimeElapsed * 34300) / 2

    return distance


try:
    while True:
        d = distance()
        print ("Measured Distance = %.1f cm" % d)
	if d<THRESHOLD_DISTANCE:
	    path ='/home/image'+"%.21s"%str(datetime.now())+'.jpg'
	    camera.start_preview()
	    #Give some time for the sensors to set its light levels
	    time.sleep(0.2)
	    camera.capture(path)
	    print "Image captured"
	    EmailAlert.mailAlert(path)
	    camera.stop_preview

        time.sleep(1)

# Stop by pressing CTRL + C
except KeyboardInterrupt:
    print("Programmed stopped")
    GPIO.cleanup()
