from src.views.coordenadas.coordenadas_interna import *
from src.views.guia import Guia

from typing import Dict

class GuiaDeTransferenciaInterna(Guia):
    def __init__(self, dados: Dict, logo):
        super().__init__(dados, logo)


    def gerar_guia(self, contador: int, imposto=False):
        for i in range(0, 2):
            self.inserir_logo(LOGO)
            self.gerar_linhas(LINHAS_ESTRUTURA, self.contador)
            self.gerar_retangulos(RETANGULOS, self.contador)
            self.inserir_strings('Times-Roman', 6, TIMES6, self.contador)
            self.inserir_strings('Times-Roman', 7, TIMES7, self.contador)
            self.inserir_strings('Times-Roman', 7, TIMES7DATA, self.contador, self.dados)
            self.inserir_strings('Times-Roman', 8, TIMES8, self.contador)
            self.inserir_strings('Times-Bold', 8, TIMESB8, self.contador)
            self.inserir_strings('Times-Bold', 7, TIMESB8HISTORICO, self.contador, self.dados)
            self.inserir_strings('Times-Bold', 9, TIMESB9, self.contador)
            self.inserir_strings('Times-Bold', 9, TIMESB8CONTA, self.contador, self.dados['Conta_origem'])
            self.inserir_strings('Times-Bold', 9, TIMESBVALORTOTAL, self.contador, self.dados)
            self.inserir_strings('Times-Bold', 12, TIMESB12, self.contador, self.dados['Conta_origem'])
            self.gerar_linhas_texto_alinhado('Times-Bold', 9, TIMESB7EXTENSO, 'Total_extenso', 4)
            if not imposto:
                self.gerar_linhas_texto_alinhado('Times-Bold', 9, TIMESB7NOMEEMPRESA, 'Nome_empresa', 3)
                self.inserir_strings('Times-Bold', 9, TIMESB8FORNECEDOR, self.contador, self.dados['Conta_destino'])
            self.contador += contador
        self.contador = 0
        self.inserir_strings('Times-Bold', 9, TIMESB9PAGAMENTO, self.contador)
        self.inserir_pontilhado(PONTILHADO)
        self.cnv.save()