from abc import ABC, abstractmethod
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from typing import Dict
from typing import List

import src.views.coordenadas.coordenadas_transferencia as transferencia
import src.views.coordenadas.coordenadas_ted as ted
import src.views.coordenadas.coordenadas_iss as iss


class Guia(ABC):
    def __init__(self, dados: Dict, logo):
        self.contador = 0
        self.altura = 0
        self.dados = dados
        self.imagens = f'C:/Users/14343258/PycharmProjects/guias_de_tranasferência/Imagens/'
        self.cnv = canvas.Canvas(f'C:/Users/14343258/PycharmProjects/guias_de_tranasferência/guias/teste/{self.dados["Empresa"]}.pdf')
        self.cnv.setPageSize(A4)
        self.logo = logo


    def inserir_logo(self, coordenadas):
        self.cnv.drawImage(
            f'{self.imagens}{self.logo}',
            self.mm(coordenadas[0]),
            self.mm(coordenadas[1] - self.contador),
            width=self.mm(coordenadas[2]),
            height=self.mm(coordenadas[3])
        )


    def mm(self, medida):
        return (medida/0.352777)


    def gerar_linhas(self, linhas, contador):
            for linha in linhas:
                self.cnv.line(
                    self.mm(linha[0]),
                    self.mm(linha[1] - contador),
                    self.mm(linha[2]),
                    self.mm(linha[3] - contador)
                )


    def inserir_pontilhado(self, coordenadas):
        self.cnv.setDash([3, 1])
        self.cnv.line(self.mm(coordenadas[0]), self.mm(coordenadas[1]), self.mm(coordenadas[2]), self.mm(coordenadas[3]))


    def gerar_retangulos(self, retangulos, contador):
        for coordenda in retangulos:
            self.cnv.rect(
                self.mm(coordenda[0]),
                self.mm(coordenda[1] - contador),
                width=self.mm(coordenda[2]),
                height=self.mm(coordenda[3])
            )


    def inserir_strings(
            self,
            fonte: str,
            tamanho: int,
            coordenadas: List,
            contador,
            entrada=None,
    ):
        self.cnv.setFont(fonte, tamanho)
        for coordenada in coordenadas:
            texto = self.selecionar_tipo_de_entrada(entrada, coordenada)
            self.cnv.drawString(
                self.mm(coordenada[0]),
                self.mm(coordenada[1] - contador),
                f'{texto}'
            )


    def selecionar_tipo_de_entrada(self, entrada, coordenada):
        if entrada == None:
            return coordenada[2]
        elif (
                isinstance(entrada, list) or
                isinstance(entrada, tuple) or
                isinstance(entrada, dict)
        ):
            return entrada[coordenada[2]]
        else:
            print('Deu alguma merda')


    def gerar_area_de_pagamentos(self, linhas_pagamento, retangulo_pagamentos, times8_pagamento):
        for pagamento in self.dados['Pagamentos']:
            self.gerar_linhas(linhas_pagamento, self.altura)
            self.gerar_retangulos(retangulo_pagamentos, self.altura)
            self.inserir_strings(
            'Times-Roman',
                6,
                times8_pagamento,
                self.altura,
                pagamento
            )
            self.altura += 3
        self.altura = 0


    def gerar_linhas_texto_alinhado(self, fonte, tamanho, coordenadas, entrada, fator):
        self.cnv.setFont(fonte, tamanho)
        corretor = 0
        for linha in self.dados[entrada]:
            self.cnv.drawString(
                self.mm(coordenadas[0]),
                self.mm((coordenadas[1] - self.contador) - corretor),
                linha
            )
            corretor += fator

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
                self.inserir_strings('Times-Bold', 8, coordinate.TIMESB8FORNECEDOR, self.contador,
                                     self.dados['Dados_empresa'])
            self.contador += contador
        self.contador = 0
        self.gerar_retangulos(coordinate.RETANGULOSTITULO, self.contador)
        self.gerar_linhas(coordinate.LINHASTPGAMENTO, self.contador)
        self.inserir_strings('Times-Bold', 7, coordinate.TIMESB9PAGAMENTO, self.contador)
        self.gerar_area_de_pagamentos(coordinate.LINHAS_PAGAMENTOS, coordinate.RETANGULO_PAGAMENTO,
                                      coordinate.TIMES8_PAGAMENTOS)
        self.inserir_pontilhado(coordinate.PONTILHADO)
        self.cnv.save()
