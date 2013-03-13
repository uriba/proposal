import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim
from subprocess import call

file_name_prefix = "graph1"

def ploti(i):
    nums = []
    with open('%s%d.csv' % (file_name_prefix,i),'rb') as csvfile:
        vals = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in vals:
            nums.append(map(float,row))
    return nums

def set_ticks(a):
    for t in a.yaxis.get_major_ticks():
        t.label.set_fontsize(15)
    for t in a.xaxis.get_major_ticks():
        t.label.set_fontsize(15)

anums = []
for i in range(1,5):
    anums.append(ploti(i))

fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)
a1 = subplot(111)
a1.plot(anums[0][0],anums[0][1])
a1.set_xlabel("Time [Hour]",fontsize=20)
a1.set_ylabel("Detected OD",fontsize=20)
set_ticks(a1)
a1.set_title('E.Coli, M9, 0.2% Glu',fontsize=20)
fig.savefig('OD1.png')

fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)
a2 = subplot(111)
a2.plot(anums[1][0],anums[1][1])
a2.set_xlabel("Time [Hour]",fontsize=20)
a2.set_ylabel("Background subtracted OD",fontsize=20)
a2.set_title('E.Coli, M9, 0.2% Glu',fontsize=20)
set_ticks(a2)
fig.savefig('OD2.png')

fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)
a3 = subplot(111)
a3.plot(anums[2][0],anums[2][1])
a3.set_xlabel("Time [Hour]",fontsize=20)
a3.set_ylabel("Log (base 2) OD",fontsize=20)
a3.set_title('E.Coli, M9, 0.2% Glu',fontsize=20)
set_ticks(a3)
fig.savefig('OD3.png')

fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)
a4 = subplot(111)
a4.plot(anums[3][0],anums[3][1])
a4.set_xlabel("Time [Hour]",fontsize=20)
a4.set_ylabel("Doublings per hour [Hour$^{-1}$]",fontsize=20)
a4.set_title('E.Coli, M9, 0.2% Glu',fontsize=20)
set_ticks(a4)
fig.savefig('OD4.png')
