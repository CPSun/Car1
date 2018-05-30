# d5 ON
# d7 & 8 toggle

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

while(True):
   GPIO.output(18, GPIO.HIGH)

   time.sleep(3)
   GPIO.output(18, GPIO.LOW)

   time.sleep(3)
   