from coordenadas.coordenadas_transferencia import *
from guia import Guia

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class Guia_de_transferencia(Guia):
    def __init__(self):
        self.cnv = canvas.Canvas(f'C:/Users/14343258/PycharmProjects/guias_de_tranasferência/guias/teste/teste8.pdf')
        self.cnv.setPageSize(A4)
        self.imagens = f'C:/Users/14343258/PycharmProjects/guias_de_tranasferência/Imagens/'
        self.contador = 0


    def gerar_guia(self):
        for i in range(0, 2):
            self.inserir_logo()
            self.gerar_linhas()
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


if __name__ == "__main__":
    teste = Guia_de_transferencia()
    teste.gerar_guia()