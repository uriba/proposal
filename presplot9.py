import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,savefig
from subprocess import call

file_name_prefix = "graph2"
call(["./fig1data", "%s" % file_name_prefix])

def ploti(i):
    nums = []
    with open('%s%d.csv' % (file_name_prefix,i),'rb') as csvfile:
        vals = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in vals:
            nums.append(map(float,row))
    return nums

fig = figure()
a = subplot(211)
anums = ploti(4)
a.plot(anums[0],anums[1],"g",anums[2],anums[3],"r")
a.set_xlabel("Time [Hour]",fontsize=20)
a.set_ylabel("Protein level (au)",fontsize=20)
ylim([0,35000])
for tick in a.xaxis.get_major_ticks():
    tick.label.set_fontsize(14)
for tick in a.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)

a = subplot(212)
anums = ploti(3)
a.plot(anums[0],anums[1],"g",anums[2],anums[3],"r")
a.set_xlabel("Time [Hour]",fontsize=20)
a.set_ylabel("Protein accumulation rate (au)",fontsize=20)
for tick in a.xaxis.get_major_ticks():
    tick.label.set_fontsize(14)
for tick in a.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)
fig.set_size_inches(12,9)
fig.set_dpi(80)
savefig('FLPlot5.png')
show()