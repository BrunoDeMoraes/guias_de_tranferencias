from typing import Dict

from src.models.repository.dados_de_conta import DadosDeContas
from src.views.guia_interna import GuiaDeTransferenciaInterna
from src.controllers.tr_interna_controller import TrInternaController


def interna_constructor(entrada: Dict):
    data_pagameto = entrada['data']
    origem = entrada['origem']
    contas = DadosDeContas()
    fornecedores = None
    pagamentos = None
    remetente = entrada['remetente'],
    valor = entrada['valor'],
    favorecido = entrada['favorecido']

    tranferencias = TrInternaController(contas, data_pagameto, fornecedores, origem, pagamentos, remetente, valor, favorecido)
    dados_de_tranferencias = tranferencias.filtrar_dados()

    for dicionario in dados_de_tranferencias:
        logo = 'logo.png'
        guia = GuiaDeTransferenciaInterna(dicionario, logo)
        guia.gerar_guia(100)
    if pagamentos:
        return 'DEU CERTO!!!'
    else:
        return 'Deu merda!!!'
