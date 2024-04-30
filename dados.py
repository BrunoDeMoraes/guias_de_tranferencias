from tkinter import messagebox

import pandas as pd
from num2words import num2words

from typing import Dict

class Dados:
    colunas = ['Cotação',
                'Item',
                'Empresa',
                'Nº DANFE',
                'V. Total',
                'Nº TED',
                'Nº de processo SEI',
                'Conta',
                'ISS',
                'IR',
                'Liquido'
               ]

    itens_somados = {}

    def carregar_dados_de_pagamento(self, fonte):
        try:
            df = pd.read_excel(fonte, sheet_name='Controle', skiprows=[0])
            filtro = df.loc[df['Nº DANFE'].notna() & df['Nº TED'].isna()]
            dados = filtro.filter(Dados.colunas)
            return dados
        except FileNotFoundError:
            messagebox.showerror(
                'Tem arquivo não!',
                'Configura os caminhos das planilhas, Doidão!'
            )

    def filtrar_danfe(self, fonte):
        pagamentos = self.carregar_dados_de_pagamento(fonte)
        duplicados = pagamentos[
            pagamentos.duplicated(
                subset=['Cotação', 'Empresa', 'Nº DANFE'], keep=False
            )
        ]
        return duplicados

    def listar_pagamentos(self, fonte):
        checagem = []
        duplicados = self.filtrar_danfe(fonte)
        for indice, linha in duplicados.iterrows():
            palavra_checagem = (
                    str(linha['Cotação']) +
                    '-' +
                    str(linha['Empresa']) +
                    '-' +
                    str(linha['Nº DANFE'])
            )
            if palavra_checagem in checagem:
                continue
            else:

                checagem.append(palavra_checagem)
                descricao = palavra_checagem.split('-')

                duplicados_subset1 = duplicados[
                    (duplicados['Cotação'] == linha['Cotação']) &
                    (duplicados['Empresa'] == linha['Empresa']) &
                    (duplicados['Nº DANFE'] == linha['Nº DANFE'])
                ]
                soma = duplicados_subset1['Liquido'].sum()
                soma_iss = duplicados_subset1['ISS'].sum()
                soma_ir = duplicados_subset1['IR'].sum()
                soma_valor_total = duplicados_subset1['V. Total'].sum()
                Dados.itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], soma, linha['Nº de processo SEI'], linha['Conta'], soma_iss, soma_ir, soma_valor_total]

        pagamentos = self.carregar_dados_de_pagamento(fonte)
        for indice, linha in pagamentos.iterrows():
            palavra_checagem = str(linha['Cotação']) + '-' + str(linha['Empresa']) + '-' + str(linha['Nº DANFE'])
            if palavra_checagem in checagem:
                continue
            else:
                checagem.append(palavra_checagem)
                descricao = palavra_checagem.split('-')
                Dados.itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], linha['Liquido'],
                                                   linha['Nº de processo SEI'], linha['Conta'], linha['ISS'],
                                                   linha['IR'], linha['V. Total']]
        self.valor_por_extenso(Dados.itens_somados)
        return Dados.itens_somados

    def pagamentos_filtrados(self, fonte, indice):
        pagamentos_filtrados = {}
        pagamentos = self.listar_pagamentos(fonte)
        for i in pagamentos.items():
            if i[1][indice] == 0:
                continue
            else:
                pagamentos_filtrados[i[0]] = i[1]
        for pagamento in pagamentos_filtrados.items():
            print(pagamento)
        return pagamentos_filtrados

    def soma_indice(self, pagamentos, indice):
        indice_somado = 0
        for pagamento in pagamentos.values():
            if pagamento[indice] == 0:
                continue
            else:
                indice_somado += float(pagamento[indice])
                print(f'total = {indice_somado}')
        return indice_somado


    def valor_por_extenso(self, itens_somados):
        for chave, valor in sorted(itens_somados.items()):
            extenso = num2words(valor[3], lang='pt_BR', to='currency')
            valor.append(extenso)

    def aglutinar_por_empresa(self, fonte):
        pagamentos = self.listar_pagamentos(fonte)
        pagamento_por_empresa = {}
        for pagamento in pagamentos.values():
            if pagamento[1] not in pagamento_por_empresa.keys():
                pagamento_por_empresa[pagamento[1]] = []
                pagamento_por_empresa[pagamento[1]].append(pagamento)
            else:
                pagamento_por_empresa[pagamento[1]].append(pagamento)
        print(pagamento_por_empresa)
        return pagamento_por_empresa

    def soma_valor_liquido(self, fonte):
        lista_de_pagamentos = self.aglutinar_por_empresa(fonte)
        for pagamento_geral in lista_de_pagamentos.values():
            total_liquido = 0
            for lista in pagamento_geral:
                total_liquido += lista[3]
            pagamento_geral.append(total_liquido)
        return lista_de_pagamentos

    def fornecedores(self, fonte):
        df = pd.read_excel(fonte, sheet_name='Fornecedores')
        empresas = {}
        for indice, linha in df.iterrows():
            a = linha.to_list()
            empresas[a[0]] = a[1:]
        return empresas


if __name__ == "__main__":
    fonte = '//srv-fs/HRG_GEOF/GEOF/PAGAMENTOS/Fontes/Matrix_2023_HRG.xlsx'
    teste = Dados()
    pagamentos_iss = teste.pagamentos_filtrados(fonte, 6)
    teste.soma_indice(pagamentos_iss, 6)
    pagamentos_ir = teste.pagamentos_filtrados(fonte, 7)
    teste.soma_indice(pagamentos_ir, 7)


    #teste.soma_valor_liquido()
