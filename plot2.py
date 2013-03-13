import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim
from subprocess import call

file_name_prefix = "graph2"
call(["rm","fig2data"])
call(["ghc","fig2data"])
call(["./fig2data", "%s" % file_name_prefix])

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
a1.plot(anums[0][2],anums[0][3],"g",anums[0][4],anums[0][5],"r")
a1.set_ylabel("Detected Fluorescence")
a1x = a1.twinx()
a1x.plot(anums[0][0],anums[0][1],"b")
a1x.set_ylabel("Detected OD")
a1.text(0.1,0.9,"(1)",horizontalalignment='right',verticalalignment='bottom',transform=a1.transAxes)

a2 = subplot(222)
a2.plot(anums[1][0],anums[1][1],anums[1][2],anums[1][3],anums[1][4],anums[1][5])
a2.set_xlabel("Time [Hour]")
a2.set_ylabel("Growth (base 2) [Hour$^{-1}$]")
a2.text(0.1,0.9,"(2)",horizontalalignment='right',verticalalignment='bottom',transform=a2.transAxes)

a3 = subplot(223)
a3.plot(anums[2][0],anums[2][1],"g",anums[2][2],anums[2][3],"r")
a3.set_xlabel("Time [Hour]")
a3.set_ylabel("Protein accumulation rate (au)")
a3.text(0.1,0.9,"(3)",horizontalalignment='right',verticalalignment='bottom',transform=a3.transAxes)

a4 = subplot(224,sharex = a3)
a4.plot(anums[3][0],anums[3][1],"g",anums[3][2],anums[3][3],"r")
a4.set_xlabel("Time [Hour]")
a4.set_ylabel("Protein level (au)")
a4.text(0.1,0.9,"(4)",horizontalalignment='right',verticalalignment='bottom',transform=a4.transAxes)

show()
