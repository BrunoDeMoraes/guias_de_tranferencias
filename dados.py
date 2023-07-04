import pandas as pd

def dados_de_pagamento():
    df = pd.read_excel("Matrix_2023_HRG.xlsx", skiprows=[0])
    print(df.columns)
    filtro = df.loc[df['Nº DANFE'].notna() & df['Nº TED'].isna()]
    novo = filtro.filter(['Cotação', 'Empresa ', 'Nº DANFE', 'V. Total', 'Nº TED'])
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

def valor_de_pagamento(dados):
    duplicados = dados[dados.duplicated(subset=dados.columns.drop('V. Total'), keep=False)]
    print(duplicados)
    checagem = []
    itens_somados = {}
    for indice, linha in duplicados.iterrows():
        palavra_checagem = str(linha['Cotação']) + str(linha['Empresa ']) + str(linha['Nº DANFE'])
        if palavra_checagem in checagem:
            continue
        else:
            checagem.append(palavra_checagem)
            print(palavra_checagem)
            duplicados_subset1 = duplicados[duplicados['Cotação'] == linha['Cotação']]
            duplicados_subset2 = duplicados_subset1[duplicados_subset1['Empresa '] == linha['Empresa ']]
            duplicados_subset3 = duplicados_subset2[duplicados_subset2['Nº DANFE'] == linha['Nº DANFE']]
            print(duplicados_subset3)
            soma = duplicados_subset3['V. Total'].sum()
            print(f'Soma dos itens da NF R$ {soma}')
            itens_somados[palavra_checagem] = soma
    print(checagem)
    print(itens_somados)




dados = dados_de_pagamento()
print(dados)
fornecedores = fornecedores()
separador(dados, fornecedores)
valor_de_pagamento(dados)