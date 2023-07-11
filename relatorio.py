from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from contas import Contas
from dados import Dados
class Relatorio(Contas, Dados):

    def gerar_ted(self):
        pass
