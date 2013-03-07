import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,savefig
from subprocess import call

file_name_prefix = "graph1"
call(["./fig1data", "%s" % file_name_prefix])

def ploti(i):
    nums = []
    with open('%s%d.csv' % (file_name_prefix,i),'rb') as csvfile:
        vals = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in vals:
            nums.append(map(float,row))
    return nums

fig = figure()
a = subplot(111)
anums = ploti(1)
a.plot(anums[0],anums[1])
a.set_xlabel("Time [Hour]",fontsize=20)
a.set_ylabel("Detected OD",fontsize=20)
for tick in a.xaxis.get_major_ticks():
    tick.label.set_fontsize(14)
for tick in a.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)
fig.set_size_inches(12,9)
fig.set_dpi(80)
savefig('ODPlot1.png')
show()
