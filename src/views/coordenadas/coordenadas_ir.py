LOGO = (10, 275, 45, 14)

LINHAS_ESTRUTURA = [
    (8, 273, 196, 273), #primeira linha superior
    (102, 268, 102, 230),  #Linha central
    (196, 268, 196, 230),  #linha direita
    (8, 268, 8, 230),  #linha esquerda
    (30, 268, 30, 264),  #divisão linha 1.2
    (148, 254, 148, 264),  #divisão linha 2.5
    (158, 268, 158, 264),  #divisão linha 1.6
    (8, 264, 196, 264),  #linha horizontal 1 258
    (80, 264, 80, 254),  #linha vertical telefone
    (8, 254, 196, 254),  #linha horizontal 2 248
    (133, 250, 133, 254),  #divisão linha 2.5
    (8, 250, 196, 250), #linha horizontal 3 238
    (8, 240, 102, 240),  #meia linha horizontal 1
    (102, 230, 196, 230),  #linha horizontal 4.5
    (8, 220, 196, 220),  #linha horizontal assinatura
    (102, 228, 102, 220),  #linha vertical assinatura
]

LINHAS_PAGAMENTOS = [
    (44, 128, 44, 131),
    (58, 128, 58, 131),
    (99, 128, 99, 131),
    (124, 128, 124, 131),
    (142, 128, 142, 131),
    (166, 128, 166, 131),
]

LINHASTPGAMENTO = [
    (44, 129, 44, 134),
    (58, 129, 58, 134),
    (99, 129, 99, 134),
    (124, 129, 124, 134),
    (142, 129, 142, 134),
    (166, 129, 166, 134),
]

RETANGULOS = [
    (140, 281, 56, 7)
]

RETANGULOSTITULO = [
    (12, 131, 180, 3.5)
]

RETANGULO_PAGAMENTO = [
    (12, 127.5, 180, 3.5)
]


# Strings
TIMES6 = []

TIMES7 = [
    (10, 265, "Agência"),
    (32, 265, "Conta"),
    (160, 265, "Valor"),
    (10, 261, "Identificação de conta"),
    (104, 261, "Tipo Conta Debitada"),
    (150, 261, "Tipo Conta Creditada"),
    (10, 251, "CNPJ/CPF(s)"),
    (104, 251, "Histórico"),
    (135, 251, "Finalidade"),
    (104, 247, "Valor por Extenso"),
    (10, 247, "Endereço"),
    (82, 261, "Telefone(s)"),
    (10, 237, (
        "Autorizo o Banco a DEBITAR em minha Conta"
        " de Depósitos, nesta Agência, o valor total"
    )
     ),
    (10, 234, (
        "indicado para realizar o presente pagamento."
    )
     ),
    (17, 221, (
        "Paulo Emanuel Oliveira de Sousa - "
        "Diretor Administrativo - Ma"
        "trícula: 1.714.143-5"
    )
     ),
    (114, 221, (
        "Willy Pereira da Silva Filho - "
        "Superintendente - Matrícula 1.680.762-6"
    )
     )
]

TIMES7DATA = [(75, 231, 'Data_impressão')]

TIMESB7NOMEEMPRESA = (
    # 104, 258
)

TIMESB7EXTENSO = (104, 242)

TIMES8 = []

TIMESB8 = [
    (10, 242, (
        "Área especial nº 01, Lote Único - "
        "Setor Central Gama/DF. CEP: 72.405-901"
    )
     ),
    (82, 256, "(61) 3449-7105"),  #telefone
    (104, 265, "Retenção de IR"),
    (104, 256, "Conta corrente/Pessoa Jurídica"),
    (146, 251, " Pagamento de impostos, tributos e taxas"),
    (150, 256, "Conta corrente/Pessoa Jurídica"),
]

TIMES8_PAGAMENTOS = [
    (13, 128.5, 4), #Nº processo SEI
    (45, 128.5, 0), #cotação
    (59, 128.5, 1), #empresa
    (100, 128.5, -1), #CNPJ
    (125, 128.5, 2), #DANFE
    (143, 128.5, 8), #valor total
    (167, 128.5, 7), #IR

]

TIMESB8CONTA = [
    (19, 265, 4), #agência
    (39, 265, 5), #conta
    (10, 256, 0),  #origem
    (39, 256, 1),  #tipo
    (25, 251, 6),  #CNPJ - regional
]

TIMESB8FORNECEDOR = [
    # (113, 265, 7), #agência
    # (148, 265, 8), #conta
    # (119, 251, 4)  #CNPJ - fornecedor
]

TIMESBVALORTOTAL = [(169, 265, 'Valor_total')]  #valor

TIMESB8ALINHADO = [
    (104, 258, 'Nome_empresa')
]

TIMESB8HISTORICO = [(114, 251, 'Empresa')]

TIMESB9 = [
    (150, 276, 'Autorização de pagamento'),
    # (138, 274, 'entre contas no âmbito do BRB'),
    (10, 269, 'Conta Remetente'),
    (104, 269, 'Destinação'),
    (84, 216, 'Assinatura do Remetente'),
]

TIMESB9PAGAMENTO = [
    (27, 132, "SEI"),
    (46, 132, "Cotação"),
    (73, 132, "Empresa"),
    (108, 132, "CNPJ"),
    (127, 132, "DANFE"),
    (146, 132, "Valor total"),
    (176, 132, "IR"),
    (10, 217, "Via BRB"),
    (10, 137, "Via Correntista"),
]

TIMESB12 = [
    (142, 283, 0),
    (178, 283, 1)
]

PONTILHADO = (8, 213, 196, 213)