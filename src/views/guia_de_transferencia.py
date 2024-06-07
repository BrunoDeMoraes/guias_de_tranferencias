from src.views.coordenadas.coordenadas_transferencia import *
from src.views.guia import Guia

from typing import Dict
from typing import List

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class Guia_de_transferencia(Guia):
    def __init__(self, dados: Dict):
        self.contador = 0
        self.altura = 0
        self.dados = dados
        self.imagens = f'C:/Users/14343258/PycharmProjects/guias_de_tranasferência/Imagens/'
        self.cnv = canvas.Canvas(f'C:/Users/14343258/PycharmProjects/guias_de_tranasferência/guias/teste/{self.dados["Empresa"]}.pdf')
        self.cnv.setPageSize(A4)


    def gerar_guia(self):
        for i in range(0, 2):
            self.inserir_logo()
            self.gerar_linhas(LINHAS_ESTRUTURA, self.contador)
            self.gerar_retangulos(RETANGULOS, self.contador)
            self.inserir_strings('Times-Roman', 6, TIMES6, self.contador)
            self.inserir_strings('Times-Roman', 7, TIMES7, self.contador)
            self.inserir_strings('Times-Roman', 8, TIMES8, self.contador)
            self.inserir_strings('Times-Bold', 8, TIMESB8, self.contador)
            self.inserir_strings('Times-Bold', 9, TIMESB9, self.contador)
            self.contador += 100
        self.contador = 0
        self.gerar_area_de_pagamentos()
        self.inserir_pontilhado()
        self.cnv.save()


    def inserir_logo(self):
        self.cnv.drawImage(
            f'{self.imagens}logo.png',
            self.mm(10),
            self.mm(275 - self.contador),
            width=self.mm(45),
            height=self.mm(14)
        )


    def gerar_linhas(self, linhas, contador):
            for linha in linhas:
                self.cnv.line(
                    self.mm(linha[0]),
                    self.mm(linha[1] - contador),
                    self.mm(linha[2]),
                    self.mm(linha[3] - contador)
                )


    def inserir_pontilhado(self):
        self.cnv.setDash([3, 1])
        self.cnv.line(self.mm(8), self.mm(192), self.mm(196), self.mm(192))


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
            entrada=None
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


    def gerar_area_de_pagamentos(self):
        for pagamento in self.dados['Pagamentos']:
            print(f'Esse é o pagamento {pagamento}')
            self.gerar_linhas(LINHAS_PAGAMENTOS, self.altura)
            self.gerar_retangulos(RETANGULO_PAGAMENTO, self.altura)
            self.inserir_strings(
                'Times-Roman',
                8,
                TIMES8_PAGAMENTOS,
                self.altura,
                pagamento
            )
            self.altura += 5
        self.altura = 0

if __name__ == "__main__":
    teste = Guia_de_transferencia()
    teste.gerar_guia()
