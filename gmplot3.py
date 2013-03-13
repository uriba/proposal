import csv
from matplotlib.pyplot import plot,show,figure,subplot,ylim,xlim,legend
from subprocess import call

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
        t.label.set_fontsize(15)
    for t in a.xaxis.get_major_ticks():
        t.label.set_fontsize(15)

for (gn,gd) in genes:
    anums = []
    for i in range(1,3):
        anums.append(ploti(gn,i))

    fig = figure()
    fig.set_size_inches(12,7)
    fig.set_dpi(80)
    a1 = subplot(111)
    a1.plot(anums[0][0],anums[0][1],"ro",anums[0][2],anums[0][3],"go",anums[0][4],anums[0][5],"bo",anums[0][6],anums[0][7],"ko",anums[0][8],anums[0][9],"co",anums[0][10],anums[0][11],"mo",)
    a1.set_xlabel("Doublings per hour [Hour$^{-1}$]",fontsize = 20)
    a1.set_ylabel("Protein accumulation rate (au)",fontsize = 20)
    xlim(0,1)
    legend(("Glu. with AA","Fruc. with AA","Glu. minus Ura", "Glu. minus AA","Gal with AA","Gal minus AA"),loc="upper left",prop={'size':20})
    a1.set_title('S.Cerevisiae, %s' % gd,fontsize=20)
    set_ticks(a1)
    fig.savefig('Cor%d1.png' % gn)

    fig = figure()
    fig.set_size_inches(12,7)
    fig.set_dpi(80)
    a2 = subplot(111)
    a2.plot(anums[1][0],anums[1][1],"ro",anums[1][2],anums[1][3],"go",anums[1][4],anums[1][5],"bo",anums[1][6],anums[1][7],"ko",anums[1][8],anums[1][9],"co",anums[1][10],anums[1][11],"mo",)
    a2.set_xlabel("Doublings per hour [Hour$^{-1}$]",fontsize = 20)
    a2.set_ylabel("Protein level (au)",fontsize = 20)
    xlim(0,1)
    legend(("Glu. with AA","Fruc. with AA","Glu. minus Ura", "Glu. minus AA","Gal with AA","Gal minus AA"),loc="upper left",prop={'size':20})
    a2.set_title('S.Cerevisiae, %s' % gd,fontsize=20)
    set_ticks(a2)
    fig.savefig('Cor%d2.png' % gn)
