import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,legend
from subprocess import call

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
        t.label.set_fontsize(15)
    for t in a.xaxis.get_major_ticks():
        t.label.set_fontsize(15)

anums = []
for i in range(1,5):
    anums.append(ploti(i))

fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)
a1 = subplot(111)
ln1 = a1.plot(anums[0][2],anums[0][3],"g",label="YFP")
ln2 = a1.plot(anums[0][4],anums[0][5],"r",label="mCherry")
a1.set_ylabel("Detected Fluorescence",fontsize=20)
a1.set_title('E.Coli, M9, 0.2% Glu',fontsize=20)
set_ticks(a1)

a1x = a1.twinx()
ln3 = a1x.plot(anums[0][0],anums[0][1],"b",label="OD")
a1x.set_ylabel("Detected OD",fontsize=20)
set_ticks(a1x)

lns = ln1+ln2+ln3
legend(lns,[l.get_label() for l in lns],loc=0,prop={'size':20})

fig.savefig('FL1.png')

fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)
a2 = subplot(111)
a2.plot(anums[1][0],anums[1][1],anums[1][2],anums[1][3],anums[1][4],anums[1][5])
a2.set_xlabel("Time [Hour]",fontsize=20)
a2.set_ylabel("Doublings per hour [Hour$^{-1}$]",fontsize=20)
legend(('OD','YFP','mCherry'),prop={'size':20})
a2.set_title('E.Coli, M9, 0.2% Glu',fontsize=20)
set_ticks(a2)
fig.savefig('FL2.png')

fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)
a3 = subplot(111)
a3.plot(anums[2][0],anums[2][1],"g",anums[2][2],anums[2][3],"r")
a3.set_xlabel("Time [Hour]",fontsize=20)
a3.set_ylabel("Protein accumulation rate (au)",fontsize=20)
a3.text(18,17000, 'Protein accumulation rate=$\\frac{\\Delta fl}{\\int OD}$',fontsize=20)
legend(('YFP','mCherry'),prop={'size':20})
a3.set_title('E.Coli, M9, 0.2% Glu',fontsize=20)
set_ticks(a3)
fig.savefig('FL3.png')

fig = figure()
fig.set_size_inches(12,6)
fig.set_dpi(80)
a4 = subplot(111)
a4.plot(anums[3][0],anums[3][1],"g",anums[3][2],anums[3][3],"r")
a4.set_xlabel("Time [Hour]",fontsize=20)
a4.set_ylabel("Protein level (au)",fontsize=20)
a4.set_title('E.Coli, M9, 0.2% Glu',fontsize=20)
ylim(0,30000)
legend(('YFP','mCherry'),prop={'size':20})
set_ticks(a4)
fig.savefig('FL4.png')

fig = figure()
fig.set_size_inches(12,7)
fig.set_dpi(80)

a4 = subplot(211)
a4.plot(anums[3][0],anums[3][1],"g",anums[3][2],anums[3][3],"r")
a4.set_ylabel("Protein level (au)",fontsize=20)
a4.set_title('E.Coli, M9, 0.2% Glu',fontsize=20)
set_ticks(a4)
ylim(0,30000)

a3 = subplot(212)
a3.plot(anums[2][0],anums[2][1],"g",anums[2][2],anums[2][3],"r")
a3.set_xlabel("Time [Hour]",fontsize=20)
a3.set_ylabel("Protein Acc. rate (au)",fontsize=20)
legend(('YFP','mCherry'),prop={'size':20})
set_ticks(a3)

fig.savefig('FL5.png')
