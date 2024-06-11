from typing import Dict

from src.models.repository.dados_de_conta import DadosDeContas
from src.models.repository.dados_de_fornecedores import DadosDeFornecedores
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository
from src.views.guia_de_ted import GuiaDeTED
from src.controllers.ted_controller import TedController


def ted_constructor(entrada: Dict):
    data_pagameto = entrada['data']
    origem = entrada['origem']
    contas = DadosDeContas()
    fornecedores = DadosDeFornecedores()
    pagamentos = DadosDePagamentoRepository()

    teds = TedController(contas, data_pagameto, fornecedores, origem, pagamentos)
    dados_de_ted = teds.filtrar_dados()

    for dicionario in dados_de_ted:
        logo = 'Logo_brb.jpg'
        guia = GuiaDeTED(dicionario, logo)
        guia.gerar_guia()
    if pagamentos:
        return 'DEU CERTO!!!'
    else:
        return 'Deu merda!!!'