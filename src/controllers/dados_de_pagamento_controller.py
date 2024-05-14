import pandas as pd
from tkinter import messagebox
from num2words import num2words

from src import *


class DadosDePagamentoController:
    def __init__(self):
        self.colunas = COLUNAS
        self.lista_de_pagamentos = {}


    def carregar_dados_de_pagamento(self, fonte):
        try:
            df = pd.read_excel(fonte, sheet_name='Controle', skiprows=[0])
            filtro = df.loc[df['Nº DANFE'].notna() & df['Nº TED'].isna()]
            dados = filtro.filter(self.colunas)
            return dados
        except FileNotFoundError:
            messagebox.showerror(
                PLANILHA_INEXISTENTE[0],
                PLANILHA_INEXISTENTE[1]
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
        danfes_complexas = self.filtrar_danfe(fonte)
        self.inserir_pagamento(danfes_complexas)
        danfes_simples = self.carregar_dados_de_pagamento(fonte)
        self.inserir_pagamento(danfes_simples)
        self.valor_por_extenso()
        for item in self.lista_de_pagamentos.items():
            print(f'{item[0]}\n    {item[1]}\n')
        return self.lista_de_pagamentos


    def inserir_pagamento(self, data_frame):
        for indice, linha in data_frame.iterrows():
            id_pagamento = self.gerar_id_de_pagamento(linha)
            if id_pagamento in self.lista_de_pagamentos.keys():
                continue
            else:
                descricao = id_pagamento.split('-')
                subset = self.gerar_subset(data_frame, linha)
                colunas_somadas = self.somar_valores_subset(subset)
                linha_de_pagamento = self.compilar_linha_de_pagamento(
                    descricao,
                    linha,
                    colunas_somadas
                )
                self.lista_de_pagamentos[id_pagamento] = linha_de_pagamento


    def gerar_id_de_pagamento(self, linha_de_pagamento):
        id = (
                str(linha_de_pagamento['Cotação']) + '-' +
                str(linha_de_pagamento['Empresa']) + '-' +
                str(linha_de_pagamento['Nº DANFE'])
        )
        return id

    def gerar_subset(self, data_frame, linha_de_pagamento):
        subset = data_frame[
            (data_frame['Cotação'] == linha_de_pagamento['Cotação']) &
            (data_frame['Empresa'] == linha_de_pagamento['Empresa']) &
            (data_frame['Nº DANFE'] == linha_de_pagamento['Nº DANFE'])
            ]
        return subset


    def somar_valores_subset(self, subset):
        soma = subset['Liquido'].sum()
        soma_iss = subset['ISS'].sum()
        soma_ir = subset['IR'].sum()
        soma_valor_total = subset['V. Total'].sum()
        somas = [soma, soma_iss, soma_ir, soma_valor_total]
        return somas

    def compilar_linha_de_pagamento(self, descricao, linha, colunas_somadas=None):
        if colunas_somadas != None:
            dados_compilados_soma = [
                descricao[0],
                descricao[1],
                descricao[2],
                colunas_somadas[0],
                linha['Nº de processo SEI'],
                linha['Conta'],
                colunas_somadas[1],
                colunas_somadas[2],
                colunas_somadas[3]
            ]
            return dados_compilados_soma
        else:
            dados_compilados = [
                descricao[0],
                descricao[1],
                descricao[2],
                linha['Liquido'],
                linha['Nº de processo SEI'],
                linha['Conta'],
                linha['ISS'],
                linha['IR'],
                linha['V. Total']
            ]
            return dados_compilados

    def valor_por_extenso(self):
        for chave, valor in sorted(self.lista_de_pagamentos.items()):
            extenso = num2words(valor[3], lang='pt_BR', to='currency')
            valor.append(extenso)


if __name__ == "__main__":
    fonte = '//srv-fs/HRG_GEOF/GEOF/PAGAMENTOS/Fontes/Matrix_2023_HRG.xlsx'
    teste = DadosDePagamentoController()
    pagamentos = teste.listar_pagamentos(fonte)

