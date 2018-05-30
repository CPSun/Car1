import csv
import matplotlib.pyplot as plot

with open('tests/18-05-22/20-17-42.csv', newline='') as csvfile:
   data = csv.reader(csvfile, delimiter=' ', quotechar='|')
   run = []
   for row in data:
      run.append(list(map(lambda value: float(value), row)))

   fig = plot.figure(figsize=(8,8))
   axis = [fig.add_subplot(4,2,1)]
   plot.ylim((0, 1000))
   for i in range(2, 9):
      axis.append(fig.add_subplot(5,2,i, sharey=axis[0]))
      plot.autoscale(False, axis='y')

   for i in range(8):
      axis[i].plot(list(map(lambda point: point[i], run)), color='black', marker='.', markeredgewidth=0)
   print(run[0])
   distance = 0
   for i in range(1, len(run)):
      distance += ((run[i][8] - run[i-1][8]) ** 2 + (run[i][9] - run[i-1][9]) ** 2) ** .5
   print(distance)
   plot.text(0,-500,"Distance:  " + str(distance))

   plot.show()