LINHAS_ESTRUTURA = [
    (8, 273, 196, 273), # primeira linha superior
    (102, 268, 102, 220),  # Linha central
    (196, 268, 196, 220),  # linha direita
    (8, 268, 8, 220),  # linha esquerda
    (30, 268, 30, 264),  # divisão linha 1.2
    (124, 268, 124, 264),  # divisão linha 1.5
    (168, 268, 168, 264),  # divisão linha 1.6
    (8, 264, 196, 264),  # linha horizontal 1 258
    (80, 264, 80, 254),  # linha vertical telefone
    (8, 254, 196, 254),  # linha horizontal 2 248
    (8, 250, 196, 250), # linha horizontal 3 238
    (8, 240, 102, 240),  # meia linha horizontal 1
    (8, 235, 102, 235),  # linha horizontal 4
    (8, 230, 196, 230),  # linha horizontal 4.5
    (8, 225, 196, 225),  # linha horizontal 5
    (8, 220, 196, 220),  # linha horizontal 6
    (8, 214, 8, 219),  # linha vertical id esquerda
    (75, 214, 75, 219),  # linha vertica id direita
    (8, 214, 75, 214),  # linha horizontal id
    (8, 199, 196, 199),  # linha horizontal assinatura
    (102, 207, 102, 199),  # linha vertical assinatura
    (60, 84, 60, 89),
    (85, 84, 85, 89),
    (110, 84, 110, 89),
    (135, 84, 135, 89),
    (160, 84, 160, 89)
]

LINHAS_PAGAMENTOS = [
    (60, 79, 60, 84),
    (85, 79, 85, 84),
    (110, 79, 110, 84),
    (135, 79, 135, 84),
    (160, 79, 160, 84)
]

RETANGULOS = [
    (126, 281, 70, 7),
    (40, 226, 3, 3),
    (70, 226, 3, 3),
    (40, 221, 3, 3),
    (70, 221, 3, 3),
    (140, 226, 3, 3),
    (170, 226, 3, 3),
    (170, 226, 3, 3),
    (140, 221, 3, 3),
    (170, 221, 3, 3),
    (21, 236, 3, 3),
    (66, 236, 3, 3),
    (12, 84, 180, 5),
]

RETANGULO_PAGAMENTO = [
    (12, 79, 180, 5)
]


# Strings
TIMES6 = [
    (25, 237, "00001 - Pagamento de ipostos, tributos e taxas"),
    (70, 237, "00005 - Pagamentos de fornecedores")
]

TIMES7 = [
    (10, 265, "Agência"),
    (32, 265, "Nº Conta Remetente"),
    (104, 265, "Agência"),
    (126, 265, "Nº Conta Favorecido"),
    (170, 265, "Valor"),
    (10, 261, "Nome do(s) Remetente(s)"),
    (104, 261, "Nome do(s) Destinatário(s)"),
    (10, 251, "CNPJ/CPF(s)"),
    (104, 251, "CNPJ/CPF(s)"),
    (104, 247, "Valor por Extenso"),
    (10, 247, "Endereço"),
    (82, 261, "Telefone(s)"),
    (10, 227, "Tipo Pessoa Debitada"),
    (10, 222, "Tipo Conta Debitada"),
    (104, 227, "Tipo Pessoa Creditada"),
    (104, 222, "Tipo Conta Creditada"),
    (10, 237, "Finalidade"),
    (10, 232, "Histórico"),
    (10, 217, "Nº Identificação Depósito"),
    (155, 217, f"Impresso em {'self.data_formatada()'}"),
    (76, 216, (
        "Preencher somente nas transferências "
        "de recursos para deposito judicial"
    )
     ),
    (10, 211, (
        "Autorizo o Banco a DEBITAR em minha Conta"
        " de Depósitos, nesta Agência, o valor da "
        "presente transferência de fundos."
    )
     ),
    (17, 201, (
        "Diego Fernandes da Silva - "
        "Diretor Administrativo - Ma"
        "trícula: 1.693.844-5"
    )
     ),
    (114, 201, (
        "Willy Pereira da Silva Filho - "
        "Superintendente - Matrícula 1.680.762-6"
    )
     )
]

TIMES8 = [
    (21, 231, f'Não sei o que é'),
    (45, 226, "Pesssoa Física"),
    (75, 226, "Pesssoa Jurídica"),
    (45, 221, "Conta Corrente"),
    (75, 221, "Conta Poupança"),
    (145, 226, "Pesssoa Física"),
    (175, 226, "Pesssoa Jurídica"),
    (145, 221, "Conta Corrente"),
    (175, 221, "Conta Poupança")
]

TIMESB8 = [
    (71, 227, "\u2713"),
    (41, 222, "\u2713"),
    (171, 227, "\u2713"),
    (141, 222, "\u2713"),
    (67, 237, "\u2713"),
    (10, 242, (
        "Área especial nº 01, Lote Único - "
        "Setor Central Gama/DF. CEP: 72.405-901"
    )
     ),
    (82, 256, "(61) 2017-1821")  #telefone
]

TIMES8_PAGAMENTOS = [
    (21, 81, 4), #CNPJ
    (69, 81, 0), #cotação
    (91, 81, 2), #empresa
    (113, 81, 8), #valor bruto
    (163, 81, 3), #valor liquido
    (138, 81, -1) #ISS+IR
]

TIMESB8CONTA = [
            (19, 265, 4), #agência
            (53, 265, 5), #conta
            (10, 256, 0),  #origem
            (25, 251, 6),  #CNPJ - regional
]

TIMESB8FORNECEDOR = [
    (113, 265, 7), #agência
    (148, 265, 8), #conta
    (119, 251, 4)  #CNPJ - fornecedor
]

TIMESBVALORTOTAL = [(176, 265, 'Valor_total')]  #valor

TIMESB8ALINHADO = [
    (104, 258, 'Nome_empresa')
]

TIMESB9 = [
    (129, 278, 'Autorização para transferência de valores'),
    (138, 274, 'entre contas no âmbito do BRB'),
    (10, 269, 'Conta Remetente'),
    (104, 269, 'Conta Destinatária'),
    (84, 196, 'Assinatura do Remetente'),
    (35, 86, "SEI"),
    (68, 86, "Cotação"),
    (93, 86, "DANFE"),
    (116, 86, "Valor total"),
    (141, 86, "IRRF / ISS"),
    (168, 86, "Valor líquido"),


]


































