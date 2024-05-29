from typing import Dict

from src.models.repository.dados_de_conta import DadosDeContas
from src.models.repository.dados_de_fornecedores import DadosDeFornecedores
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository
from src.views.guia_de_transferencia import Guia_de_transferencia

from src.controllers.transfer_contoller import TransferController


def transfer_constructor(entrada: Dict):
    contas = DadosDeContas()
    data_pagameto = entrada['data']
    fornecedores = DadosDeFornecedores()
    origem = entrada['origem']
    pagamentos = DadosDePagamentoRepository()

    tranferencias = TransferController(contas, data_pagameto, fornecedores, origem, pagamentos)
    tranferencias.construir_guia()

    # for tranferencia in tranferencias_prep:
    #     dados_de_compra
    #     dados_fornecedor
    #     dados_da_conta_ses
    #     Valor_tolta


    if pagamentos:
        return 'DEU CERTO!!!'
    else:
        return 'Deu merda!!!'


# fonte = 'C:/Users/14343258/PycharmProjects/guias_de_tranasferência/src/models/repository'





