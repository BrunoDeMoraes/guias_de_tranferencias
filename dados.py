import pandas as pd
from num2words import num2words

class Dados:

    #def
    def dados_de_pagamento(self):
        df = pd.read_excel("Matrix_2023_HRG.xlsx", skiprows=[0])
        filtro = df.loc[df['Nº DANFE'].notna() & df['Nº TED'].isna()]
        dados = filtro.filter(
            ['Cotação', 'Item', 'Empresa ', 'Nº DANFE', 'V. Total', 'Nº TED', 'Nº de processo SEI', 'Conta']
        )
        return dados

    def valor_por_extenso(self, itens_somados):
        for chave, valor in sorted(itens_somados.items()):
            extenso = num2words(valor[3], lang='pt_BR', to='currency')
            valor.append(extenso)

    def listar_pagamentos(self):
        pagamentos = self.dados_de_pagamento()
        duplicados = pagamentos[pagamentos.duplicated(subset=['Cotação', 'Empresa ', 'Nº DANFE'], keep=False)]
        itens_somados = {}
        checagem = []
        for indice, linha in duplicados.iterrows():
            palavra_checagem = str(linha['Cotação']) + '-' + str(linha['Empresa ']) + '-' + str(linha['Nº DANFE'])
            if palavra_checagem in checagem:
                continue
            else:
                checagem.append(palavra_checagem)
                duplicados_subset1 = duplicados[
                    (duplicados['Cotação'] == linha['Cotação']) &
                    (duplicados['Empresa '] == linha['Empresa ']) &
                    (duplicados['Nº DANFE'] == linha['Nº DANFE'])
                ]
                soma = duplicados_subset1['V. Total'].sum()
                descricao = palavra_checagem.split('-')
                itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], soma, linha['Nº de processo SEI'], linha['Conta']]
        for indice, linha in pagamentos.iterrows():
            palavra_checagem = str(linha['Cotação']) + '-' + str(linha['Empresa ']) + '-' + str(linha['Nº DANFE'])
            if palavra_checagem in checagem:
                continue
            else:
                checagem.append(palavra_checagem)
                descricao = palavra_checagem.split('-')
                itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], linha['V. Total'], linha['Nº de processo SEI'], linha['Conta']]
        self.valor_por_extenso(itens_somados)
        return itens_somados

    def fornecedores(self):
        df = pd.read_excel("Matrix_2023_HRG.xlsx", sheet_name='Fornecedores')
        empresas = {}
        for indice, linha in df.iterrows():
            a = linha.to_list()
            empresas[a[0]] = a[1:]
            #print(empresas)
        return empresas
