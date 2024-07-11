import pandas as pd
from tkinter import messagebox
from num2words import num2words
from typing import Dict

from src import *


class DadosDePagamentoRepository:
    def __init__(self):
        self.colunas = COLUNAS
        self.lista_de_pagamentos = {}


    def soma_valor_liquido(self, fonte: str) -> Dict:
        lista_de_pagamentos = self.agupar_por_empresa(fonte)
        for pagamento_geral in lista_de_pagamentos.values():
            total_liquido = 0
            for lista in pagamento_geral:
                total_liquido += lista[3]
            pagamento_geral.append(total_liquido)
        return lista_de_pagamentos


    def agupar_por_empresa(self, fonte: str) -> Dict:
        pagamentos = self.listar_pagamentos(fonte)
        pagamento_por_empresa = {}
        for pagamento in pagamentos.values():
            chave = (pagamento[1] + pagamento[5])
            if chave not in pagamento_por_empresa.keys():
                pagamento_por_empresa[chave] = []
                pagamento_por_empresa[chave].append(pagamento)
            else:
                pagamento_por_empresa[chave].append(pagamento)
        return pagamento_por_empresa


    def listar_pagamentos(self, fonte):
        danfes_complexas = self.__filtrar_danfe(fonte)
        self.__inserir_pagamento(danfes_complexas)
        danfes_simples = self.__carregar_dados_de_pagamento(fonte)
        self.__inserir_pagamento(danfes_simples)
        self.valor_por_extenso()
        return self.lista_de_pagamentos


    def __carregar_dados_de_pagamento(self, fonte):
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


    def __filtrar_danfe(self, fonte):
        pagamentos = self.__carregar_dados_de_pagamento(fonte)
        duplicados = pagamentos[
            pagamentos.duplicated(
                subset=['Cotação', 'Empresa', 'Nº DANFE'],
                keep=False
            )
        ]
        return duplicados


    def __inserir_pagamento(self, data_frame):
        for indice, linha in data_frame.iterrows():
            id_pagamento = self.__gerar_id_de_pagamento(linha)
            if id_pagamento in self.lista_de_pagamentos.keys():
                continue
            else:
                descricao = id_pagamento.split('-')
                subset = self.__gerar_subset(data_frame, linha)
                colunas_somadas = self.__somar_valores_subset(subset)
                linha_de_pagamento = self.__compilar_linha_de_pagamento(
                    descricao,
                    linha,
                    colunas_somadas
                )
                self.lista_de_pagamentos[id_pagamento] = linha_de_pagamento


    def __gerar_id_de_pagamento(self, linha_de_pagamento):
        id = (
                str(linha_de_pagamento['Cotação']) + '-' +
                str(linha_de_pagamento['Empresa']) + '-' +
                str(linha_de_pagamento['Nº DANFE'])
        )
        return id


    def __gerar_subset(self, data_frame, linha_de_pagamento):
        subset = data_frame[
            (data_frame['Cotação'] == linha_de_pagamento['Cotação']) &
            (data_frame['Empresa'] == linha_de_pagamento['Empresa']) &
            (data_frame['Nº DANFE'] == linha_de_pagamento['Nº DANFE'])
            ]
        return subset


    def __somar_valores_subset(self, subset):
        soma = subset['Liquido'].sum()
        soma_iss = subset['ISS'].sum()
        soma_ir = subset['IR'].sum()
        soma_valor_total = subset['V. Total'].sum()
        somas = [soma, soma_iss, soma_ir, soma_valor_total]
        return somas


    def __compilar_linha_de_pagamento(self, descricao, linha, colunas_somadas):
        print(f'DDDD {descricao[2]} tipo {type(descricao[2])}')
        dados_compilados_soma = [
            descricao[0],
            descricao[1],
            self.corrigir_n_danfe(descricao[2]),
            colunas_somadas[0],
            linha['Nº de processo SEI'],
            linha['Conta'],
            colunas_somadas[1],
            colunas_somadas[2],
            colunas_somadas[3]
        ]
        return dados_compilados_soma

    def corrigir_n_danfe(self, danfe):
        if '.' in danfe:
            return danfe[0:danfe.index('.')]
        else:
            return danfe



    def valor_por_extenso(self):
        for chave, valor in sorted(self.lista_de_pagamentos.items()):
            extenso = num2words(valor[3], lang='pt_BR', to='currency')
            valor.append(extenso)


if __name__ == "__main__":
    fonte = '//srv-fs/HRG_GEOF/GEOF/PAGAMENTOS/Fontes/Matrix_2023_HRG.xlsx'
    teste = DadosDePagamentoRepository()
    pagamentos = teste.agupar_por_empresa(fonte)

