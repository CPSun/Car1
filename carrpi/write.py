
import threading
from vnpy import *
import serial
import random
import struct
import time
import queue
import csv
import os.path

# STATUS
#  0  exit program
#  1  resume normal
#  2  pause 
#  3  Start

def writeData(pipe, file):
   print("Thread started")
   active = True
   paused = False
   while(active):
      ardino.reset_input_buffer()
      while(pipe.empty() and not paused):
         ardino_data = ardino.read(16)
         (v1, v2, v3, v4, c1, c2, c3, c4) = struct.unpack("hhhhhhhh", ardino_data)
         lla_data = vn.read_gps_solution_lla().lla
         lat = lla_data.x
         lng = lla_data.y
         temp = vn.read_imu_measurements().temp
         acc = vn.read_acceleration_measurements().z
         vel = vn.read_ins_solution_ecef().velocity.z
         xb.write(struct.pack("hhhhhhhhfffff", v1, v2, v3, v4, c1, c2, c3, c4,
            lat, lng, temp, acc, vel))
         file.writerow([v1, v2, v3, v4, c1, c2, c3, c4,
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

ardino = serial.Serial('/dev/ttyACM0', 9600)

pipe = queue.Queue()
i = 0
calibx = 0
caliby = 0
calibz = 0
print("CALIBRATING")

while(i < 10):
   vnData = vn.read_yaw_pitch_roll()
   calibx += vnData.x
   caliby += vnData.y
   calibz += vnData.z
   print(i)
   i+=1

calibx = calibx / 10
caliby = caliby / 10
calibz = calibz / 10
print("DONE")

testing = False
i = 0
while(os.path.isfile("test"+str(i) + '.csv')):
   i+=1
with open('test'+str(i)+'.csv', 'w', newline='') as csvfile:
   dataFile = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
   while(True):
      reading = xb.read(1)
      (value,) = struct.unpack('c', reading)
      print(int(reading))
      value = 3
      if(int(value) == 3 and not testing):
         tell = threading.Thread(target=writeData, args=(pipe,dataFile))
         tell.start()
         testing = True
      if(testing):
         pipe.put(int(reading))