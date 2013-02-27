import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim
from subprocess import call

file_name_prefix = "graph1"
call(["rm","fig1data"])
call(["ghc","fig1data"])
call(["./fig1data", "%s" % file_name_prefix])

def ploti(i):
    nums = []
    with open('%s%d.csv' % (file_name_prefix,i),'rb') as csvfile:
        vals = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in vals:
            nums.append(map(float,row))
    return nums

fig = figure()
anums = []
for i in range(1,5):
    anums.append(ploti(i))
a1 = subplot(221)
a1.plot(anums[0][0],anums[0][1])
a1.set_xlabel("Time [Hour]")
a1.set_ylabel("Detected OD")
a1.text(0.1,0.9,"(1)",horizontalalignment='right',verticalalignment='bottom',transform=a1.transAxes)
a2 = subplot(222,sharey=a1, sharex = a1)
a2.plot(anums[1][0],anums[1][1])
a2.set_xlabel("Time [Hour]")
a2.set_ylabel("Background subtracted OD")
a2.text(0.1,0.9,"(2)",horizontalalignment='right',verticalalignment='bottom',transform=a2.transAxes)
a3 = subplot(223, sharex = a1)
a3.plot(anums[2][0],anums[2][1])
a3.set_xlabel("Time [Hour]")
a3.set_ylabel("Log (base 2) OD")
a3.text(0.1,0.9,"(3)",horizontalalignment='right',verticalalignment='bottom',transform=a3.transAxes)
a4 = subplot(224, sharex = a1)
a4.plot(anums[3][0],anums[3][1])
a4.set_xlabel("Time [Hour]")
a4.set_ylabel("Growth rate (base 2) [Hour$^{-1}$]")
a4.text(0.1,0.9,"(4)",horizontalalignment='right',verticalalignment='bottom',transform=a4.transAxes)

show()
