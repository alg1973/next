import matplotlib.pyplot as plt

# x axis values
#x = [1,2,3,4,5,6]
# corresponding y axis values
#y = [2,4,1,5,2,6]
y = [18.437, 
     18.437, 
     18.375, 
     18.375, 
     18.375, 
     18.375, 
     18.375, 
     18.375, 
     18.375, 
     18.375, 
     18.375, 
     18.375, 
     18.375, 
     18.375, 
     18.375, 
     18.312, 
     18.312, 
     18.312, 
     18.312, 
     18.312, 
     18.312, 
     18.312, 
     18.312, 
     18.312, 
     18.312, 
     18.25, 
     18.25, 
     18.25, 
     18.25] 

x = [ 1634067688.03,
      1634067809.78,
      1634067936.66,
      1634068058.42,
      1634068180.18,
      1634068306.98,
      1634068428.83,
      1634068550.66,
      1634068672.35,
      1634068794.1,
      1634068915.95,
      1634069042.74,
      1634069164.42,
      1634069286.19,
      1634069407.94,
      1634069529.7,
      1634069711.63,
      1634069833.46,
      1634069960.27,
      1634070086.99,
      1634070208.75,
      1634070335.62,
      1634070457.39,
      1634070579.14,
      1634070700.75,
      1634070827.39,
      1634070964.74,
      1634071086.42,
      1634071208.18]

# plotting the points
#plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3,
#		marker='o', markerfacecolor='blue', markersize=12)

plt.plot(x, y)
	

# setting x and y axis range
plt.ylim(18,19)
plt.xlim(1634067688,1634071209)

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('Some cool customizations!')

# function to show the plot
plt.show()
