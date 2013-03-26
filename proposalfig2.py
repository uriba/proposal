import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,xlim,legend
from subprocess import call
import numpy as np

axisfontsize = 8
ticksize = 6
annotation_size = 8
titlesize = 10
markersize=3

file_name_prefix = "graph3"
genes = [   (1,'PYK1 - pyruvate kinase'),
            (2,'HHF2 - core histone protein'),
            (3,'PAB1 - Poly(A) binding protein'),
            (4,'RPL8A - Ribosomal 60S protein'),
            (5,'CCW12 - Cell wall mannoprotein'),
            (6,'ACT1 - Actin'),
            (7,'CLN1 - G1 cyclin involved in regulation of the cell cycle')
        ]

def ploti(g,i):
    nums = []
    with open('%s%d%d.csv' % (file_name_prefix,g,i),'rb') as csvfile:
        vals = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in vals:
            nums.append(map(float,row))
    return nums

def set_ticks(a):
    for t in a.yaxis.get_major_ticks():
        t.label.set_fontsize(ticksize)
    for t in a.xaxis.get_major_ticks():
        t.label.set_fontsize(ticksize)

(gn,gd) = genes[2]
anums = []
for i in range(1,3):
    anums.append(ploti(gn,i))

fig = figure()
fig.subplots_adjust(left=0.2)
fig.suptitle('S.Cerevisiae\nPoly(A) binding protein' ,fontsize=titlesize)
fig.set_size_inches(2.5,5)
fig.set_dpi(80)

xs = []
ys = []
for i in range (0,len(anums[0])/2):
    xs.append(np.array(anums[0][2*i]))
    ys.append(np.array(anums[0][2*i+1])/1000)

x = np.concatenate(xs,axis=0)
y = np.concatenate(ys,axis=0)
squareslope = sum(x*x*y)/sum(x*x*x*x)
trendx = np.arange(0,1,0.05)
z=trendx*trendx*squareslope

a1 = subplot(211)
a1.plot(xs[0],ys[0],"ro",xs[1],ys[1],"go",xs[2],ys[2],"bo",xs[3],ys[3],"ko",xs[4],ys[4],"co",xs[5],ys[5],"mo",markersize=markersize)
a1.plot(trendx,z,"b--")
a1.annotate('$y=%.2fx^2$' % squareslope, xy=(0.45,0.45*0.45*squareslope),xytext=(0.1,0.5),fontsize=axisfontsize)
a1.set_xlabel("Growth rate [dbl/Hour]",fontsize = axisfontsize)
a1.set_ylabel("Protein accumulation rate (au)",fontsize = axisfontsize)
xlim(0,1)
a1.text(0.95,0.9,"(A)",horizontalalignment='right',verticalalignment='bottom',transform=a1.transAxes, fontsize=annotation_size)
set_ticks(a1)
legend(("Glu. with AA","Fruc. with AA","Glu. minus Ura", "Glu. minus AA","Gal with AA","Gal minus AA"),loc="upper left",prop={'size':ticksize},numpoints=1)

xs = []
ys = []
for i in range (0,len(anums[0])/2):
    xs.append(np.array(anums[1][2*i]))
    ys.append(np.array(anums[1][2*i+1])/1000)
x = np.concatenate(xs,axis=0)
y = np.concatenate(ys,axis=0)

slope = sum(x*y)/sum(x*x)
z=trendx*slope

a2 = subplot(212)
a2.plot(xs[0],ys[0],"ro",xs[1],ys[1],"go",xs[2],ys[2],"bo",xs[3],ys[3],"ko",xs[4],ys[4],"co",xs[5],ys[5],"mo",markersize=markersize)
a2.plot(trendx,z,"b--")
a2.annotate('$y=%.2fx$' % slope, xy=(0.2,0.2*slope),xytext=(0.1,0.8),fontsize=axisfontsize)
a2.set_xlabel("Growth rate [dbl/Hour]",fontsize = axisfontsize)
a2.set_ylabel("Protein level (au)",fontsize = axisfontsize)
xlim(0,1)
a2.text(0.95,0.9,"(B)",horizontalalignment='right',verticalalignment='bottom',transform=a2.transAxes, fontsize=annotation_size)
set_ticks(a2)
# fig.tight_layout()
fig.savefig('propfig2.pdf')
