#Kartik Vats & Manasi Nagtode
#PROVE Vehicle Master Script
#March 13, 2017 v1.0

#importing modules
import serial
import time
import threading
from xbee import XBee
from tkinter import *
from tkinter.scrolledtext import *
from vnpy import *

#One-Dimensional Kalman Filter: You will create an object
#of this for every sensor you wish to filter
# class KalmanFilter:
#         q = 1.0 #process noise covariance
#         r = 1.0 #measurement noise covariance
#         x = 0.0 #value
#         p = 1.0 #estimation error covariance
#         k = 1.0 #kalman gain

#         def __init__(self, q, r, p, start):
#                 self.q = q
#                 self.r = r
#                 self.p = p
#                 self.x = start
#         def update(self, measurement):
#                 #prediction update
#                 self.p = self.p + self.q
                
#                 #measurement update
#                 self.k = self.p / (self.p + self.r)
#                 self.x = self.x + self.k * (measurement - self.x)
#                 self.p = (1 - self.k) * self.p


#Global flag for if there is a run going on
running = False 

#File to write to on microSD card
file = None

#Global variables containing serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)
ez = EzAsyncData.connect("/dev/ttyUSB1", 115200) #?
vn = ez.sensor
xbee = XBee(serial.Serial("/dev/ttyUSB0", 9600))

# def smoothen(data, alpha, pastSmoothed):
#     if alpha >= 1:
#         alpha = 0.99
#     elif alpha < 0:
#         alpha = 0
#     return (data * (1 - alpha) + (pastSmoothed * alpha))

vnPitch = 0.0
vnAccelX = 0.0
vnAccelY = 0.0
vnAccelZ = 0.0

def readVector():
   global vnPitch
   global vnAccelX
   global vnAccelY
   global vnAccelZ
   
   while running == True:
      reg = vn.read_yaw_pitch_roll_magnetic_acceleration_and_angular_rates()
      vnPitch = reg.yaw_pitch_roll.y
      if vnPitch > 30:
         print("deploy solenoid\n")
         #Write to xbee
      vnAccelX = reg.accel.x
      vnAccelY = reg.accel.y
      vnAccelZ = reg.accel.z
   return

#Function you need to work with
def readData(): #Reads All Serial Data from Arduino&VectorNAV, also writes data to xbee
    readVal = 1
    first = True
    while running == True:
        tempData = ser.readline().decode().strip() #tempData is the string coming from arduino
        values = tempData.split() #values is a 0 indexed array which holds a string for each sensor value from arduino
      #   if first == True:
      #       first = False
      #       #If you wish to use KalmanFilters on additional sensors here is where you add them.
        ts1 = float(values[len(values) - 1])
      #       #vnaccelXKF = KalmanFilter(1.0, 1.0, 1.0, vnAccelX)
      #       #above is the init for kf
      #       #if smoothing additional values, declare those variables here
      #       asz1smooth = 0
      #   else:
        ts1.update(float(values[len(values) - 1]))
      #       #vnaccelXKF.update(vnAccelX)

      #second parameter alpha is (0, 1) if > .5 will weigh past data more, less than .5 weighs current data more
      #   asz1smooth = smoothen(float(values[4]), 0.05, asz1smooth)
        
        print("Raw Value: ", float(values[4]),"\n")
        print("Raw Value: ", float(values[5]), "\n")
        #reg = vn.read_yaw_pitch_roll_magnetic_acceleration_and_angular_rates()
        #if reg.yaw_pitch_roll.y > 30:
        #        print("deploy solenoid\n")
        #array values is 0-indexed, when you add more sensors to arduino code make sure you update it here
        tempData = values[0] + "\t" + values[1] + "\t" + values[2] + "\t"
        tempData = tempData + values[3] + "\t"
        tempData = tempData + "\t" + "%.3f" % vnAccelX + "\t" + "%.3f" % vnAccelY + "\t" + "%.3f" % vnAccelZ
        tempData = tempData + "\t" + "%.3f" % vnPitch + "\t"
        #tempData = tempData + "%.3f" % vnaccelXKF.x + "\t"
        tempData = tempData + "%.3f" % ts1 + "\n" #as of now ts1.x is temperature, make sure right before new line you insert temperature
        
        textScreen.insert(INSERT, tempData)
        file.write(tempData)
        xbee.write(tempData.encode("utf-8"))
        textScreen.see(END)
    file.close()
    return

#Function called when the start button is clicked
def start():
   global running
   global file

   if running == False:
      fileName = time.strftime("Run at %I.%M.%S %m-%d-%Y.csv")
      file = open(fileName, "w+")
      ser.flushInput()
      textScreen.delete(1.0,END)
      running = True
      readVnThread = threading.Thread(target=readVector)
      readDataThread = threading.Thread(target=readData)
      readVnThread.start()
      readDataThread.start()
    
#Function called when stop button is clicked
def stop():
   global running

   if running == True:
      running = False
        


#Popup GUI
root = Tk()
root.title("PROVE Vehicle 1.0")

#Declaring buttons here and telling them which functions to call when clicked
startButton = Button(root, text="Start Run", command=start)
stopButton = Button(root, text="Stop Run", command=stop)

textScreen = ScrolledText(master = root, wrap =WORD, width = 120, height = 12)
textScreen.pack(padx=10, pady=10, fill=BOTH, expand=True)


#Putting buttons into GUI Window
startButton.pack()
stopButton.pack()

root.mainloop()