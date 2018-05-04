import serial
from xbee import XBee
from struct import unpack

ser = serial.Serial("/dev/cu.usbserial-A5056VJ9", 9600)
xbee = XBee(ser)
while(1):
   print(int(ser.read().decode('utf8')))
