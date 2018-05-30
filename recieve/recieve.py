import matplotlib.pyplot as plot
from matplotlib.widgets import Button
import matplotlib.animation as animation
import matplotlib as mpl
import numpy as np
import time
import serial
import struct
import csv
import queue
import datetime
import os.path
import os
import threading

xb = serial.Serial("/dev/cu.usbserial-A5056WMY")

pipe = queue.Queue()

x = 1
fig = plot.figure()
axis = [fig.add_subplot(5,2,1)]
axis[0].set_ylim((0,1000))
axis[0].set_xlim((0,20))
axis[0].autoscale(False)

def start(event):
   xb.write(struct.pack('c', b'3'))
   xb.write(struct.pack('c', b'1'))
   print("Started")

def stop(event):
   xb.write(struct.pack('c', b'2'))
   print("Stopped")
   plot.close()

def listen(file):
   while(True):
      data = xb.read(28)
      data = (struct.unpack("hhhhhhhhfff", data))
      g = globals()['data']
      for i in range(8):
         g[i].append(data[i])
      globals()['data'] = g
      file.writerow(data)
      print(data)

ax = plot.axes([0.6, 0.05, 0.1, 0.075])
button = Button(ax, 'Stop')
button.on_clicked(stop)
ax = plot.axes([0.7, 0.05, 0.1, 0.075])
button2 = Button(ax, 'Start')
button2.on_clicked(start)
for i in range(2, 9):
   axis.append(fig.add_subplot(5,2,i, sharex=axis[0], sharey=axis[0]))

globals()['data'] = [[],[],[],[],[],[],[],[]]

def animate(i, pipe):
   data = globals()["data"]
   for i in range(8):
      axis[i].autoscale(False)
      axis[i].plot(data[i], color='black', marker='.', markeredgewidth=0)
   if(len(data[0]) > 20):
      axis[i].set_xlim(len(data[0])-10,len(data[0])+10)
i = 0

date = time.strftime("%y-%m-%d")
time = time.strftime("%H-%M-%S")
if not os.path.exists("tests"):
   os.makedirs("tests")
if not os.path.exists("tests/" + date):
   os.makedirs("tests/" + date)

with open('tests/' + date + '/' + time + '.csv', 'w', newline='') as csvfile:
   file = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
   listen = threading.Thread(target=listen, args=(file,))
   listen.start()
   ani = animation.FuncAnimation(fig, animate, repeat=False, interval=1000, fargs=(pipe,))
   plot.show()
   csvfile.close()