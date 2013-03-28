import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,legend,xlim,axvspan,tight_layout
from subprocess import call
import numpy as np

axisfontsize = 6
ticksize = 5
annotation_size = 8
file_name_prefix = "graph2"
initcutoff = 53 
activityoffset = 10
def ploti(i):
    nums = []
    with open('%s%d.csv' % (file_name_prefix,i),'rb') as csvfile:
        vals = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in vals:
            nums.append(map(float,row))
    return nums

def set_ticks(p):
    for t in p.yaxis.get_major_ticks():
        t.label.set_fontsize(ticksize)
        t.label2.set_fontsize(ticksize)
    for t in p.xaxis.get_major_ticks():
        t.label.set_fontsize(ticksize)

anums = []
for i in range(1,5):
    anums.append(ploti(i))

fig = figure()
fig.set_size_inches(5,4.7)
fig.set_dpi(80)

x = np.array(anums[1][0])
y = np.array(anums[1][1])
x1 = np.array(anums[3][0])
y1 = np.array(anums[3][1])/1000
x2 = np.array(anums[3][2])
y2 = np.array(anums[3][3])/1000

fig.subplots_adjust(right=0.9,wspace=0.45,hspace=0.32,top=0.95,bottom=0.1)
a = subplot(311)
a.set_title('E.Coli, M9, 0.2% Glu',fontsize=axisfontsize)

a = subplot(321)
fl1 = np.array(anums[0][3])/1000
fl2 = np.array(anums[0][5])/1000
ln1 = a.plot(anums[0][2],fl1,"g",label="YFP")
ln2 = a.plot(anums[0][4],fl2,"r",label="mCherry")
a.set_ylabel("Fluorescence [au]",fontsize=axisfontsize)
set_ticks(a)
ylim(0,10)

ax = a.twinx()
ln3 = ax.plot(anums[0][0],anums[0][1],"b",label="OD")
ax.set_ylabel("OD",fontsize=axisfontsize)
a.set_xlabel("Time [Hour]",fontsize=axisfontsize)
a.text(0.1,0.9,"(A)",horizontalalignment='right',verticalalignment='bottom',transform=a.transAxes, fontsize=annotation_size)

lns = ln1+ln2+ln3
legend(lns,[l.get_label() for l in lns],prop={'size':axisfontsize},loc="center left")
set_ticks(ax)

b = subplot(322)
b.plot(x[initcutoff:],y[initcutoff:],"b.",markersize=2)
b.set_xlabel("Time [Hour]",fontsize=axisfontsize)
b.set_ylabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
ylim(0,0.8)
set_ticks(b)
b.text(0.1,0.9,"(B)",horizontalalignment='right',verticalalignment='bottom',transform=b.transAxes, fontsize=annotation_size)

a1 = subplot(323)
a1.plot(y[initcutoff:],y1[initcutoff:],"g.",y[initcutoff:],y2[initcutoff:],"r.",markersize=2)
a1.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a1.set_ylabel("Protein level per OD [au]",fontsize=axisfontsize)
set_ticks(a1)
a1.text(0.1,0.9,"(C)",horizontalalignment='right',verticalalignment='bottom',transform=a1.transAxes, fontsize=annotation_size)
xlim(0,0.8)
ylim(0,35)

a2 = subplot(324)
x3 = np.array(anums[2][0])
y3 = np.array(anums[2][1])/1000
x4 = np.array(anums[2][2])
y4 = np.array(anums[2][3])/1000
a2.plot(y[initcutoff:],y3[initcutoff-activityoffset:-activityoffset],"g.",
        y[initcutoff:],y4[initcutoff - activityoffset:- activityoffset],"r.",markersize=2)
a2.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a2.set_ylabel("Protein acc. rate\nper OD [au]",fontsize=axisfontsize)
# legend(('YFP','mCherry'),prop={'size':ticksize})
xlim(0,0.8)
ylim(0,50)
a2.text(0.1,0.9,"(D)",horizontalalignment='right',verticalalignment='bottom',transform=a2.transAxes, fontsize=annotation_size)
set_ticks(a2)

trendx = np.arange(0,1,0.05)
a3 = subplot(325)
a3.plot(y[initcutoff:],y1[initcutoff:]/y[initcutoff:],"g.",y[initcutoff:],y2[initcutoff:]/y[initcutoff:],"r.",markersize=2)

consty=np.zeros(len(trendx),dtype=float)

a3.plot(trendx,consty+20,color='black',linewidth=1,alpha=0.5,linestyle='--')
a3.plot(trendx,consty+46.5,color='black',linewidth=1,alpha=0.5,linestyle='--')
a3.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a3.set_ylabel(r"$ \frac{\mathdefault{Protein\/level\/per\/OD}}{\mathdefault{Growth\/rate}} $ [au]",fontsize=axisfontsize)
xlim(0,0.8)
ylim(0,60)
a3.text(0.1,0.9,"(E)",horizontalalignment='right',verticalalignment='bottom',transform=a3.transAxes, fontsize=annotation_size)
set_ticks(a3)

a4 = subplot(326)
a4.plot(y[initcutoff:],y3[initcutoff - activityoffset:-activityoffset]/(y[initcutoff:]*y[initcutoff:]),"g.",
        y[initcutoff:],y4[initcutoff - activityoffset:-activityoffset]/(y[initcutoff:]*y[initcutoff:]),"r.",markersize=2)
a4.plot(trendx,consty+45,color='black',linewidth=1,alpha=0.5,linestyle='--')
a4.plot(trendx,consty+100,color='black',linewidth=1,alpha=0.5,linestyle='--')
a4.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a4.set_ylabel(r"$ \frac{\mathdefault{Protein\/acc.\/rate\/per\/OD}}{\mathdefault{Growth\/rate}^2} $ [au]",fontsize=axisfontsize)
xlim(0,0.8)
ylim(0,160)
a4.text(0.1,0.9,"(F)",horizontalalignment='right',verticalalignment='bottom',transform=a4.transAxes, fontsize=annotation_size)
set_ticks(a4)

fig.savefig('propfig1_alt.pdf')
