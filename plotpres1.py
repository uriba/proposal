from matplotlib.pyplot import plot,show,figure,subplot,ylim,title,legend
from numpy import linspace, arange, amax
from numpy.random import random,normal

fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)
a1 = subplot(121)
a1.set_xlabel("Time [Hour]",fontsize=20)
a1.set_ylabel("Amount",fontsize=20)
title("Logarithmic - non-balanced",fontsize=20)
x = linspace(0,10)
y = 2**x
rands = normal(0.5,0.2,50)
z = abs(rands*y)
a1.plot(x,y,x,z)
a1.fill_between(x,y,z)
a1.fill_between(x,z,0,facecolor='green')
legend(('RNA','Protein'),prop={'size':20},loc='upper left')
a2 = subplot(122)
z1 = arange (50)
rands = normal(0.05,0.1,50)
z1[0] = rands[0]
for i in range (0,50):
    z1[i] = z1[i-1]*(1+rands[i])
z2 = 0.5*z1
a2.plot(x,z1,x,z2)
a2.fill_between(x,z1,z2)
a2.fill_between(x,z2,0,facecolor='green')
ylim((0,amax(z1)))
a2.set_xlabel("Time [Hour]",fontsize=20)
a2.set_ylabel("Amount",fontsize=20)
title("Balanced - non-logarithmic",fontsize=20)

fig.savefig('balance.png')
