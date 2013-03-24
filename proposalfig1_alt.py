import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,legend,xlim,axvspan,tight_layout
from subprocess import call
import numpy as np

axisfontsize = 8
ticksize = 6
annotation_size = 8
file_name_prefix = "graph2"
initcutoff = 22
activityoffset = 10
def ploti(i):
    nums = []
    with open('%s%d.csv' % (file_name_prefix,i),'rb') as csvfile:
        vals = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in vals:
            nums.append(map(float,row))
    return nums

def set_ticks(a):
    for t in a.yaxis.get_major_ticks():
        t.label.set_fontsize(ticksize)
    for t in a.xaxis.get_major_ticks():
        t.label.set_fontsize(ticksize)

anums = []
for i in range(1,5):
    anums.append(ploti(i))

fig = figure()
fig.set_size_inches(5,7)
fig.set_dpi(80)

x = np.array(anums[1][0])
y = np.array(anums[1][1])
x1 = np.array(anums[3][0])
y1 = np.array(anums[3][1])/1000
x2 = np.array(anums[3][2])
y2 = np.array(anums[3][3])/1000

a1 = subplot(322)
a1.plot(y[initcutoff:],y1[initcutoff:],"g.",y[initcutoff:],y2[initcutoff:],"r.")
a1.set_ylabel("Protein level\nper OD [au]",fontsize=axisfontsize)
set_ticks(a1)
ylim(0,35)
# xlim(15,25)

a2 = subplot(321)
x3 = np.array(anums[2][0])
y3 = np.array(anums[2][1])/1000
x4 = np.array(anums[2][2])
y4 = np.array(anums[2][3])/1000
a2.plot(y[initcutoff:],y3[initcutoff-activityoffset:-activityoffset],"g.",
        y[initcutoff:],y4[initcutoff - activityoffset:- activityoffset],"r.")
a2.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a2.set_ylabel("Protein Acc. rate\nper OD [au]",fontsize=axisfontsize)
# legend(('YFP','mCherry'),prop={'size':ticksize})
# xlim(15,25)
ylim(0,50)
set_ticks(a2)

a3 = subplot(324)
a3.plot(y[initcutoff:],y1[initcutoff:]/y[initcutoff:],"g.",y[initcutoff:],y2[initcutoff:]/y[initcutoff:],"r.")
a3.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a3.set_ylabel("Protein level\nper OD/Growth rate [au]",fontsize=axisfontsize)
set_ticks(a3)

a4 = subplot(323)
a4.plot(y[initcutoff:],y3[initcutoff - activityoffset:-activityoffset]/y[initcutoff:],"g.",
        y[initcutoff:],y4[initcutoff - activityoffset:-activityoffset]/y[initcutoff:],"r.")
a4.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a4.set_ylabel("Protein Acc. rate\nper OD/Growth rate [au]",fontsize=axisfontsize)
set_ticks(a4)

a5 = subplot(325)
a5.plot(y[initcutoff:],y3[initcutoff - activityoffset:-activityoffset]/(y[initcutoff:]*y[initcutoff:]),"g.",
        y[initcutoff:],y4[initcutoff - activityoffset:-activityoffset]/(y[initcutoff:]*y[initcutoff:]),"r.")
a5.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a5.set_ylabel("Protein Acc. rate\nper OD/Growth rate^2 [au]",fontsize=axisfontsize)
set_ticks(a5)

tight_layout()
fig.savefig('propfig1_alt.pdf')
