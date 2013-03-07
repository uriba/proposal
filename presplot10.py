import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,savefig
from subprocess import call

file_name_prefix = "graph3"
call(["./fig3data", "%s" % file_name_prefix])

def ploti(i):
    nums = []
    with open('%s1%d.csv' % (file_name_prefix,i),'rb') as csvfile:
        vals = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in vals:
            nums.append(map(float,row))
    return nums

fig = figure()
anums = []
for i in range(1,3):
    anums.append(ploti(i))
a1 = subplot(121)
a1.plot(anums[0][0],anums[0][1],"ro")
a1.set_xlabel("Growth rate (base 2) [Hour$^{-1}$]",fontsize=20)
a1.set_ylabel("Protein accumulation rate (au)",fontsize=20)
for tick in a1.xaxis.get_major_ticks():
    tick.label.set_fontsize(14)
for tick in a1.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)

a2 = subplot(122,sharex = a1)
a2.plot(anums[1][0],anums[1][1],"ro")
a2.set_xlabel("Growth rate (base 2) [Hour$^{-1}$]",fontsize=20)
a2.set_ylabel("Protein level (au)",fontsize=20)
for tick in a2.xaxis.get_major_ticks():
    tick.label.set_fontsize(14)
for tick in a2.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)
fig.set_size_inches(12,9)
fig.set_dpi(80)
savefig('CorPlot1.png')
show()
