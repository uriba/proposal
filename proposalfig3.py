import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,xlim,legend,tight_layout
from subprocess import call
import numpy as np

axisfontsize = 6
ticksize = 5
annotation_size = 6
titlesize = 10
markersize=3

file_name_prefix = "graph3"
genes = [   (0,0,'PYK1 - pyruvate kinase'),
            (5,1,'HHF2 - core histone protein'),
        #    (2,'PAB1 - Poly(A) binding protein'),
            (1,2,'RPL8A - Ribosomal 60S protein'),
            (3,3,'CCW12 - Cell wall mannoprotein'),
            (4,4,'ACT1 - Actin'),
            (2,5,'CLN1 - G1 cyclin')
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

fig = figure()
fig.subplots_adjust(right=0.83,top=0.95,wspace=0.30,hspace=0.8)
fig.set_size_inches(5,7)
fig.set_dpi(80)

for (loc,gn,gd) in genes:
    anums = []
    for i in range(1,3):
        anums.append(ploti(gn+1,i))

    fig.text(0.5,0.98-(float(loc)*0.92/6),gd,horizontalalignment='center',verticalalignment='top',fontsize = titlesize)
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

    a1 = subplot(6,2,2*loc+1)
    a1.plot(xs[0],ys[0],"ro",xs[1],ys[1],"go",xs[2],ys[2],"bo",xs[3],ys[3],"ko",xs[4],ys[4],"co",xs[5],ys[5],"mo",markersize=markersize)
    a1.plot(trendx,z,"b--")
    a1.text(0.1,0.6,'$y=%.2fx^2$' % squareslope,fontsize=axisfontsize,transform=a1.transAxes)
    a1.set_xlabel("Growth rate [dbl/Hour]",fontsize = axisfontsize)
    a1.set_ylabel("Prot. acc. rate [au]",fontsize = axisfontsize)
    xlim(0,1)
    set_ticks(a1)

    xs = []
    ys = []
    for i in range (0,len(anums[0])/2):
        xs.append(np.array(anums[1][2*i]))
        ys.append(np.array(anums[1][2*i+1])/1000)
    x = np.concatenate(xs,axis=0)
    y = np.concatenate(ys,axis=0)

    slope = sum(x*y)/sum(x*x)
    z=trendx*slope

    a2 = subplot(6,2,2*loc+2)
    a2.plot(xs[0],ys[0],"ro",xs[1],ys[1],"go",xs[2],ys[2],"bo",xs[3],ys[3],"ko",xs[4],ys[4],"co",xs[5],ys[5],"mo",markersize=markersize)
    a2.plot(trendx,z,"b--")
    a2.text(0.1,0.7,'$y=%.2fx$' % slope,fontsize=axisfontsize,transform=a2.transAxes)
    a2.set_xlabel("Growth rate [dbl/Hour]",fontsize = axisfontsize)
    a2.set_ylabel("Prot. level [au]",fontsize = axisfontsize)
    xlim(0,1)
    if loc==0:
        legend(("Glu. with AA","Fruc. with AA","Glu. minus Ura", "Glu. minus AA","Gal with AA","Gal minus AA"),loc="center left",prop={'size':ticksize},numpoints=1,bbox_to_anchor=(1,0.5))
    set_ticks(a2)

fig.savefig('propfig3.pdf')
