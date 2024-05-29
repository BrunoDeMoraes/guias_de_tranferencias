from src.views.coordenadas.coordenadas_transferencia import *
from src.views.guia import Guia

from typing import List

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class Guia_de_transferencia(Guia):
    def __init__(self):
        self.cnv = canvas.Canvas(f'C:/Users/14343258/PycharmProjects/guias_de_tranasferência/guias/teste/teste3.pdf')
        self.cnv.setPageSize(A4)
        self.imagens = f'C:/Users/14343258/PycharmProjects/guias_de_tranasferência/Imagens/'
        self.contador = 0


    def gerar_guia(self):
        for i in range(0, 2):
            self.inserir_logo()
            self.gerar_linhas()
            self.gerar_retangulos()
            self.inserir_strings('Times-Roman', 6, TIMES6)
            self.inserir_strings('Times-Roman', 7, TIMES7)
            self.inserir_strings('Times-Roman', 8, TIMES8)
            self.inserir_strings('Times-Bold', 8, TIMESB8)
            self.inserir_strings('Times-Bold', 9, TIMESB9)
            self.contador += 100
        self.inserir_pontilhado()
        self.cnv.save()
        self.contador = 0


    def inserir_logo(self):
        self.cnv.drawImage(
            f'{self.imagens}logo.png',
            self.mm(10),
            self.mm(275 - self.contador),
            width=self.mm(45),
            height=self.mm(14)
        )


    def gerar_linhas(self):
            for linha in LINHAS:
                self.cnv.line(
                    self.mm(linha[0]),
                    self.mm(linha[1] - self.contador),
                    self.mm(linha[2]),
                    self.mm(linha[3] - self.contador)
                )


    def inserir_pontilhado(self):
        self.cnv.setDash([3, 1])
        self.cnv.line(self.mm(8), self.mm(192), self.mm(196), self.mm(192))

    def gerar_retangulos(self):
        for coordenda in RETANGULOS:
            self.cnv.rect(
                self.mm(coordenda[0]),
                self.mm(coordenda[1] - self.contador),
                width=self.mm(coordenda[2]),
                height=self.mm(coordenda[3])
            )

    def inserir_strings(self, fonte: str, tamanho: int, coordenadas: List):
        self.cnv.setFont(fonte, tamanho)
        for coordenada in coordenadas:
            self.cnv.drawString(
                self.mm(coordenada[0]),
                self.mm(coordenada[1] - self.contador),
                f'{coordenada[2]}'
            )

if __name__ == "__main__":
    teste = Guia_de_transferencia()
    teste.gerar_guia()
