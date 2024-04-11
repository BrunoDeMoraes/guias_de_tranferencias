import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import fonts
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from datetime import date

from contas import Contas
from dados import Dados
from estrutura import Estrutura

from comandos_sql import TABELAS
from comandos_sql import CONTAS
from comandos_sql import URLS

class Relatorio(Contas, Dados, Estrutura):
    def __init__(self):
        self.pasta = self.caminho_do_arquivo()
        self.criar_pastas(self.pasta)
        self.criar_bd(TABELAS)
        self.contas = self.consultar_registros(CONTAS)
        self.urls = self.consultar_registros(URLS)
        print(f"Estas são as URLs {self.urls}")
        self.pagamentos = self.soma_valor_liquido(self.urls[0][1])
        self.empresas = self.fornecedores(self.urls[0][1])
        self.data = date.today()
        self.data_formatada = self.data.strftime('%d/%m/%Y')

    def pagamentos_formatados(self):
        pagamentos_listados = []
        for pagamento in self.pagamentos.values():
            print(f'Esse é o pagamento {pagamento}')
            resumo = f'''Cotação: {pagamento[0]}\nEmpresa: {pagamento[1]}\nNota Fiscal nº: {pagamento[2]}\nValor: R$ {self.formartar_valor(pagamento[3])} ({pagamento[8]})\nProcesso SEI nº: {pagamento[4]}\nTipo de verba: {pagamento[5]}'''
            pagamentos_listados.append(resumo)
        return pagamentos_listados

    def formatar_relatorio(self, iteravel):
        valores_impressao = ""
        for i in iteravel:
            valores_impressao = valores_impressao + f'\n{i}\n'
        return valores_impressao

    def formatar_nome(self, nome):
        divisao = nome.split()
        novo_nome = (" ").join(divisao[0:-1])
        return novo_nome

    def formartar_valor(self, valor):
        arredondado = f"{valor:.2f}"
        virgula = arredondado.replace(".", ",")
        if len(virgula) >= 10:
            milhao = virgula[0:-9] + "." + virgula[-9:-6] + "." + virgula[-6:]
            return milhao
        elif len(virgula) >= 7:
            mil = virgula[0:-6] + "." + virgula[-6:]
            return (mil)
        else:
            return virgula

    def formatar_cnpj(self, cnpj):
        mascara = f"{cnpj[-14:-12]}.{cnpj[-12:-9]}.{cnpj[-9:-6]}/{cnpj[-6:-2]}-{cnpj[-2:]}"
        return mascara

    def formatar_conta(self, conta):
        conta_formatada = f"{conta[:-4]}.{conta[-4:-1]}-{conta[-1]}"
        return conta_formatada


    def mm(self, medida):
        return (medida/0.352777)

    def alinhar_texto(self, texto: str):
        palavras = texto.split(" ")
        linha = ""
        texto_alinhado = []
        for palavra in palavras:
            if len((linha + palavra)) > 60:
                #print(len(linha))
                texto_alinhado.append(linha)
                linha = palavra + " "
            else:
                linha += palavra + " "
            if palavra == palavras[-1]:
                texto_alinhado.append(linha)
        return texto_alinhado

    def criar_ted(self, pagamento, empresa, conta, origem, data_pagamento):
        if not os.path.exists(f'{self.pasta}/guias/{origem}/{data_pagamento}/TEDS'):
            os.makedirs(f'{self.pasta}/guias/{origem}/{data_pagamento}/TEDS')

        cnv = canvas.Canvas(f'{self.pasta}/guias/{origem}/{data_pagamento}/TEDS/{pagamento[0][0:3]}-{pagamento[1]}-{pagamento[2]}.pdf')
        cnv.setPageSize(A4)

        contador = 0
        for i in range(0, 2):
            print(empresa)
            cnv.drawImage(
                f'{self.pasta}/Imagens/Logo_brb.jpg', self.mm(0), self.mm(276 - contador), width=self.mm(85),
                height=self.mm(18
                               )
            )

            cnv.line(self.mm(102), self.mm(268 - contador), self.mm(102), self.mm(198 - contador))  # Linha central
            cnv.line(self.mm(196), self.mm(268 - contador), self.mm(196), self.mm(188 - contador))  # linha direita
            cnv.line(self.mm(8), self.mm(268 - contador), self.mm(8), self.mm(188 - contador))  # linha esquerda
            cnv.line(self.mm(25), self.mm(268 - contador), self.mm(25), self.mm(258 - contador))  # divisão linha 1.1
            cnv.line(self.mm(52), self.mm(268 - contador), self.mm(52), self.mm(258 - contador))  # divisão linha 1.2
            cnv.line(self.mm(78), self.mm(268 - contador), self.mm(78), self.mm(258 - contador))  # divisão linha 1.3
            cnv.line(self.mm(119), self.mm(268 - contador), self.mm(119), self.mm(258 - contador))  # divisão linha 1.4
            cnv.line(self.mm(142), self.mm(268 - contador), self.mm(142), self.mm(258 - contador))  # divisão linha 1.5
            cnv.line(self.mm(168), self.mm(268 - contador), self.mm(168), self.mm(258 - contador))  # divisão linha 1.6
            cnv.line(self.mm(8), self.mm(258 - contador), self.mm(196), self.mm(258 - contador))  # linha horizontal 1
            cnv.line(self.mm(8), self.mm(248 - contador), self.mm(196), self.mm(248 - contador))  # linha horizontal 2
            cnv.line(self.mm(8), self.mm(238 - contador), self.mm(196), self.mm(238 - contador))  # linha horizontal 3
            cnv.line(self.mm(8), self.mm(228 - contador), self.mm(102),
                     self.mm(228 - contador))  # meia linha horizontal 1
            cnv.line(self.mm(8), self.mm(218 - contador), self.mm(196), self.mm(218 - contador))  # linha horizontal 4
            cnv.line(self.mm(8), self.mm(208 - contador), self.mm(196), self.mm(208 - contador))  # linha horizontal 5
            cnv.line(self.mm(8), self.mm(203 - contador), self.mm(196), self.mm(203 - contador))  # linha horizontal 6
            cnv.line(self.mm(8), self.mm(198 - contador), self.mm(196), self.mm(198 - contador))  # linha horizontal 7
            cnv.line(self.mm(8), self.mm(193 - contador), self.mm(196), self.mm(193 - contador))  # linha horizontal 8
            cnv.line(self.mm(8), self.mm(188 - contador), self.mm(196), self.mm(188 - contador))  # linha horizontal 9
            cnv.line(self.mm(8), self.mm(183 - contador), self.mm(8),
                     self.mm(178 - contador))  # linha vertical id esquerda
            cnv.line(self.mm(75), self.mm(183 - contador), self.mm(75),
                     self.mm(178 - contador))  # linha vertica id direita
            cnv.line(self.mm(8), self.mm(178 - contador), self.mm(75), self.mm(178 - contador))  # linha horizontal id
            cnv.line(self.mm(8), self.mm(163 - contador), self.mm(196),
                     self.mm(163 - contador))  # linha horizontal assinatura
            cnv.line(self.mm(102), self.mm(172 - contador), self.mm(102),
                     self.mm(163 - contador))  # linha vertical assinatura

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
            cnv.drawString(self.mm(144), self.mm(265 - contador), "Nº Conta Favorecido")
            cnv.drawString(self.mm(170), self.mm(265 - contador), "Valor")
            cnv.drawString(self.mm(10), self.mm(255 - contador), "Nome do(s) Remetente(s)")
            cnv.drawString(self.mm(104), self.mm(255 - contador), "Nome do(s) Destinatário(s)")
            cnv.drawString(self.mm(10), self.mm(245 - contador), "CNPJ/CPF(s)")
            cnv.drawString(self.mm(104), self.mm(245 - contador), "CNPJ/CPF(s)")
            cnv.drawString(self.mm(10), self.mm(235 - contador), "Nº identidade / Órgão expedidor / UF")
            cnv.drawString(self.mm(104), self.mm(235 - contador), "Valor por Extenso")
            cnv.drawString(self.mm(10), self.mm(225 - contador), "Endereço")
            cnv.drawString(self.mm(10), self.mm(215 - contador), "Telefone(s)")
            cnv.drawString(self.mm(104), self.mm(215 - contador), "Nº Identidade / Órgão expedidor / UF")
            cnv.drawString(self.mm(10), self.mm(205 - contador), "Tipo Pessoa Debitada")
            cnv.drawString(self.mm(10), self.mm(200 - contador), "Tipo Conta Debitada")
            cnv.drawString(self.mm(104), self.mm(205 - contador), "Tipo Pessoa Creditada")
            cnv.drawString(self.mm(104), self.mm(200 - contador), "Tipo Conta Creditada")
            cnv.drawString(self.mm(10), self.mm(195 - contador), "Finalidade")
            cnv.drawString(self.mm(10), self.mm(190 - contador), "Histórico")
            cnv.drawString(self.mm(10), self.mm(185 - contador), "Nº Identificação Depósito")
            cnv.drawString(self.mm(155), self.mm(185 - contador), f"{pagamento[0][0:3]}-{self.formatar_nome(pagamento[1])} {pagamento[2]}")
            cnv.drawString(self.mm(155), self.mm(182 - contador), f"Impresso em {self.data_formatada}")
            cnv.drawString(self.mm(76), self.mm(180 - contador), "Preencher somente nas transferências de recursos para deposito judicial")
            cnv.drawString(self.mm(10), self.mm(175 - contador), "Autorizo o Banco a DEBITAR em minha Conta de Depósitos, nesta Agência, o valor da presente transferência de fundos.")
            cnv.drawString(self.mm(17), self.mm(160 - contador), "Diego Fernandes da Silva - Diretor Administrativo - Matrícula: 1.693.844-5")
            cnv.drawString(self.mm(114), self.mm(160 - contador), "Willy Pereira da Silva Filho - Superintendente - Matrícula 1.680.762-6")

            # nome_destinatário
            cnv.setFont("Times-Bold", 7)
            nome_teste = f"{empresa[0]}"
            nome = self.alinhar_texto(nome_teste)

            calc = 0
            for i in nome:
                cnv.drawString(self.mm(104), self.mm((252 - contador) - calc), i)
                calc += 3

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
            cnv.drawString(self.mm(71), self.mm(205 - contador), "\u2713")
            cnv.drawString(self.mm(41), self.mm(200 - contador), "\u2713")
            cnv.drawString(self.mm(171), self.mm(205 - contador), "\u2713")
            cnv.drawString(self.mm(141), self.mm(200 - contador), "\u2713")
            cnv.drawString(self.mm(106), self.mm(195 - contador), "\u2713")
            cnv.drawString(self.mm(10), self.mm(221 - contador),
                           "Área especial nº 01, Lote Único - Setor Central Gama/DF. CEP: 72.405-901")



            cnv.setFont("Times-Bold", 10)
            cnv.drawString(self.mm(115), self.mm(275 - contador), 'Transferência Eletrônica Disponível - TED -"E"')
            cnv.line(self.mm(8), self.mm(273 - contador), self.mm(196), self.mm(273 - contador))
            cnv.drawString(self.mm(10), self.mm(269 - contador), 'Instituição Financeira Remetente')
            cnv.drawString(self.mm(104), self.mm(269 - contador), 'Instituição Financeira Destinatária')
            cnv.drawString(self.mm(84), self.mm(155 - contador), 'Assinatura do Remetente')

            print(f"{conta} empresa {empresa}")

            #contas
            cnv.drawString(self.mm(10), self.mm(260 - contador), f"{conta[0][3]}") #banco
            cnv.drawString(self.mm(27), self.mm(260 - contador), f"{conta[0][4]}") #agência

            conta_tratada = self.formatar_conta(conta[0][5])
            cnv.drawString(self.mm(54), self.mm(260 - contador), f"{conta_tratada}") #conta
            cnv.drawString(self.mm(10), self.mm(250 - contador), f"{origem}") #origem

            cnpj_regional = self.formatar_cnpj(conta[0][6])
            cnv.drawString(self.mm(10), self.mm(240 - contador), f"{cnpj_regional}") #CNPJ - regional


            #fornecedor
            cnv.drawString(self.mm(104), self.mm(260 - contador), f"{empresa[6]}") #banco
            cnv.drawString(self.mm(121), self.mm(260 - contador), f"{empresa[7]}") #agência
            cnv.drawString(self.mm(144), self.mm(260 - contador), f"{empresa[8]}") #conta
            cnv.drawString(self.mm(104), self.mm(240 - contador), f"{empresa[4]}") #CNPJ - fornecedor
            cnv.drawString(self.mm(10), self.mm(210 - contador), "(61) 2017-1821") #telefone

            #dados
            cnv.drawString(self.mm(170), self.mm(260 - contador), f"R$ {self.formartar_valor(pagamento[3])}") #valor
            cnv.drawString(self.mm(46), self.mm(189 - contador), f"{pagamento[4]}") #CNPJ - empresa
            cnv.drawString(self.mm(121), self.mm(189 - contador), f"{pagamento[0]}") #cotação
            cnv.drawString(self.mm(161), self.mm(189 - contador), f"{pagamento[2]}") #danfe

            valor_teste = f"{pagamento[8]}"
            v_nome = self.alinhar_texto(valor_teste)

            calc = 0
            for i in v_nome:
                cnv.drawString(self.mm(104), self.mm((230 - contador) - calc), i)
                calc += 4

            cnv.setFont("Times-Bold", 12)
            cnv.drawString(self.mm(143), self.mm(281 - contador), f"{conta[0][1]} - {conta[0][2]}")
            contador += 143

        cnv.setDash([3, 1])
        cnv.line(self.mm(8), self.mm(149), self.mm(196), self.mm(149))
        cnv.save()

    def cria_transferencia(self, pagamento, empresa, conta, origem, data_pagamento):
        if not os.path.exists(f'{self.pasta}/guias/{origem}/{data_pagamento}/TBRB'):
            os.makedirs(f'{self.pasta}/guias/{origem}/{data_pagamento}/TBRB')

        cnv = canvas.Canvas(f'{self.pasta}/guias/{origem}/{data_pagamento}/TBRB/{pagamento[0][0:3]}-{pagamento[1]}-{pagamento[2]}.pdf')
        cnv.setPageSize(A4)

        contador = 0
        for i in range(0, 2):
            cnv.drawImage(
                f'{self.pasta}/Imagens/logo.png', self.mm(10), self.mm(275 - contador), width=self.mm(45),
                height=self.mm(14
                               )
            )

            cnv.line(self.mm(102), self.mm(268 - contador), self.mm(102), self.mm(208 - contador))  # Linha central
            cnv.line(self.mm(196), self.mm(268 - contador), self.mm(196), self.mm(198 - contador))  # linha direita
            cnv.line(self.mm(8), self.mm(268 - contador), self.mm(8), self.mm(198 - contador))  # linha esquerda
            #cnv.line(self.mm(25), self.mm(268 - contador), self.mm(25), self.mm(258 - contador))  # divisão linha 1.1
            cnv.line(self.mm(30), self.mm(268 - contador), self.mm(30), self.mm(258 - contador))  # divisão linha 1.2
            #cnv.line(self.mm(78), self.mm(268 - contador), self.mm(78), self.mm(258 - contador))  # divisão linha 1.3
            #cnv.line(self.mm(119), self.mm(268 - contador), self.mm(119), self.mm(258 - contador))  # divisão linha 1.4
            cnv.line(self.mm(124), self.mm(268 - contador), self.mm(124), self.mm(258 - contador))  # divisão linha 1.5
            cnv.line(self.mm(168), self.mm(268 - contador), self.mm(168), self.mm(258 - contador))  # divisão linha 1.6
            cnv.line(self.mm(8), self.mm(258 - contador), self.mm(196), self.mm(258 - contador))  # linha horizontal 1
            cnv.line(self.mm(8), self.mm(248 - contador), self.mm(196), self.mm(248 - contador))  # linha horizontal 2
            cnv.line(self.mm(8), self.mm(238 - contador), self.mm(196), self.mm(238 - contador))  # linha horizontal 3
            cnv.line(self.mm(8), self.mm(228 - contador), self.mm(102),
                     self.mm(228 - contador))  # meia linha horizontal 1
            cnv.line(self.mm(8), self.mm(218 - contador), self.mm(196), self.mm(218 - contador))  # linha horizontal 4
            cnv.line(self.mm(8), self.mm(213 - contador), self.mm(196), self.mm(213 - contador))  # linha horizontal 9
            cnv.line(self.mm(8), self.mm(208 - contador), self.mm(196), self.mm(208 - contador))  # linha horizontal 5
            cnv.line(self.mm(8), self.mm(203 - contador), self.mm(196), self.mm(203 - contador))  # linha horizontal 6
            cnv.line(self.mm(8), self.mm(198 - contador), self.mm(196), self.mm(198 - contador))  # linha horizontal 7
            #cnv.line(self.mm(8), self.mm(193 - contador), self.mm(196), self.mm(193 - contador))  # linha horizontal 8

            cnv.line(self.mm(8), self.mm(193 - contador), self.mm(8),
                     self.mm(188 - contador))  # linha vertical id esquerda
            cnv.line(self.mm(75), self.mm(193 - contador), self.mm(75),
                     self.mm(188 - contador))  # linha vertica id direita
            cnv.line(self.mm(8), self.mm(188 - contador), self.mm(75), self.mm(188 - contador))  # linha horizontal id
            cnv.line(self.mm(8), self.mm(173 - contador), self.mm(196),
                     self.mm(173 - contador))  # linha horizontal assinatura
            cnv.line(self.mm(102), self.mm(182 - contador), self.mm(102),
                     self.mm(173 - contador))  # linha vertical assinatura

            cnv.rect(self.mm(126), self.mm(281 - contador), width=self.mm(70), height=self.mm(7))
            cnv.rect(self.mm(40), self.mm(214 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(70), self.mm(214 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(40), self.mm(209 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(70), self.mm(209 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(140), self.mm(214 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(170), self.mm(214 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(140), self.mm(209 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(170), self.mm(209 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(25), self.mm(204 - contador), width=self.mm(3), height=self.mm(3))
            cnv.rect(self.mm(105), self.mm(204 - contador), width=self.mm(3), height=self.mm(3))

            cnv.setFont("Times-Roman", 7)
            cnv.drawString(self.mm(10), self.mm(265 - contador), "Agência")
            cnv.drawString(self.mm(32), self.mm(265 - contador), "Nº Conta Remetente")
            cnv.drawString(self.mm(104), self.mm(265 - contador), "Agência")
            cnv.drawString(self.mm(126), self.mm(265 - contador), "Nº Conta Favorecido")
            cnv.drawString(self.mm(170), self.mm(265 - contador), "Valor")
            cnv.drawString(self.mm(10), self.mm(255 - contador), "Nome do(s) Remetente(s)")
            cnv.drawString(self.mm(104), self.mm(255 - contador), "Nome do(s) Destinatário(s)")
            cnv.drawString(self.mm(10), self.mm(245 - contador), "CNPJ/CPF(s)")
            cnv.drawString(self.mm(104), self.mm(245 - contador), "CNPJ/CPF(s)")
            #cnv.drawString(self.mm(10), self.mm(235 - contador), "Nº identidade / Órgão expedidor / UF")
            cnv.drawString(self.mm(104), self.mm(235 - contador), "Valor por Extenso")
            cnv.drawString(self.mm(10), self.mm(235 - contador), "Endereço")
            cnv.drawString(self.mm(10), self.mm(225 - contador), "Telefone(s)")
            #cnv.drawString(self.mm(104), self.mm(215 - contador), "Nº Identidade / Órgão expedidor / UF")
            cnv.drawString(self.mm(10), self.mm(215 - contador), "Tipo Pessoa Debitada")
            cnv.drawString(self.mm(10), self.mm(210 - contador), "Tipo Conta Debitada")
            cnv.drawString(self.mm(104), self.mm(215 - contador), "Tipo Pessoa Creditada")
            cnv.drawString(self.mm(104), self.mm(210 - contador), "Tipo Conta Creditada")
            cnv.drawString(self.mm(10), self.mm(205 - contador), "Finalidade")
            cnv.drawString(self.mm(10), self.mm(200 - contador), "Histórico")
            cnv.drawString(self.mm(10), self.mm(195 - contador), "Nº Identificação Depósito")
            cnv.drawString(self.mm(155), self.mm(195 - contador),
                           f"{pagamento[0][0:3]}-{self.formatar_nome(pagamento[1])} {pagamento[2]}")
            cnv.drawString(self.mm(155), self.mm(192 - contador), f"Impresso em {self.data_formatada}")
            cnv.drawString(self.mm(76), self.mm(190 - contador),
                           "Preencher somente nas transferências de recursos para deposito judicial")
            cnv.drawString(self.mm(10), self.mm(185 - contador),
                           "Autorizo o Banco a DEBITAR em minha Conta de Depósitos, nesta Agência, o valor da presente transferência de fundos.")
            cnv.drawString(self.mm(17), self.mm(170 - contador),
                           "Diego Fernandes da Silva - Diretor Administrativo - Matrícula: 1.693.844-5")
            cnv.drawString(self.mm(114), self.mm(170 - contador),
                           "Willy Pereira da Silva Filho - Superintendente - Matrícula 1.680.762-6")

            # nome_destinatário
            cnv.setFont("Times-Bold", 7)
            nome_teste = f"{empresa[0]}"
            nome = self.alinhar_texto(nome_teste)

            calc = 0
            for i in nome:
                cnv.drawString(self.mm(104), self.mm((252 - contador) - calc), i)
                calc += 3

            cnv.setFont("Times-Roman", 8)
            cnv.drawString(self.mm(45), self.mm(214 - contador), "Pesssoa Física")
            cnv.drawString(self.mm(75), self.mm(214 - contador), "Pesssoa Jurídica")
            cnv.drawString(self.mm(45), self.mm(209 - contador), "Conta Corrente")
            cnv.drawString(self.mm(75), self.mm(209 - contador), "Conta Poupança")
            cnv.drawString(self.mm(145), self.mm(214 - contador), "Pesssoa Física")
            cnv.drawString(self.mm(175), self.mm(214 - contador), "Pesssoa Jurídica")
            cnv.drawString(self.mm(145), self.mm(209 - contador), "Conta Corrente")
            cnv.drawString(self.mm(175), self.mm(209 - contador), "Conta Poupança")
            cnv.drawString(self.mm(30), self.mm(204 - contador), "00001 - Pagamento de ipostos, tributos e taxas")
            cnv.drawString(self.mm(110), self.mm(204 - contador), "00005 - Pagamentos de fornecedores")
            cnv.drawString(self.mm(40), self.mm(199 - contador), "SEI:")
            cnv.drawString(self.mm(110), self.mm(199 - contador), "Cotação:")
            cnv.drawString(self.mm(150), self.mm(199 - contador), "DANFE:")

            cnv.setFont("Times-Bold", 8)
            cnv.drawString(self.mm(71), self.mm(215 - contador), "\u2713")
            cnv.drawString(self.mm(41), self.mm(210 - contador), "\u2713")
            cnv.drawString(self.mm(171), self.mm(215 - contador), "\u2713")
            cnv.drawString(self.mm(141), self.mm(210 - contador), "\u2713")
            cnv.drawString(self.mm(106), self.mm(205 - contador), "\u2713")
            cnv.drawString(self.mm(10), self.mm(230 - contador),
                           "Área especial nº 01, Lote Único - Setor Central Gama/DF. CEP: 72.405-901")

            cnv.setFont("Times-Bold", 10)
            cnv.drawString(self.mm(129), self.mm(278 - contador), 'Autorização para transferência de valores')
            cnv.drawString(self.mm(138), self.mm(274 - contador), 'entre contas no âmbito do BRB')
            cnv.line(self.mm(8), self.mm(273 - contador), self.mm(196), self.mm(273 - contador))
            cnv.drawString(self.mm(10), self.mm(269 - contador), 'Conta Remetente')
            cnv.drawString(self.mm(104), self.mm(269 - contador), 'Conta Destinatária')
            cnv.drawString(self.mm(84), self.mm(165 - contador), 'Assinatura do Remetente')

            # contas

            conta_tratada = self.formatar_conta(conta[0][5])
            #cnv.drawString(self.mm(10), self.mm(260 - contador), f"{conta[0][3]}")  # banco
            cnv.drawString(self.mm(10), self.mm(260 - contador), f"{conta[0][4]}")  # agência
            cnv.drawString(self.mm(32), self.mm(260 - contador), f"{conta_tratada}")  # conta
            cnv.drawString(self.mm(10), self.mm(250 - contador), f"{origem}")  # origem

            cnpj_regional = self.formatar_cnpj(conta[0][6])
            cnv.drawString(self.mm(10), self.mm(240 - contador), f"{cnpj_regional}")  # CNPJ - regional

            # fornecedor
            #cnv.drawString(self.mm(104), self.mm(260 - contador), f"{empresa[6]}")  # banco
            cnv.drawString(self.mm(104), self.mm(260 - contador), f"{empresa[7]}")  # agência
            cnv.drawString(self.mm(126), self.mm(260 - contador), f"{empresa[8]}")  # conta
            cnv.drawString(self.mm(104), self.mm(240 - contador), f"{empresa[4]}")  # CNPJ - fornecedor
            cnv.drawString(self.mm(10), self.mm(220 - contador), "(61) 2017-1821")  # telefone

            # dados
            cnv.drawString(self.mm(170), self.mm(260 - contador), f"R$ {self.formartar_valor(pagamento[3])}")  # valor
            cnv.drawString(self.mm(46), self.mm(199 - contador), f"{pagamento[4]}")  #nº SEI
            cnv.drawString(self.mm(121), self.mm(199 - contador), f"{pagamento[0]}")  # cotação
            cnv.drawString(self.mm(161), self.mm(199 - contador), f"{pagamento[2]}")  # danfe

            valor_teste = f"{pagamento[8]}"
            v_nome = self.alinhar_texto(valor_teste)

            calc = 0
            for i in v_nome:
                cnv.drawString(self.mm(104), self.mm((230 - contador) - calc), i)
                calc += 4

            cnv.setFont("Times-Bold", 12)
            cnv.drawString(self.mm(146), self.mm(283 - contador), f"{conta[0][1]} - {conta[0][2]}")
            contador += 143

        cnv.setDash([3, 1])
        cnv.line(self.mm(8), self.mm(155), self.mm(196), self.mm(155))
        cnv.save()

    def gerar_teds(self, origem, data_pagamento):
        self.pagamentos = self.soma_valor_liquido(self.definir_fonte(origem))
        self.empresas = self.fornecedores(self.definir_fonte(origem))

        for pag in self.pagamentos.keys():
            print(f'{pag} - valor total: R$ {self.pagamentos[pag]}')

        for empresa in self.pagamentos.keys():
             print(empresa)
             contador = 0
             for pagamento in self.pagamentos[empresa]:
                 if isinstance(pagamento, int):
                     continue
                 else:
                     print(f'   {contador} - {pagamento}')
                     contador += 1

        #         dados_empresa = self.empresas[pagamento[0][1]]
        #         print(dados_empresa)
        #         codigo = pagamento[5]
        #         conta = self.pegar_conta(origem, codigo)
        #         banco = self.empresas[pagamento[1]][5]
        #         nome_empresa = pagamento[1]
        #         if (banco) == "BRB":
        #             self.cria_transferencia(pagamento, dados_empresa, conta, origem, data_pagamento)
        #         else:
        #             self.criar_ted(pagamento, dados_empresa, conta, origem, data_pagamento)
        #         if pagamento[6] != 0:
        #             dados_iss = self.empresas['ISS ()']
        #             pagamento[1] = pagamento[1] + ' ISS'
        #             pagamento[3] = pagamento[6]
        #             pagamento[8] = pagamento[9]
        #             self.cria_transferencia(pagamento, dados_iss, conta, origem, data_pagamento)
        #         if pagamento[7] != 0:
        #             dados_ir = self.empresas['IR ()']
        #             pagamento[1] = pagamento[1][0:-3] + ' IR'
        #             pagamento[3] = pagamento[7]
        #             pagamento[8] = pagamento[10]
        #             self.cria_transferencia(pagamento, dados_ir, conta, origem, data_pagamento)



if __name__ == '__main__':
    r = Relatorio()
    #a = r.fornecedores()
    #a = r.soma_valor_liquido()
    #print(a)
    #r.criar_ted()
    #nome_teste = "CIA SUPRIMENTOS (AEJ IMPORTAÇÃO E EXPORTAÇÃO DE MATERIAIS HOSPITALARES E EDUCACIONAIS LTDA textoextragrandao para testar se o código realemente funciona com qualquer palavra enorme)"
    #r.alinhar_texto(nome_teste)
