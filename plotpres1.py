from matplotlib.pyplot import plot,show,figure,subplot,ylim,title
from numpy import linspace
from numpy.random import random,normal

fig = figure()
a1 = subplot(121)
a1.set_xlabel("Time [Hour]")
a1.set_ylabel("Amount")
title("Logarithmic - non-balanced")
x = linspace(0,10)
y = 2**x
z = abs(normal(0.5,0.2,50)*y)
a1.plot(x,y,x,z)
a2 = subplot(122)
z2 = 0.5*z
a2.plot(x,z,x,z2)
a2.set_xlabel("Time [Hour]")
a2.set_ylabel("Amount")
title("Balanced - non-logarithmic")

show()
