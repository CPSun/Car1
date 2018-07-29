# d5 ON
# d7 & 8 toggle

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

while(True):
   GPIO.output(2, GPIO.HIGH)
   GPIO.output(3, GPIO.LOW)  
   time.sleep(3)
   