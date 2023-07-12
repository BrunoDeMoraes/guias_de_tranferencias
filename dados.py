import pandas as pd
from num2words import num2words

class Dados:
    def dados_de_pagamento(self):
        df = pd.read_excel("Matrix_2023_HRG.xlsx", skiprows=[0])
        filtro = df.loc[df['Nº DANFE'].notna() & df['Nº TED'].isna()]
        self.pagamentos = filtro.filter(
            ['Cotação', 'Empresa ', 'Nº DANFE', 'V. Total', 'Nº TED', 'Nº de processo SEI', 'Conta']
        )

    def valor_de_pagamento(self):
        duplicados = self.pagamentos[self.pagamentos.duplicated(subset=['Cotação', 'Empresa ', 'Nº DANFE'], keep=False)]
        self.itens_somados = {}
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
                self.itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], soma, linha['Nº de processo SEI'], linha['Conta']]
        for indice, linha in self.pagamentos.iterrows():
            palavra_checagem = str(linha['Cotação']) + '-' + str(linha['Empresa ']) + '-' + str(linha['Nº DANFE'])
            if palavra_checagem in checagem:
                continue
            else:
                checagem.append(palavra_checagem)
                descricao = palavra_checagem.split('-')
                self.itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], linha['V. Total'], linha['Nº de processo SEI'], linha['Conta']]
        self.valor_por_extenso()


    def valor_por_extenso(self):
        for chave, valor in sorted(self.itens_somados.items()):
            extenso = num2words(valor[3], lang='pt_BR', to='currency')
            valor.append(extenso)

    def fornecedores(self):
        df = pd.read_excel("Matrix_2023_HRG.xlsx", sheet_name='Fornecedores')
        self.empresas = {}
        for indice, linha in df.iterrows():
            a = linha.to_list()
            self.empresas[a[0]] = a[1:]
            print(self.empresas)

    def separador(self, dados):
        for indice, linha in dados.iterrows():
            a = linha.to_list()
            if self.empresas[a[1]][5] == "BRB":
                print(f"{a[1]} - TED")
                print(f"{a[1]} - tranferência")
            else:
                pass

    def valores_formatados(self):
        valores_impressao = ""
        for i in self.itens_somados.values():
            valores_impressao = valores_impressao + f'\n{i}\n'
        print(valores_impressao)
        return valores_impressao

    def listar_pagamentos(self):
        self.dados_de_pagamento()
        self.valor_de_pagamento()
        self.valores_formatados()

    def checa_carregamento(self):
        return hasattr(self, 'itens_somados')
