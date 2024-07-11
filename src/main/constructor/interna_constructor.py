from typing import Dict

from src.models.repository.dados_de_conta import DadosDeContas
# from src.models.repository.dados_de_fornecedores import DadosDeFornecedores
# from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository
from src.views.guia_de_transferencia import GuiaDeTransferencia
from src.controllers.tr_interna_controller import TrInternaController


def interna_constructor(entrada: Dict):
    data_pagameto = entrada['data']
    origem = entrada['origem']
    contas = DadosDeContas()
    fornecedores = None
    pagamentos = None

    tranferencias = TrInternaController(contas, data_pagameto, fornecedores, origem, pagamentos)
    dados_de_tranferencias = tranferencias.filtrar_dados()

    for dicionario in dados_de_tranferencias:
        logo = 'logo.png'
        guia = GuiaDeTransferencia(dicionario, logo)
        guia.gerar_guia(100)
    if pagamentos:
        return 'DEU CERTO!!!'
    else:
        return 'Deu merda!!!'
