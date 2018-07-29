
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

# frame = vn.read_reference_frame_rotation()
# frame.e00 = 0
# frame.e01 = 0
# frame.e02 = 1
# frame.e10 = 0
# frame.e11 = 1
# frame.e12 = 0
# frame.e20 = -1
# frame.e21 = 0
# frame.e22 = 0
# vn.write_reference_frame_rotation(frame)


while True:
   print(vn.read_yaw_pitch_roll())