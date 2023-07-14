from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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
            else:
                print(f"{empresa} - Banco: {banco} - melhor fazer uma TED!, ")

if __name__ == '__main__':
    r = Relatorio()
    r.separador()
    #r.fornecedores()