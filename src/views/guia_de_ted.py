from src.views.coordenadas.coordenadas_transferencia import *
from src.views.guia import Guia

from typing import Dict

class GuiaDeTED(Guia):
    def __init__(self, dados: Dict, logo):
        super().__init__(dados, logo)

    def gerar_guia(self):
        for i in range(0, 2):
            self.inserir_logo()
            self.gerar_linhas(LINHAS_ESTRUTURA, self.contador)
            self.gerar_retangulos(RETANGULOS, self.contador)
            self.inserir_strings('Times-Roman', 6, TIMES6, self.contador)
            self.inserir_strings('Times-Roman', 7, TIMES7, self.contador)
            self.inserir_strings('Times-Roman', 7, TIMES7DATA, self.contador, self.dados)
            self.inserir_strings('Times-Roman', 8, TIMES8, self.contador)
            self.inserir_strings('Times-Bold', 8, TIMESB8, self.contador)
            self.inserir_strings('Times-Bold', 7, TIMESB8HISTORICO, self.contador, self.dados)
            self.inserir_strings('Times-Bold', 9, TIMESB9, self.contador)
            self.inserir_strings('Times-Bold', 8, TIMESB8CONTA, self.contador, self.dados['Conta_origem'])
            self.inserir_strings('Times-Bold', 8, TIMESB8FORNECEDOR, self.contador, self.dados['Dados_empresa'])
            self.inserir_strings('Times-Bold', 8, TIMESBVALORTOTAL, self.contador, self.dados)
            self.inserir_strings('Times-Bold', 12, TIMESB12, self.contador, self.dados['Conta_origem'])
            self.gerar_linhas_texto_alinhado('Times-Bold', 7, TIMESB7NOMEEMPRESA, 'Nome_empresa', 3)
            self.gerar_linhas_texto_alinhado('Times-Bold', 9, TIMESB7EXTENSO, 'Total_extenso', 4)
            self.contador += 100
        self.contador = 0
        self.gerar_area_de_pagamentos(LINHAS_PAGAMENTOS, RETANGULO_PAGAMENTO, TIMES8_PAGAMENTOS)
        self.inserir_pontilhado()
        self.cnv.save()


if __name__ == "__main__":
    teste = GuiaDeTED()
    teste.gerar_guia()