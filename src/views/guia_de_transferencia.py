from src.views.coordenadas.coordenadas_transferencia import *
from src.views.guia import Guia

from typing import Dict

import src.views.coordenadas.coordenadas_transferencia as transferencia
import src.views.coordenadas.coordenadas_ted as ted
import src.views.coordenadas.coordenadas_iss as iss



class GuiaDeTransferencia(Guia):
    def __init__(self, dados: Dict, logo):
        super().__init__(dados, logo)

    def gerar_guia(self, contador: int, coordenada, imposto=False):
        coordenadas = {
            'transferencia': transferencia,
            'ted': ted,
            'iss': iss
        }
        coordinate = coordenadas[coordenada]
        for i in range(0, 2):
            self.inserir_logo(coordinate.LOGO)
            self.gerar_linhas(coordinate.LINHAS_ESTRUTURA, self.contador)
            self.gerar_retangulos(coordinate.RETANGULOS, self.contador)
            self.inserir_strings('Times-Roman', 6, coordinate.TIMES6, self.contador)
            self.inserir_strings('Times-Roman', 7, coordinate.TIMES7, self.contador)
            self.inserir_strings('Times-Roman', 7, coordinate.TIMES7DATA, self.contador, self.dados)
            self.inserir_strings('Times-Roman', 8, coordinate.TIMES8, self.contador)
            self.inserir_strings('Times-Bold', 8, coordinate.TIMESB8, self.contador)
            self.inserir_strings('Times-Bold', 7, coordinate.TIMESB8HISTORICO, self.contador, self.dados)
            self.inserir_strings('Times-Bold', 9, coordinate.TIMESB9, self.contador)
            self.inserir_strings('Times-Bold', 9, coordinate.TIMESB8CONTA, self.contador, self.dados['Conta_origem'])
            self.inserir_strings('Times-Bold', 9, coordinate.TIMESBVALORTOTAL, self.contador, self.dados)
            self.inserir_strings('Times-Bold', 12, coordinate.TIMESB12, self.contador, self.dados['Conta_origem'])
            self.gerar_linhas_texto_alinhado('Times-Bold', 9, coordinate.TIMESB7EXTENSO, 'Total_extenso', 4)
            if not imposto:
                self.gerar_linhas_texto_alinhado('Times-Bold', 7, coordinate.TIMESB7NOMEEMPRESA, 'Nome_empresa', 3)
                self.inserir_strings('Times-Bold', 8, coordinate.TIMESB8FORNECEDOR, self.contador, self.dados['Dados_empresa'])
            self.contador += contador
        self.contador = 0
        self.gerar_retangulos(coordinate.RETANGULOSTITULO, self.contador)
        self.gerar_linhas(coordinate.LINHASTPGAMENTO, self.contador)
        self.inserir_strings('Times-Bold', 7, coordinate.TIMESB9PAGAMENTO, self.contador)
        self.gerar_area_de_pagamentos(coordinate.LINHAS_PAGAMENTOS, coordinate.RETANGULO_PAGAMENTO, coordinate.TIMES8_PAGAMENTOS)
        self.inserir_pontilhado(coordinate.PONTILHADO)
        self.cnv.save()
