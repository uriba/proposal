import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim
from subprocess import call

def ploti(i):
    nums = []
    with open('test%d.csv' % i,'rb') as csvfile:
        vals = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in vals:
            nums.append(map(float,row))
    return nums

fig = figure()
anums = []
for i in range(1,3):
    anums.append(ploti(i))
a1 = subplot(211)
a1.plot(anums[0][0],anums[0][1],anums[0][2],anums[0][3],anums[0][4],anums[0][5],anums[0][6],anums[0][7],anums[0][8],anums[0][9],anums[0][10],anums[0][11],)
a2 = subplot(212)
a2.plot(anums[1][0],anums[1][1],anums[1][2],anums[1][3],anums[1][4],anums[1][5],anums[1][6],anums[1][7],anums[1][8],anums[1][9],anums[1][10],anums[1][11],)

show()
