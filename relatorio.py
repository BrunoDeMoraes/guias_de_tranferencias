from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import fonts

from contas import Contas
from dados import Dados
class Relatorio(Contas, Dados):
    def __init__(self):
        self.lis = []

    def separador(self):
        fornecedores = self.fornecedores()
        self.dados_de_pagamento()
        pagamentos = self.valor_de_pagamento().values()
        for pagamento in pagamentos:
            empresa = pagamento[1]
            banco = fornecedores[pagamento[1]][5]
            if (banco) == "BRB":
                print(f"{empresa} - É BRB, porra! Transferência intena")
                #chama guia BRB
            else:
                print(f"{empresa} - Banco: {banco} - melhor fazer uma TED!, ")
                #chama guia de TED


    def mm(self, medida):
        return (medida/0.352777)

    def criar_ted(self):
        #ontes = fonts.
        #print(fontes)
        pasta = self.caminho_do_arquivo()
        cnv = canvas.Canvas(f'{pasta}/ted.pdf')
        cnv.setPageSize(A4)
        cnv.drawImage(f'{pasta}/Imagens/Logo_brb.jpg', self.mm(0), self.mm(276), width=self.mm(85), height=self.mm(18))
        cnv.rect(self.mm(126), self.mm(279), width=self.mm(70), height=self.mm(7))
        cnv.setFont("Courier-Bold", 12)
        cnv.drawString(self.mm(140), self.mm(281), "Emenda parlamentar")
        cnv.setFont("Courier-Bold", 8)
        cnv.drawString(self.mm(9), self.mm(275), "ISPB -00.000.208")
        cnv.setFont("Courier-Bold", 10)
        cnv.drawString(self.mm(110), self.mm(275), 'Transferência Eletrônica Disponível - TED -"E"')
        cnv.setFont("Courier-Bold", 10)
        cnv.drawString(self.mm(110), self.mm(275), 'Transferência Eletrônica Disponível - TED -"E"')
        cnv.setFont("Courier-Bold", 10)
        cnv.drawString(self.mm(110), self.mm(275), 'Transferência Eletrônica Disponível - TED -"E"')
        cnv.setFont("Courier-Bold", 10)
        cnv.drawString(self.mm(110), self.mm(275), 'Transferência Eletrônica Disponível - TED -"E"')
        cnv.save()

if __name__ == '__main__':
    r = Relatorio()
    r.criar_ted()
    #r.fornecedores()