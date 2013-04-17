import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,legend,xlim,axvspan,tight_layout
from subprocess import call
import numpy as np

axisfontsize = 20
ticksize = 15
file_name_prefix = "graph2"
initcutoff = 53 
activityoffset = 10
markersize = 5
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
fig.set_size_inches(12,6)
fig.set_dpi(80)

x = np.array(anums[1][0])
y = np.array(anums[1][1])
x1 = np.array(anums[3][0])
y1 = np.array(anums[3][1])/1000
x2 = np.array(anums[3][2])
y2 = np.array(anums[3][3])/1000

a = subplot(111)
a.set_title('E.Coli, M9, 0.2% Glu',fontsize=axisfontsize)

a = subplot(111)
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

lns = ln1+ln2+ln3
legend(lns,[l.get_label() for l in lns],prop={'size':axisfontsize},loc="center left")
set_ticks(ax)

fig.savefig('proppres1.png')
#####################################
fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)

b = subplot(111)
b.plot(x[initcutoff:],y[initcutoff:],"b.",markersize=markersize)
b.set_xlabel("Time [Hour]",fontsize=axisfontsize)
b.set_ylabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
ylim(0,0.8)
set_ticks(b)
fig.savefig('proppres2.png')
#####################################
fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)

a1 = subplot(111)
a1.plot(y[initcutoff:],y1[initcutoff:],"g.",y[initcutoff:],y2[initcutoff:],"r.",markersize=markersize)
a1.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a1.set_ylabel("Protein level per OD [au]",fontsize=axisfontsize)
set_ticks(a1)
xlim(0,0.8)
ylim(0,35)
fig.savefig('proppres3.png')
#####################################
fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)

a2 = subplot(111)
x3 = np.array(anums[2][0])
y3 = np.array(anums[2][1])/1000
x4 = np.array(anums[2][2])
y4 = np.array(anums[2][3])/1000
a2.plot(y[initcutoff:],y3[initcutoff-activityoffset:-activityoffset],"g.",
        y[initcutoff:],y4[initcutoff - activityoffset:- activityoffset],"r.",markersize=markersize)
a2.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a2.set_ylabel("Protein acc. rate\nper OD [au]",fontsize=axisfontsize)
# legend(('YFP','mCherry'),prop={'size':ticksize})
xlim(0,0.8)
ylim(0,50)
set_ticks(a2)
fig.savefig('proppres4.png')
#####################################
fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)

trendx1 = np.arange(0,0.45,0.05)
trendx2 = np.arange(0.65,1,0.05)

a3 = subplot(111)
a3.plot(y[initcutoff:],y1[initcutoff:]/y[initcutoff:],"g.",y[initcutoff:],y2[initcutoff:]/y[initcutoff:],"r.",markersize=markersize)

consty1=np.zeros(len(trendx1),dtype=float)
consty2=np.zeros(len(trendx2),dtype=float)

a3.plot(trendx1,consty1+20,color='black',linewidth=1,alpha=0.5,linestyle='--')
a3.plot(trendx2,consty2+20,color='black',linewidth=1,alpha=0.5,linestyle='--')
a3.plot(trendx1,consty1+46.5,color='black',linewidth=1,alpha=0.5,linestyle='--')
a3.plot(trendx2,consty2+46.5,color='black',linewidth=1,alpha=0.5,linestyle='--')
a3.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a3.set_ylabel(r"$ \frac{\mathdefault{Protein\/level\/per\/OD}}{\mathdefault{Growth\/rate}} $ [au]",fontsize=axisfontsize)
xlim(0,0.8)
ylim(0,60)
set_ticks(a3)
fig.savefig('proppres5.png')
#####################################
fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)

a4 = subplot(111)
a4.plot(y[initcutoff:],y3[initcutoff - activityoffset:-activityoffset]/(y[initcutoff:]*y[initcutoff:]),"g.",
        y[initcutoff:],y4[initcutoff - activityoffset:-activityoffset]/(y[initcutoff:]*y[initcutoff:]),"r.",markersize=markersize)
a4.plot(trendx1,consty1+45,color='black',linewidth=1,alpha=0.5,linestyle='--')
a4.plot(trendx2,consty2+45,color='black',linewidth=1,alpha=0.5,linestyle='--')
a4.plot(trendx1,consty1+100,color='black',linewidth=1,alpha=0.5,linestyle='--')
a4.plot(trendx2,consty2+100,color='black',linewidth=1,alpha=0.5,linestyle='--')
a4.set_xlabel("Growth rate [Dbl/Hour]",fontsize=axisfontsize)
a4.set_ylabel(r"$ \frac{\mathdefault{Protein\/acc.\/rate\/per\/OD}}{\mathdefault{Growth\/rate}^2} $ [au]",fontsize=axisfontsize)
xlim(0,0.8)
ylim(0,160)
set_ticks(a4)
fig.savefig('proppres6.png')
######################################
fig = figure()
fig.set_size_inches(20,12)
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

fig.savefig('proppres_add.png')
##################################
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

(gn,gd) = genes[2]
anums = []
for i in range(1,3):
    anums.append(ploti(gn,i))

fig = figure()
fig.set_size_inches(12,6)
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

a1 = subplot(111)
a1.plot(xs[0],ys[0],"ro",xs[1],ys[1],"go",xs[2],ys[2],"bo",xs[3],ys[3],"ko",xs[4],ys[4],"co",xs[5],ys[5],"mo",markersize=markersize)
a1.plot(trendx,z,"b--")
a1.annotate('$y=%.2fx^2$' % squareslope, xy=(0.45,0.45*0.45*squareslope),xytext=(0.1,0.5),fontsize=axisfontsize)
a1.set_xlabel("Growth rate [dbl/Hour]",fontsize = axisfontsize)
a1.set_ylabel("Protein accumulation rate [au]",fontsize = axisfontsize)
xlim(0,1)
set_ticks(a1)
a1.set_title('S.Cerevisiae\nPoly(A) binding protein' ,fontsize=axisfontsize)
legend(("Glu. with AA","Fruc. with AA","Glu. minus Ura", "Glu. minus AA","Gal with AA","Gal minus AA"),loc="upper left",prop={'size':ticksize},numpoints=1)
fig.savefig('proppres7.png')
#########################################
fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)

xs = []
ys = []
for i in range (0,len(anums[0])/2):
    xs.append(np.array(anums[1][2*i]))
    ys.append(np.array(anums[1][2*i+1])/1000)
x = np.concatenate(xs,axis=0)
y = np.concatenate(ys,axis=0)

slope = sum(x*y)/sum(x*x)
z=trendx*slope

a2 = subplot(111)
a2.plot(xs[0],ys[0],"ro",xs[1],ys[1],"go",xs[2],ys[2],"bo",xs[3],ys[3],"ko",xs[4],ys[4],"co",xs[5],ys[5],"mo",markersize=markersize)
a2.plot(trendx,z,"b--")
a2.annotate('$y=%.2fx$' % slope, xy=(0.2,0.2*slope),xytext=(0.1,0.8),fontsize=axisfontsize)
a2.set_xlabel("Growth rate [dbl/Hour]",fontsize = axisfontsize)
a2.set_ylabel("Protein level [au]",fontsize = axisfontsize)
xlim(0,1)
set_ticks(a2)
legend(("Glu. with AA","Fruc. with AA","Glu. minus Ura", "Glu. minus AA","Gal with AA","Gal minus AA"),loc="upper left",prop={'size':ticksize},numpoints=1)
a2.set_title('S.Cerevisiae\nPoly(A) binding protein' ,fontsize=axisfontsize)
fig.savefig('proppres8.png')
