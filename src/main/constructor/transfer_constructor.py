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
    dados_de_tranferencias = tranferencias.filtrar_dados()

    for dicionario in dados_de_tranferencias:
        guia = Guia_de_transferencia(dicionario)
        guia.gerar_guia()
    if pagamentos:
        return 'DEU CERTO!!!'
    else:
        return 'Deu merda!!!'
