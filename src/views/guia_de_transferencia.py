from coordenadas import *
from guia import Guia

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class Guia_de_transferencia(Guia):
    def gerar_guia(self):
        cnv = canvas.Canvas(f'{self.pasta}/guias/{origem}/{data_pagamento}/TEDS/{pagamento[0][1]}-{conta[1]}-{conta[2]}.pdf')
        cnv.setPageSize(A4)