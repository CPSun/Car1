
import threading
from vnpy import *
import serial
import random
import struct
import time
import queue
import csv
import os.path
import RPi.GPIO as GPIO

# STATUS
#  0  exit program
#  1  resume normal
#  2  pause 
#  3  Start

#  GPIO 3 = flap down
#  GIPO 2 = flap up

CRITICAL_FLAP_ANGLE = 3

#thread compares VN value to previous readings to determine lift angle
def checkFlap(vn, arduino):
   calib = 0
   for i in range(100):
      reading = vn.read_yaw_pitch_roll().z * -1
      print(reading)
      calib += reading
   calib /= 100
   print(calib)
   while(True):
      # print(vn.read_ins_solution_ecef().velocity)
      reading = vn.read_yaw_pitch_roll().z * -1 - calib
      print(reading)
      if(reading > CRITICAL_FLAP_ANGLE):
         print("HERE")
         GPIO.output(3, GPIO.LOW)
         GPIO.output(2, GPIO.HIGH)
         time.sleep(1)
         GPIO.output(3, GPIO.LOW)
         GPIO.output(2, GPIO.LOW)

#Gets the sum of values inclusive of start
def arrsum(arr, start, end):
   sum = 0
   for i in range(start, end):
      sum += arr[i]
   return sum / (end - start)

#Thread for testing and writing data
def writeData(pipe, file):
   print("Thread started")
   active = True
   paused = False
   while(active):
      arduino.reset_input_buffer()
      while(pipe.empty() and not paused):
         ardino_data = arduino.read(16)
         (v1, v2, v3, v4, c1, c2, c3, c4) = struct.unpack("hhhhhhhh", ardino_data)
         lla_data = vn.read_gps_solution_lla().lla
         lat = lla_data.x
         lng = lla_data.y
         temp = vn.read_imu_measurements().temp
         acc = vn.read_acceleration_measurements().y
         vel = vn.read_ins_solution_ecef().velocity.y
         time = vn.read_ins_solution_ecef().time
         xb.write(struct.pack("fhhhhhhhhfffff", time, v1, v2, v3, v4, c1, c2, c3, c4,
            lat, lng, temp, acc, vel))
         file.writerow([time, v1, v2, v3, v4, c1, c2, c3, c4,
            lat, lng, temp, acc, vel])
      command = pipe.get()
      print("Recieved a " + str(command))
      if(command == 0):
         active = False
         print("Quitting")
      if(command == 2):
         paused = True
         print("Paused")
         while(paused):
            command = pipe.get()
            if(command == 1):
               paused = False
               print("Resuming")
            elif(command == 0):
               print("Quitting")
               paused = False
               active = False

vn = VnSensor()
vn.connect('/dev/ttyUSB0', 115200)

xb = serial.Serial('/dev/ttyUSB1', 9600)

arduino = serial.Serial('/dev/ttyACM0', 9600)

#Sets up GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

GPIO.output(3, GPIO.HIGH)
GPIO.output(2, GPIO.LOW)
time.sleep(3)
GPIO.output(3, GPIO.LOW)
GPIO.output(2, GPIO.LOW)
pipe = queue.Queue()

testing = False
i = 0


#stats thread to monitor flap
flapThread = threading.Thread(target=checkFlap, args=(vn, arduino))
flapThread.start()


# finds a new file name
while(os.path.isfile("test"+str(i) + '.csv')):
   i+=1
with open('test'+str(i)+'.csv', 'w', newline='') as csvfile:
   dataFile = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
   while(True):
      reading = xb.read(1)
      (value,) = struct.unpack('c', reading)
      value = 3
      if(int(value) == 3 and not testing):
         tell = threading.Thread(target=writeData, args=(pipe,dataFile))
         tell.start()
         testing = True
      if(testing):
         pipe.put(int(reading))