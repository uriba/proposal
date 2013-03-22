import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,legend,xlim,axvspan
from subprocess import call
import numpy as np

axisfontsize = 8
ticksize = 6
annotation_size = 8
file_name_prefix = "graph2"
def ploti(i):
    nums = []
    with open('%s%d.csv' % (file_name_prefix,i),'rb') as csvfile:
        vals = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in vals:
            nums.append(map(float,row))
    return nums

def set_ticks(a):
    for t in a.yaxis.get_major_ticks():
        t.label.set_fontsize(ticksize)
    for t in a.xaxis.get_major_ticks():
        t.label.set_fontsize(ticksize)

anums = []
for i in range(1,5):
    anums.append(ploti(i))

fig = figure()
fig.set_size_inches(5,4)
fig.set_dpi(80)

a = subplot(311)
x = np.array(anums[1][0])
y = np.array(anums[1][1])
a.plot(x,y,marker='.',linestyle='-')
a.set_ylabel("Growth rate [dbl/Hour]",fontsize=axisfontsize)
a.set_title('E.Coli, M9, 0.2% Glu',fontsize=axisfontsize)
set_ticks(a)
ylim(0,0.7)
xlim(15,25)
a.fill_between(x,y, where=(x>=18) & (x<=19.5), facecolor='c',alpha=0.5)
a.text(18.3,0.3, "Maximal\ngrowth\n$g_{max}\\approx0.6$", fontsize=ticksize)
a.fill_between(x,y, where=(x>=19.5) & (x<=22.5), facecolor='m',alpha=0.5)
a.text(20.3,0.3, "Transition", fontsize=ticksize)
a.fill_between(x,y, where=(x>=22.5) & (x<=24), facecolor='b',alpha=0.5)
a.text(22.8,0.1, "Slow\ngrowth\n$g_{slow}\\approx0.4$", fontsize=ticksize)
a.text(0.05,0.85,"(A)",horizontalalignment='right',verticalalignment='bottom',transform=a.transAxes, fontsize=annotation_size)

a1 = subplot(312)
x1 = np.array(anums[3][0])
y1 = np.array(anums[3][1])/1000
x2 = np.array(anums[3][2])
y2 = np.array(anums[3][3])/1000
a1.plot(x1,y1,"g",x2,y2,"r",marker='.',linestyle='-')
a1.set_ylabel("Protein level\nper OD (au)",fontsize=axisfontsize)
set_ticks(a1)
ylim(0,30)
xlim(15,25)
a1.fill_between(x1,y1, where=(x1>=18) & (x1<=19.5), facecolor='c',alpha=0.5)
a1.text(18.3,15, "High\nlevel\n$P_{YFP}^{h}\\approx27$", fontsize=ticksize)
a1.text(18.2,7, "$P_{mCh}^{h}\\approx14$", fontsize=ticksize)
a1.fill_between(x1,y1, where=(x1>=19.5) & (x1<=22.5), facecolor='m',alpha=0.5)
a1.text(20.3,15, "Transition", fontsize=ticksize)
a1.fill_between(x1,y1, where=(x1>=22.5) & (x1<=24), facecolor='b',alpha=0.5)
a1.text(22.6,10, "Low\nlevel\n$P_{YFP}^{l}\\approx19$", fontsize=ticksize)
a1.text(22.6,3, "$P_{mCh}^{l}\\approx9$", fontsize=ticksize)
a1.text(0.05,0.85,"(B)",horizontalalignment='right',verticalalignment='bottom',transform=a1.transAxes, fontsize=annotation_size)

a2 = subplot(313)
x1 = np.array(anums[2][0])
y1 = np.array(anums[2][1])/1000
x2 = np.array(anums[2][2])
y2 = np.array(anums[2][3])/1000
a2.plot(x1,y1,"g",x2,y2,"r",marker='.',linestyle='-')
a2.set_xlabel("Time [Hour]",fontsize=axisfontsize)
a2.set_ylabel("Protein Acc. rate\nper OD (au)",fontsize=axisfontsize)
legend(('YFP','mCherry'),prop={'size':ticksize})
xlim(15,25)
ylim(0,50)
set_ticks(a2)
a2.fill_between(x1,y1, where=(x1>=16.5) & (x1<=18), facecolor='c',alpha=0.5)
a2.text(16.65,22, "High\nactivity\n$A_{YFP}^{h}\\approx40$", fontsize=ticksize)
a2.text(16.65,10, "$A_{mCh}^{h}\\approx20$", fontsize=ticksize)
a2.fill_between(x1,y1, where=(x1>=18) & (x1<=21), facecolor='m',alpha=0.5)
a2.text(18.8,20, "Transition", fontsize=ticksize)
a2.fill_between(x1,y1, where=(x1>=21) & (x1<=22.5), facecolor='b',alpha=0.5)
a2.text(21.2,20, "Low activity", fontsize=ticksize)
a2.text(21.3,11, "$A_{YFP}^{l}\\approx18$", fontsize=ticksize)
a2.text(21.3,2, "$A_{mCh}^{l}\\approx8$", fontsize=ticksize)
a2.text(0.05,0.85,"(C)",horizontalalignment='right',verticalalignment='bottom',transform=a2.transAxes, fontsize=annotation_size)

fig.savefig('propfig1.pdf')
