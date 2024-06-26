from typing import Dict

from src.models.repository.dados_de_conta import DadosDeContas
from src.models.repository.dados_de_fornecedores import DadosDeFornecedores
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository
from src.views.guia import Guia
from src.controllers.transfer_contoller import TransferController


def transfer_constructor(entrada: Dict):
    data_pagameto = entrada['data']
    origem = entrada['origem']
    contas = DadosDeContas()
    fornecedores = DadosDeFornecedores()
    pagamentos = DadosDePagamentoRepository()

    tranferencias = TransferController(contas, data_pagameto, fornecedores, origem, pagamentos)
    dados_de_tranferencias = tranferencias.filtrar_dados()

    for dicionario in dados_de_tranferencias:
        logo = 'logo.png'
        guia = Guia(dicionario, logo)
        guia.gerar_guia(100, 'transferencia')
    if pagamentos:
        return 'DEU CERTO!!!'
    else:
        return 'Deu merda!!!'
