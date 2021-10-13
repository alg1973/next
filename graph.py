#!/usr/bin/python

import matplotlib.pyplot as plt
import datetime
import th_data
import sys

term_data = th_data.th_data()

p=60
if len(sys.argv)==2:
        p=int(sys.argv[1])
        
(ts, values) = term_data.get_data(p)

dates = map(datetime.datetime.fromtimestamp, ts)

# plotting the points
#plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3,
#		marker='o', markerfacecolor='blue', markersize=12)

#plt.plot(x, y)
plt.plot_date(dates, values, linestyle='dashed', linewidth = 1)	

# setting x and y axis range
plt.ylim(5,24)
#plt.xlim(1634067688,1634071209)

# naming the x axis
plt.xlabel('date')
# naming the y axis
plt.ylabel('T(C)')

# giving a title to my graph
plt.title('Temperature')

# function to show the plot
plt.show()
