import csv
import pandas as pd

def cria_arquivo():
    c = csv.writer(open("relatorio_desp.csv", "wb"))
    c.writerow(["Load","G1","G2","G3","Total","Corte"])

def escreve_no_arquivo(Load, G1, G2, G3, Total, Corte):
    c.writerow([str(Load),str(G1),str(G2),str(G3),str(Total),str(Corte)])
    
def faz_relatorio(Load, G1, G2, G3, Total, Corte):
    cria_arquivo()
    N = len(Load)
    for i in range(N):
        c = csv.writer(open("relatorio_desp.csv", "wb"))
        escreve_no_arquivo(Load[i], G1[i], G2[i], G3[i], sum(Total[i]), Corte[i])
        print('.')
    
    print('\n\nrelatorio finalizado...')
    
def cria_relatorio(Load, G1, G2, G3, Total, Corte):
    df = pd.DataFrame({
        'Load'  : Load,
        'G1'    : G1,
        'G2'    : G2,
        'G3'    : G3,
        'Total' : Total,
        'Corte' : Corte,
    })
    
    df.apply(lambda x: round(x['G1'], 0), axis = 1)
    df.apply(lambda x: round(x['G2'], 0), axis = 1)
    df.apply(lambda x: round(x['G3'], 0), axis = 1)
    df.apply(lambda x: round(x['Total'], 0), axis = 1)
    
    df.to_csv('relatorio_desp.csv')
    df.to_excel('relatorio_desp.xlsx')
    print('\n\nrelatorio pronto!!!')
    

