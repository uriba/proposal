from matplotlib.pyplot import plot,show,figure,subplot,ylim
from numpy import linspace
from numpy.random import random,normal

fig = figure()
a1 = subplot(121)
a1.set_xlabel("Time [Hour]")
a1.set_ylabel("Amount")
x = linspace(0,10)
y = 2**x
z = abs(normal(0.5,0.2,50)*y)
a1.plot(x,y,x,z)
a2 = subplot(122)
y2= 5*x
z2 = 2*x
a2.plot(x,y2,x,z2)
a2.set_xlabel("Time [Hour]")
a2.set_ylabel("Amount")

show()
