import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim
from subprocess import call

file_name_prefix = "graph3"
call(["ghc","fig3data"])
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
a1.plot(anums[0][0],anums[0][1],"ro",anums[0][2],anums[0][3],"go",anums[0][4],anums[0][5],"bo",anums[0][6],anums[0][7],"ko",anums[0][8],anums[0][9],"co",anums[0][10],anums[0][11],"mo",)
a1.set_xlabel("Growth rate (base 2) [Hour$^{-1}$]")
a1.set_ylabel("Protein accumulation rate (au)")
a1.text(0.1,0.9,"(1)",horizontalalignment='right',verticalalignment='bottom',transform=a1.transAxes)

a2 = subplot(122,sharex = a1)
a2.plot(anums[1][0],anums[1][1],"ro",anums[1][2],anums[1][3],"go",anums[1][4],anums[1][5],"bo",anums[1][6],anums[1][7],"ko",anums[1][8],anums[1][9],"co",anums[1][10],anums[1][11],"mo",)
a2.set_xlabel("Growth rate (base 2) [Hour$^{-1}$]")
a2.set_ylabel("Protein level (au)")
a2.text(0.1,0.9,"(2)",horizontalalignment='right',verticalalignment='bottom',transform=a2.transAxes)

show()
