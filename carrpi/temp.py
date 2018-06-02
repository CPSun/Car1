
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


vn = VnSensor()
vn.connect('/dev/ttyUSB0', 115200)
while(1):
   # print(vn.read_acceleration_measurements())
   # print(vn.read_yaw_pitch_roll())
   # print(vn.read_gps_solution_lla().lla)
   # print(vn.read_imu_measurements().temp)
   print(vn.read_ins_solution_ecef().velocity.z)