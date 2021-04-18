from despacho import *
from relatorio import *


data = np.array([   [1,510,7.2,0.00142,0.9,150,600,175,45],
                    [2,310,7.85,0.00194,1.0,100,400,80,80],
                    [3,78,7.97,0.00482,1.0,50,200,45,15  ]])


N = 24
#Load = gera_demanda(300,1200,N, ale=True)
Load = [355,480,650,758,791,885,899,1005,955,
        814,920,1187,1037,1195,1148,1051,933,
        761,703,645,390,322,379,394]
ups = []
dws = []
DE = []
Pg = []
L  = []
tt = []

fde = desp(Load[0], data[:,0],data[:,1], data[:,2], data[:,3], data[:,4], data[:,5], data[:,6])
DE.append(fde)
tt.append(0)
Pg.append(fde[:-1])

for t in range(1,N):
    fde = despacho(Load[t], fde[:-1], data)
    Pg.append(fde[:-1])
    L.append(fde[-1])
    tt.append(t)

view_1(Load)
view_2(Load, Pg)

corte = [np.round(abs(Load[i]-sum(Pg[i]))) for i in range(24)]
print(corte)

g1      = [(Pg[i])[0] for i in range(len(Pg))]
g2      = [(Pg[i])[1] for i in range(len(Pg))]
g3      = [(Pg[i])[2] for i in range(len(Pg))]
total   = [sum(Pg[i]) for i in range(len(Pg))]

cria_relatorio(Load,g1,g2,g3,total,corte)


