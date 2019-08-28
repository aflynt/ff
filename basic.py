#!/opt/rh/rh-python36/root/usr/bin/python
import tkinter
import matplotlib.pyplot as plt

x =[1, 2, 3, 4]
y =[2, 3, 9, 24]

# MANUAL PLOTTING
#plt.ylim(-4,4)

plt.use('TkAgg')
plt.ylabel(r'$Forces$ $(N)$')
plt.title('Global Forces')
plt.plot(x,y  ,'-', label=r'$F_x (N)$')
plt.show()
