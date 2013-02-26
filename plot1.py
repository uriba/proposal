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
a2 = subplot(222,sharey=a1, sharex = a1)
a2.plot(anums[1][0],anums[1][1])
a3 = subplot(223)
a3.plot(anums[2][0],anums[2][1])
a4 = subplot(224)
a4.plot(anums[3][0],anums[3][1])

show()
