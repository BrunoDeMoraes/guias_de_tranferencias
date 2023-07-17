from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import fonts
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table

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

        linhas = ['Banco', 'Agência', 'Nº Conta Remetente', 'Uso do Banco']
        linhas2 = [1, 2, 3, 4]
        linhas3 = [1, 2, 3, 4]

        #print(fontes)
        pasta = self.caminho_do_arquivo()

        cnv = canvas.Canvas(f'{pasta}/ted.pdf')
        fontes = cnv.getAvailableFonts()
        for f in fontes:
            print(f)
        cnv.setPageSize(A4)

        contador = 0
        for i in range(0, 2):
            cnv.drawImage(
                f'{pasta}/Imagens/Logo_brb.jpg', self.mm(0), self.mm(276 - contador), width=self.mm(85),
                height=self.mm(18
                               )
            )

            cnv.rect(self.mm(126), self.mm(279 - contador), width=self.mm(70), height=self.mm(7))
            cnv.rect(self.mm(40), self.mm(204 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(70), self.mm(204 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(40), self.mm(199 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(70), self.mm(199 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(140), self.mm(204 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(170), self.mm(204 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(140), self.mm(199 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(170), self.mm(199 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(25), self.mm(194 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(105), self.mm(194 - contador), width=self.mm(3), height=self.mm(3))

            cnv.setFont("Times-Roman", 7)
            cnv.drawString(self.mm(10), self.mm(265 - contador), "Banco")
            cnv.drawString(self.mm(27), self.mm(265 - contador), "Agência")
            cnv.drawString(self.mm(54), self.mm(265 - contador), "Nº Conta Remetente")
            cnv.drawString(self.mm(80), self.mm(265 - contador), "Uso do Banco")
            cnv.drawString(self.mm(104), self.mm(265 - contador), "Banco")
            cnv.drawString(self.mm(121), self.mm(265 - contador), "Agência")
            cnv.drawString(self.mm(148), self.mm(265 - contador), "Nº Conta Favorecido")
            cnv.drawString(self.mm(174), self.mm(265 - contador), "Valor")
            cnv.drawString(self.mm(10), self.mm(255 - contador), "Nome do(s) Remetente(s)")
            cnv.drawString(self.mm(104), self.mm(255 - contador), "Nome do(s) Destinatário(s)")
            cnv.drawString(self.mm(10), self.mm(245 - contador), "CNPJ/CPF(s)")
            cnv.drawString(self.mm(104), self.mm(245 - contador), "CNPJ/CPF(s)")
            cnv.drawString(self.mm(10), self.mm(235 - contador), "Nº identidade / Órgão expedidor / UF")
            cnv.drawString(self.mm(104), self.mm(235 - contador), "Valor por Extenso")
            cnv.drawString(self.mm(10), self.mm(225 - contador), "Endereço")
            cnv.drawString(self.mm(10), self.mm(215 - contador), "Telefone(s)")
            cnv.drawString(self.mm(104), self.mm(215 - contador), "Nº identidade / Órgão expedidor / UF")
            cnv.drawString(self.mm(10), self.mm(205 - contador), "Tipo Pessoa Debitada")
            cnv.drawString(self.mm(10), self.mm(200 - contador), "Tipo Conta Debitada")
            cnv.drawString(self.mm(104), self.mm(205 - contador), "Tipo Pessoa Creditada")
            cnv.drawString(self.mm(104), self.mm(200 - contador), "Tipo Conta Creditada")
            cnv.drawString(self.mm(10), self.mm(195 - contador), "Finalidade")
            cnv.drawString(self.mm(10), self.mm(190 - contador), "Histórico")

            cnv.setFont("Times-Roman", 8)
            cnv.drawString(self.mm(45), self.mm(204 - contador), "Pesssoa Física")
            cnv.drawString(self.mm(75), self.mm(204 - contador), "Pesssoa Jurídica")
            cnv.drawString(self.mm(45), self.mm(199 - contador), "Conta Corrente")
            cnv.drawString(self.mm(75), self.mm(199 - contador), "Conta Poupança")
            cnv.drawString(self.mm(145), self.mm(204 - contador), "Pesssoa Física")
            cnv.drawString(self.mm(175), self.mm(204 - contador), "Pesssoa Jurídica")
            cnv.drawString(self.mm(145), self.mm(199 - contador), "Conta Corrente")
            cnv.drawString(self.mm(175), self.mm(199 - contador), "Conta Poupança")
            cnv.drawString(self.mm(30), self.mm(194 - contador), "00001 - Pagamento de ipostos, tributos e taxas")
            cnv.drawString(self.mm(110), self.mm(194 - contador), "00005 - Pagamentos de fornecedores")
            cnv.drawString(self.mm(40), self.mm(189 - contador), "SEI:")
            cnv.drawString(self.mm(110), self.mm(189 - contador), "Cotação:")
            cnv.drawString(self.mm(150), self.mm(189 - contador), "DANFE:")

            cnv.setFont("Times-Bold", 8)
            cnv.drawString(self.mm(9), self.mm(275 - contador), "ISPB -00.000.208")


            cnv.setFont("Times-Bold", 10)
            cnv.drawString(self.mm(115), self.mm(275 - contador), 'Transferência Eletrônica Disponível - TED -"E"')
            cnv.line(self.mm(8), self.mm(273 - contador), self.mm(196), self.mm(273 - contador))
            cnv.drawString(self.mm(10), self.mm(269 - contador), 'Instituição Financeira Remetente')

            cnv.setFont("Times-Bold", 12)
            cnv.drawString(self.mm(140), self.mm(281 - contador), "Emenda parlamentar")

            cnv.line(self.mm(102), self.mm(268 - contador), self.mm(102), self.mm(198 - contador)) #Linha central
            cnv.line(self.mm(196), self.mm(268 - contador), self.mm(196), self.mm(188 - contador)) #linha direita
            cnv.line(self.mm(8), self.mm(268 - contador), self.mm(8), self.mm(188 - contador)) #linha esquerda
            cnv.line(self.mm(25), self.mm(268 - contador), self.mm(25), self.mm(258 - contador)) #divisão linha 1.1
            cnv.line(self.mm(52), self.mm(268 - contador), self.mm(52), self.mm(258 - contador)) #divisão linha 1.2
            cnv.line(self.mm(78), self.mm(268 - contador), self.mm(78), self.mm(258 - contador)) #divisão linha 1.3
            cnv.line(self.mm(119), self.mm(268 - contador), self.mm(119), self.mm(258 - contador)) #divisão linha 1.4
            cnv.line(self.mm(146), self.mm(268 - contador), self.mm(146), self.mm(258 - contador)) #divisão linha 1.5
            cnv.line(self.mm(172), self.mm(268 - contador), self.mm(172), self.mm(258 - contador)) #divisão linha 1.6
            cnv.line(self.mm(8), self.mm(258 - contador), self.mm(196), self.mm(258 - contador)) #linha horizontal 1
            cnv.line(self.mm(8), self.mm(248 - contador), self.mm(196), self.mm(248 - contador)) #linha horizontal 2
            cnv.line(self.mm(8), self.mm(238 - contador), self.mm(196), self.mm(238 - contador)) #linha horizontal 3
            cnv.line(self.mm(8), self.mm(228 - contador), self.mm(102), self.mm(228 - contador)) #meia linha horizontal 1
            cnv.line(self.mm(8), self.mm(218 - contador), self.mm(196), self.mm(218 - contador)) #linha horizontal 4
            cnv.line(self.mm(8), self.mm(208 - contador), self.mm(196), self.mm(208 - contador)) #linha horizontal 5
            cnv.line(self.mm(8), self.mm(203 - contador), self.mm(196), self.mm(203 - contador)) #linha horizontal 6
            cnv.line(self.mm(8), self.mm(198 - contador), self.mm(196), self.mm(198 - contador)) #linha horizontal 7
            cnv.line(self.mm(8), self.mm(193 - contador), self.mm(196), self.mm(193 - contador)) #linha horizontal 8
            cnv.line(self.mm(8), self.mm(188 - contador), self.mm(196), self.mm(188 - contador)) #linha horizontal 9
            cnv.line(self.mm(8), self.mm(183 - contador), self.mm(8), self.mm(178 - contador))  #linha vertical id esquerda
            cnv.line(self.mm(75), self.mm(183 - contador), self.mm(75), self.mm(178 - contador)) #linha vertica id direita
            cnv.line(self.mm(8), self.mm(178 - contador), self.mm(75), self.mm(178 - contador)) #linha horizontal id
            cnv.line(self.mm(8), self.mm(163 - contador), self.mm(196), self.mm(163 - contador)) #linha horizontal assinatura
            cnv.line(self.mm(102), self.mm(172 - contador), self.mm(102), self.mm(163 - contador)) #linha vertical assinatura
            contador += 143

        cnv.setDash([3, 1])
        cnv.line(self.mm(8), self.mm(153), self.mm(196), self.mm(153))

        #cnv.drawImage(f'{pasta}/Imagens/Logo_brb.jpg', self.mm(0), self.mm(138), width=self.mm(85), height=self.mm(18))






        cnv.save()


if __name__ == '__main__':
    r = Relatorio()
    r.criar_ted()
    #r.fornecedores()