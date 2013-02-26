import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim
from subprocess import call

file_name_prefix = "graph3"
call(["rm","fig3data"])
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
a1 = subplot(211)
a1.plot(anums[0][0],anums[0][1],"ro")
a2 = subplot(212)
a2.plot(anums[1][0],anums[1][1],"ro")

show()
