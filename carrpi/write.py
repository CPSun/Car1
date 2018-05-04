
from xbee import XBee
import threading
from vnpy import *
import serial

vn = VnSensor()
vn.connect('/dev/ttyUSB0', 115200)
ser = serial.Serial("/dev/ttyUSB1", 9600)
xbee = XBee(ser)

# c = EzAsyncData.connect('/dev/ttyUSB0', 115200)
#    print(s.read_yaw_pitch_roll())

# ser = serial.Serial('/dev/cu.usbserial-A5056WMY', 9600)
# ser = serial.Serial()
# print(serial.tools.list_ports.comports(include_links=False))
# Use an XBee 802.15.4 device
# xbee = XBee(ser)
# To use with an XBee ZigBee device, replace with:
# xbee = ZigBee(ser)
# Set remote DIO pin 2 to low (mode 4)
x=0
while x< 20:
   reading = vn.read_yaw_pitch_roll()
   print(str(reading.x), reading.x)
   ser.write(str(x).encode("utf-8"))
   x+=1
   # print({int(reading.x), int(reading.y), int(reading.z)})
   # bytearray({int(reading.x), int(reading.y), int(reading.z)})
   # b=bytearray({reading.x})
   # b.extend(reading.x)
   # ser.write(b)