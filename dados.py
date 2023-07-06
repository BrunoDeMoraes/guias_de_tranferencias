import pandas as pd

class Dados():
    def dados_de_pagamento(self):
        df = pd.read_excel("Matrix_2023_HRG.xlsx", skiprows=[0])
        print(df.columns)
        filtro = df.loc[df['Nº DANFE'].notna() & df['Nº TED'].isna()]
        self.pagamentos = filtro.filter(
            ['Cotação', 'Empresa ', 'Nº DANFE', 'V. Total', 'Nº TED']
        )
        print(self.pagamentos)

    def valor_de_pagamento(self):
        duplicados = self.pagamentos[self.pagamentos.duplicated(subset=self.pagamentos.columns.drop('V. Total'), keep=False)]
        print(duplicados)
        checagem = []
        itens_somados = {}
        for indice, linha in duplicados.iterrows():
            palavra_checagem = str(linha['Cotação']) + '-' + str(linha['Empresa ']) + '-' + str(linha['Nº DANFE'])
            if palavra_checagem in checagem:
                continue
            else:
                checagem.append(palavra_checagem)
                print(palavra_checagem)
                duplicados_subset1 = duplicados[
                    (duplicados['Cotação'] == linha['Cotação']) &
                    (duplicados['Empresa '] == linha['Empresa ']) &
                    (duplicados['Nº DANFE'] == linha['Nº DANFE'])
                ]
                print(duplicados_subset1)
                soma = duplicados_subset1['V. Total'].sum()
                print(f'Soma dos itens da NF R$ {soma}')
                descricao = palavra_checagem.split('-')
                itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], soma]
        for indice, linha in self.pagamentos.iterrows():
            palavra_checagem = str(linha['Cotação']) + '-' + str(linha['Empresa ']) + '-' + str(linha['Nº DANFE'])
            if palavra_checagem in checagem:
                continue
            else:
                checagem.append(palavra_checagem)
                print(palavra_checagem)
                descricao = palavra_checagem.split('-')
                itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], linha['V. Total']]
        print(checagem)
        for chave, valor in sorted(itens_somados.items()):
            print(f'{chave} - {valor}')
        return itens_somados

    def fornecedores(self):
        df = pd.read_excel("Matrix_2023_HRG.xlsx", sheet_name='Fornecedores')
        self.empresas = {}
        for indice, linha in df.iterrows():
            a = linha.to_list()
            self.empresas[a[0]] = a[1:]
    def separador(self, dados):
        for indice, linha in dados.iterrows():
            a = linha.to_list()
            if self.empresas[a[1]][5] == "BRB":
                print(f"{a[1]} - TED")
                print(f"{a[1]} - tranferência")
            else:
                pass

    def relatorio_inicial(self):
        self.dados_de_pagamento()
        self.valor_de_pagamento()

#dados = dados_de_pagamento()
#print(dados)
#fornecedores = fornecedores()
#separador(dados, fornecedores)
#valor_de_pagamento(dados)

#teste = Dados()
#teste.dados_de_pagamento()
#print(teste.pagamentos)
#teste.fornecedores()
#print(teste.empresas)