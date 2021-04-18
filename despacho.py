import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def gera_demanda(n_min, n_max, n=10, ale=True):
    if (ale):
        return np.random.randint(n_min, n_max, n)
    else:
        return np.linspace(n_min, n_max, n)


def desp(Pd, u, a, b, g, cst, pmin, pmax):
    Load = np.float(Pd)
    ng = len(u)
    a = np.multiply(a, cst)  # alpha[i] * custo[i]
    b = np.multiply(b, cst)  # beta[i] * custo[i]
    g = np.multiply(g, cst)  # gamma[i] * custo[i]
    Pg = []
    Lambda = max(b)  # maior custo
    
    iter=0 
    while abs(Load) > 0.0001 and iter<1000:
        Pg = np.divide((Lambda - b) / 2, g)
        Pg = np.minimum(Pg, pmax)
        Pg = np.maximum(Pg, pmin)
        Load = Pd - np.sum(Pg)
        Lambda = Lambda + ((Load * 2) / (np.sum(np.divide(1, g))))
        iter+=1

    cc = np.add(a, np.multiply(b, Pg) + np.multiply(g, Pg * Pg))
    total_cc = np.sum(cc)
    res = [pg for pg in Pg]
    res.append(Lambda)
    return np.array(res)


def despacho(Pd, Pg0, data):
    Load = Pd
    u = data[:, 0]
    a = data[:, 1]
    b = data[:, 2]
    g = data[:, 3]
    cst = data[:, 4]
    pmin = data[:, 5]
    pmax = data[:, 6]
    ur = data[:,7]
    dr = data[:,8]
    ng = len(u)
    corte = 0
    
    p_low = np.maximum(pmin, np.add(Pg0, -dr))
    p_high = np.minimum(pmax, np.add(Pg0, ur))
    
    print('low: ', p_low)
    
    
    if Pd > sum(Pg0):  # aceleração
        pmax = p_high
    elif Pd < sum(Pg0):  # desaceleração
        pmax = p_low
    else:
        return desp(Load, u, a, b, g, cst, pmin, pmax)

    
    

    if (Load - sum(pmax)) > 1:
        corte = Load - sum(pmax)
    else:
        if (Load - sum(pmin)) < 1:
            corte = Load
    print('corte: ', corte, ' (MW)')

    Load = Load - corte

    res = desp(Load, u, a, b, g, cst, pmin, pmax)
    return np.array(res)


def view_1(Load):
    plt.figure(figsize=(15, 5))
    t = np.arange(24)
    ups = [i for i in range(1,len(t)) if Load[i]>Load[i-1]]
    dws = [i for i in range(1,len(t)) if Load[i]<Load[i-1]]

    print(ups)

    plt.bar(ups, [Load[t] for t in ups],color='b')
    plt.bar(dws, [Load[t] for t in dws],color='r')

    plt.savefig('grafico_demanda.png', transparent=True)
    plt.show()

def view_2(Load, Pg):
    t = np.arange(24)
    ger = [sum(Pg[i]) for i in range(len(Pg))]
    g1  = [(Pg[i])[0] for i in range(len(Pg))]
    g2  = [(Pg[i])[1] for i in range(len(Pg))]
    g3  = [(Pg[i])[2] for i in range(len(Pg))]

    print(g1)
    
    for i in range(len(Load)):
        print(f'Pd: {Load[i]} -> {ger[i]}')

    plt.bar(t, Load, color='blue',label='Demanda')
    plt.bar(t, ger, color='green',label='Geração')
    plt.bar(t, np.add(g1,np.add(g2,g3)), color='red',label='G1')
    plt.bar(t, np.add(g2,g3), color='orange',label='G2')
    plt.bar(t, g3, color='yellow',label='G3')
    df = pd.DataFrame({
        'Geração': ger,
        'Demanda': Load,
    })

    df.plot.bar()

    df2 = pd.DataFrame({
        'PL': Load,
        'G1': g1,
        'G2': g2,
        'G3': g3,
    })

    df2.plot.bar()



    plt.title('Demanda vs Geração (Corte)')
    plt.legend(loc='upper right')
    plt.savefig('PdxG.png', transparent=True)
    plt.show()