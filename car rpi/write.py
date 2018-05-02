
# Import and init an XBee device
from xbee import XBee, ZigBee
import serial
import threading

ser = serial.Serial("/dev/cu.usbserial-A5056VJ9", 9600)
# ser = serial.Serial('/dev/cu.usbserial-A5056WMY', 9600)
# ser = serial.Serial()
# print(serial.tools.list_ports.comports(include_links=False))
# Use an XBee 802.15.4 device
# xbee = XBee(ser)
# To use with an XBee ZigBee device, replace with:
# xbee = ZigBee(ser)
# Set remote DIO pin 2 to low (mode 4)
while 1:
   ser.write(bytearray(b'Hi!'))
   