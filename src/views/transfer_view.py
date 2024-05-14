def cria_transferencia(self, pagamento, empresa, conta, origem, data_pagamento):
    print(
        f'Criei uma Transferência da {empresa}\nConta: {conta}\nTipo: {origem}\nData: {data_pagamento}\nPagamentos contidos {pagamento}\n\n')
    if not os.path.exists(f'{self.pasta}/guias/{origem}/{data_pagamento}/TBRB'):
        os.makedirs(f'{self.pasta}/guias/{origem}/{data_pagamento}/TBRB')

    cnv = canvas.Canvas(
        f'{self.pasta}/guias/{origem}/{data_pagamento}/TBRB/{pagamento[0][1]}-{conta[1]}-{conta[2]}.pdf')
    cnv.setPageSize(A4)

    contador = 0
    for i in range(0, 2):
        cnv.drawImage(
            f'{self.pasta}/Imagens/logo.png', self.mm(10), self.mm(275 - contador), width=self.mm(45),
            height=self.mm(14))

        cnv.line(self.mm(8), self.mm(273 - contador), self.mm(196), self.mm(273 - contador))  # primeira linha superior

        cnv.line(self.mm(102), self.mm(268 - contador), self.mm(102), self.mm(220 - contador))  # Linha central
        cnv.line(self.mm(196), self.mm(268 - contador), self.mm(196), self.mm(220 - contador))  # linha direita
        cnv.line(self.mm(8), self.mm(268 - contador), self.mm(8), self.mm(220 - contador))  # linha esquerda

        # cnv.line(self.mm(25), self.mm(268 - contador), self.mm(25), self.mm(258 - contador))  # divisão linha 1.1
        cnv.line(self.mm(30), self.mm(268 - contador), self.mm(30), self.mm(264 - contador))  # divisão linha 1.2
        # cnv.line(self.mm(78), self.mm(268 - contador), self.mm(78), self.mm(258 - contador))  # divisão linha 1.3
        # cnv.line(self.mm(119), self.mm(268 - contador), self.mm(119), self.mm(258 - contador))  # divisão linha 1.4
        cnv.line(self.mm(124), self.mm(268 - contador), self.mm(124), self.mm(264 - contador))  # divisão linha 1.5
        cnv.line(self.mm(168), self.mm(268 - contador), self.mm(168), self.mm(264 - contador))  # divisão linha 1.6

        cnv.line(self.mm(8), self.mm(264 - contador), self.mm(196), self.mm(264 - contador))  # linha horizontal 1 258
        cnv.line(self.mm(80), self.mm(264 - contador), self.mm(80), self.mm(254 - contador))  # linha vertical telefone
        cnv.line(self.mm(8), self.mm(254 - contador), self.mm(196), self.mm(254 - contador))  # linha horizontal 2 248
        cnv.line(self.mm(8), self.mm(250 - contador), self.mm(196), self.mm(250 - contador))  # linha horizontal 3 238
        cnv.line(self.mm(8), self.mm(240 - contador), self.mm(102),
                 self.mm(240 - contador))  # meia linha horizontal 1
        cnv.line(self.mm(8), self.mm(235 - contador), self.mm(102), self.mm(235 - contador))  # linha horizontal 4
        cnv.line(self.mm(8), self.mm(230 - contador), self.mm(196), self.mm(230 - contador))  # linha horizontal 4.5
        cnv.line(self.mm(8), self.mm(225 - contador), self.mm(196), self.mm(225 - contador))  # linha horizontal 5
        cnv.line(self.mm(8), self.mm(220 - contador), self.mm(196), self.mm(220 - contador))  # linha horizontal 6

        cnv.line(self.mm(8), self.mm(214 - contador), self.mm(8),
                 self.mm(219 - contador))  # linha vertical id esquerda
        cnv.line(self.mm(75), self.mm(214 - contador), self.mm(75),
                 self.mm(219 - contador))  # linha vertica id direita
        cnv.line(self.mm(8), self.mm(214 - contador), self.mm(75), self.mm(214 - contador))  # linha horizontal id

        cnv.line(self.mm(8), self.mm(199 - contador), self.mm(196),
                 self.mm(199 - contador))  # linha horizontal assinatura
        cnv.line(self.mm(102), self.mm(207 - contador), self.mm(102),
                 self.mm(199 - contador))  # linha vertical assinatura

        cnv.rect(self.mm(126), self.mm(281 - contador), width=self.mm(70), height=self.mm(7))
        cnv.rect(self.mm(40), self.mm(226 - contador), width=self.mm(3), height=self.mm(3))
        cnv.rect(self.mm(70), self.mm(226 - contador), width=self.mm(3), height=self.mm(3))
        cnv.rect(self.mm(40), self.mm(221 - contador), width=self.mm(3), height=self.mm(3))
        cnv.rect(self.mm(70), self.mm(221 - contador), width=self.mm(3), height=self.mm(3))
        cnv.rect(self.mm(140), self.mm(226 - contador), width=self.mm(3), height=self.mm(3))
        cnv.rect(self.mm(170), self.mm(226 - contador), width=self.mm(3), height=self.mm(3))
        cnv.rect(self.mm(140), self.mm(221 - contador), width=self.mm(3), height=self.mm(3))
        cnv.rect(self.mm(170), self.mm(221 - contador), width=self.mm(3), height=self.mm(3))
        cnv.rect(self.mm(21), self.mm(236 - contador), width=self.mm(3), height=self.mm(3))
        cnv.rect(self.mm(66), self.mm(236 - contador), width=self.mm(3), height=self.mm(3))

        cnv.rect(self.mm(12), self.mm(84), width=self.mm(180), height=self.mm(5))
        cnv.line(self.mm(60), self.mm(84), self.mm(60),
                 self.mm(89))
        cnv.line(self.mm(85), self.mm(84), self.mm(85),
                 self.mm(89))
        cnv.line(self.mm(110), self.mm(84), self.mm(110),
                 self.mm(89))
        cnv.line(self.mm(135), self.mm(84), self.mm(135),
                 self.mm(89))
        cnv.line(self.mm(160), self.mm(84), self.mm(160),
                 self.mm(89))

        cnv.setFont("Times-Roman", 8)
        altura = 0
        total_pagamento = 0
        for dados in pagamento:
            cnv.drawString(self.mm(21), self.mm(81 - altura), f'{dados[4]}')
            cnv.drawString(self.mm(69), self.mm(81 - altura), f'{dados[0]}')
            cnv.drawString(self.mm(91), self.mm(81 - altura), f'{dados[2]}')
            cnv.drawString(self.mm(113), self.mm(81 - altura), f'R$ {self.formartar_valor(dados[8])}')
            cnv.drawString(self.mm(138), self.mm(81 - altura), f'R$ {self.formartar_valor((dados[6] + dados[7]))}')
            cnv.drawString(self.mm(163), self.mm(81 - altura), f'R$ {self.formartar_valor(dados[3])}')
            total_pagamento += dados[3]

            cnv.rect(self.mm(12), self.mm(79 - altura), width=self.mm(180), height=self.mm(5))
            cnv.line(self.mm(60), self.mm(79 - altura), self.mm(60),
                     self.mm(84 - altura))
            cnv.line(self.mm(85), self.mm(79 - altura), self.mm(85),
                     self.mm(84 - altura))
            cnv.line(self.mm(110), self.mm(79 - altura), self.mm(110),
                     self.mm(84 - altura))
            cnv.line(self.mm(135), self.mm(79 - altura), self.mm(135),
                     self.mm(84 - altura))
            cnv.line(self.mm(160), self.mm(79 - altura), self.mm(160),
                     self.mm(84 - altura))
            altura += 5

        cnv.setFont("Times-Roman", 6)
        cnv.drawString(self.mm(25), self.mm(237 - contador), "00001 - Pagamento de ipostos, tributos e taxas")
        cnv.drawString(self.mm(70), self.mm(237 - contador), "00005 - Pagamentos de fornecedores")

        #
        cnv.setFont("Times-Roman", 7)
        cnv.drawString(self.mm(10), self.mm(265 - contador), "Agência")
        cnv.drawString(self.mm(32), self.mm(265 - contador), "Nº Conta Remetente")
        cnv.drawString(self.mm(104), self.mm(265 - contador), "Agência")
        cnv.drawString(self.mm(126), self.mm(265 - contador), "Nº Conta Favorecido")
        cnv.drawString(self.mm(170), self.mm(265 - contador), "Valor")
        cnv.drawString(self.mm(10), self.mm(261 - contador), "Nome do(s) Remetente(s)")
        cnv.drawString(self.mm(104), self.mm(261 - contador), "Nome do(s) Destinatário(s)")
        cnv.drawString(self.mm(10), self.mm(251 - contador), "CNPJ/CPF(s)")
        cnv.drawString(self.mm(104), self.mm(251 - contador), "CNPJ/CPF(s)")
        # cnv.drawString(self.mm(10), self.mm(235 - contador), "Nº identidade / Órgão expedidor / UF")
        cnv.drawString(self.mm(104), self.mm(247 - contador), "Valor por Extenso")
        cnv.drawString(self.mm(10), self.mm(247 - contador), "Endereço")
        cnv.drawString(self.mm(82), self.mm(261 - contador), "Telefone(s)")
        # cnv.drawString(self.mm(104), self.mm(215 - contador), "Nº Identidade / Órgão expedidor / UF")
        cnv.drawString(self.mm(10), self.mm(227 - contador), "Tipo Pessoa Debitada")
        cnv.drawString(self.mm(10), self.mm(222 - contador), "Tipo Conta Debitada")
        cnv.drawString(self.mm(104), self.mm(227 - contador), "Tipo Pessoa Creditada")
        cnv.drawString(self.mm(104), self.mm(222 - contador), "Tipo Conta Creditada")
        cnv.drawString(self.mm(10), self.mm(237 - contador), "Finalidade")
        cnv.drawString(self.mm(10), self.mm(232 - contador), "Histórico")
        cnv.drawString(self.mm(10), self.mm(217 - contador), "Nº Identificação Depósito")
        # cnv.drawString(self.mm(155), self.mm(195 - contador),
        #                f"{pagamento[0][0:3]}-{self.formatar_nome(pagamento[1])} {pagamento[2]}")
        cnv.drawString(self.mm(155), self.mm(217 - contador), f"Impresso em {self.data_formatada()}")
        cnv.drawString(self.mm(76), self.mm(216 - contador),
                       "Preencher somente nas transferências de recursos para deposito judicial")
        cnv.drawString(self.mm(10), self.mm(211 - contador),
                       "Autorizo o Banco a DEBITAR em minha Conta de Depósitos, nesta Agência, o valor da presente transferência de fundos.")
        cnv.drawString(self.mm(17), self.mm(201 - contador),
                       "Diego Fernandes da Silva - Diretor Administrativo - Matrícula: 1.693.844-5")
        cnv.drawString(self.mm(114), self.mm(201 - contador),
                       "Willy Pereira da Silva Filho - Superintendente - Matrícula 1.680.762-6")

        # nome_destinatário
        cnv.setFont("Times-Bold", 7)
        nome_teste = f"{empresa[0]}"
        nome = self.alinhar_texto(nome_teste)

        calc = 0
        for i in nome:
            cnv.drawString(self.mm(104), self.mm((258 - contador) - calc), i)
            calc += 3

        cnv.setFont("Times-Roman", 8)
        cnv.drawString(self.mm(21), self.mm(231 - contador), f'{pagamento[0][1][0:-9]}')
        cnv.drawString(self.mm(45), self.mm(226 - contador), "Pesssoa Física")
        cnv.drawString(self.mm(75), self.mm(226 - contador), "Pesssoa Jurídica")
        cnv.drawString(self.mm(45), self.mm(221 - contador), "Conta Corrente")
        cnv.drawString(self.mm(75), self.mm(221 - contador), "Conta Poupança")
        cnv.drawString(self.mm(145), self.mm(226 - contador), "Pesssoa Física")
        cnv.drawString(self.mm(175), self.mm(226 - contador), "Pesssoa Jurídica")
        cnv.drawString(self.mm(145), self.mm(221 - contador), "Conta Corrente")
        cnv.drawString(self.mm(175), self.mm(221 - contador), "Conta Poupança")

        cnv.setFont("Times-Bold", 8)
        cnv.drawString(self.mm(71), self.mm(227 - contador), "\u2713")
        cnv.drawString(self.mm(41), self.mm(222 - contador), "\u2713")
        cnv.drawString(self.mm(171), self.mm(227 - contador), "\u2713")
        cnv.drawString(self.mm(141), self.mm(222 - contador), "\u2713")
        cnv.drawString(self.mm(67), self.mm(237 - contador), "\u2713")
        cnv.drawString(self.mm(10), self.mm(242 - contador),
                       "Área especial nº 01, Lote Único - Setor Central Gama/DF. CEP: 72.405-901")

        cnv.setFont("Times-Bold", 9)
        cnv.drawString(self.mm(129), self.mm(278 - contador), 'Autorização para transferência de valores')
        cnv.drawString(self.mm(138), self.mm(274 - contador), 'entre contas no âmbito do BRB')

        cnv.drawString(self.mm(10), self.mm(269 - contador), 'Conta Remetente')
        cnv.drawString(self.mm(104), self.mm(269 - contador), 'Conta Destinatária')
        cnv.drawString(self.mm(84), self.mm(196 - contador), 'Assinatura do Remetente')

        # contas

        conta_tratada = self.formatar_conta(conta[5])
        # cnv.drawString(self.mm(10), self.mm(260 - contador), f"{conta[0][3]}")  # banco
        cnv.drawString(self.mm(19), self.mm(265 - contador), f"{conta[4]}")  # agência
        cnv.drawString(self.mm(53), self.mm(265 - contador), f"{conta_tratada}")  # conta
        cnv.drawString(self.mm(10), self.mm(256 - contador), f"{origem}")  # origem

        cnpj_regional = self.formatar_cnpj(conta[6])
        print(f'Este é o problema {cnpj_regional}')
        cnv.drawString(self.mm(25), self.mm(251 - contador), f"{cnpj_regional}")  # CNPJ - regional

        # fornecedor
        # cnv.drawString(self.mm(104), self.mm(260 - contador), f"{empresa[6]}")  # banco
        cnv.drawString(self.mm(113), self.mm(265 - contador), f"{empresa[7]}")  # agência
        cnv.drawString(self.mm(148), self.mm(265 - contador), f"{empresa[8]}")  # conta
        cnv.drawString(self.mm(119), self.mm(251 - contador), f"{empresa[4]}")  # CNPJ - fornecedor
        cnv.drawString(self.mm(82), self.mm(256 - contador), "(61) 2017-1821")  # telefone

        # dados
        cnv.drawString(self.mm(176), self.mm(265 - contador), f"R$ {self.formartar_valor(total_pagamento)}")  # valor
        # cnv.drawString(self.mm(46), self.mm(199 - contador), f"{pagamento[4]}")  #nº SEI
        # cnv.drawString(self.mm(121), self.mm(199 - contador), f"{pagamento[0]}")  # cotação
        # cnv.drawString(self.mm(161), self.mm(199 - contador), f"{pagamento[2]}")  # danfe

        total_extenso = num2words(total_pagamento, lang='pt_BR', to='currency')
        v_nome = self.alinhar_texto(total_extenso)

        calc = 0
        for i in v_nome:
            cnv.drawString(self.mm(104), self.mm((242 - contador) - calc), i)
            calc += 4

        cnv.drawString(self.mm(35), self.mm(86), "SEI")
        cnv.drawString(self.mm(68), self.mm(86), "Cotação")
        cnv.drawString(self.mm(93), self.mm(86), "DANFE")
        cnv.drawString(self.mm(116), self.mm(86), "Valor total")
        cnv.drawString(self.mm(141), self.mm(86), "IRRF / ISS")
        cnv.drawString(self.mm(168), self.mm(86), "Valor líquido")

        cnv.setFont("Times-Bold", 12)
        cnv.drawString(self.mm(146), self.mm(283 - contador), f"{conta[1]} - {conta[2]}")

        contador += 100

    cnv.setDash([3, 1])
    cnv.line(self.mm(8), self.mm(192), self.mm(196), self.mm(192))
    cnv.save()