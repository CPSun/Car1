from vnpy import *
s = VnSensor()
s.connect('/dev/ttyUSB0', 115200)
# c = EzAsyncData.connect('/dev/ttyUSB0', 115200)
while(1):
   # print(c.next_data().any_acceleration)
   print(s.read_gps_solution_ecef().velocity)
   print(s.read_yaw_pitch_roll())
#    print(s.read_yaw_pitch_roll())