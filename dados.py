import pandas as pd

def dados_de_pagamento():
    df = pd.read_excel("Matrix_2023_HRG.xlsx", skiprows=[0])
    filtro = df.loc[df['Nº DANFE'].notna() & df['Nº TED'].isna()]
    novo = filtro.filter(['Cotação', 'Empresa ', 'Nº DANFE', 'Nº TED'])
    return novo

def fornecedores():
    df = pd.read_excel("Matrix_2023_HRG.xlsx", sheet_name='Fornecedores')
    linhas = {}
    for indice, linha in df.iterrows():
        a = linha.to_list()
        linhas[a[0]] = a[1:]
    return linhas

def separador(dados, fornecedores):
    for indice, linha in dados.iterrows():
        a = linha.to_list()
        if fornecedores[a[1]][5] == "BRB":
            print(f"{a[1]} - tranferência")
        else:
            print(f"{a[1]} - TED")

dados = dados_de_pagamento()
fornecedores = fornecedores()
separador(dados, fornecedores)
