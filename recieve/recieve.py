
   
import matplotlib.pyplot as plot
from matplotlib.widgets import Button
import matplotlib.animation as animation
import matplotlib as mpl
import numpy as np
import time
import serial
import struct
import csv
xb = serial.Serial("/dev/cu.usbserial-A5056WMY")

x = 1
fig = plot.figure()
axis = [fig.add_subplot(5,2,1)]
axis[0].set_ylim((0,1000))
axis[0].set_xlim((0,10))
axis[0].autoscale(False)

def clicked(event):
   globals()["time"] = 0

ax = plot.axes([0.7, 0.05, 0.1, 0.075])
button = Button(ax, 'Next')
button.on_clicked = clicked
for i in range(2, 9):
   axis.append(fig.add_subplot(5,2,i, sharex=axis[0], sharey=axis[0]))
# with open('data.csv', 'a', newline='') as csvfile:
#    file = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
globals()['time'] = 0
def animate(i):
      timescale = 5
   # while x < 20:
      globals()['time'] += 1
      data = xb.read(28)
      data = (struct.unpack("hhhhhhhhfff", data))
      # file.writerow(data)
      print(data)
      for i in range(8):
         axis[i].autoscale(False)
         axis[i].plot(globals()['time']/ timescale,data[i], color='black', marker='.', markeredgewidth=0)
      if(globals()["time"]/timescale > 5):
         axis[i].set_xlim([globals()["time"]/timescale-5, globals()["time"]/timescale+5])
      # plot.pause(.0001)
ani = animation.FuncAnimation(fig, animate, repeat=False, interval=2)
plot.show()