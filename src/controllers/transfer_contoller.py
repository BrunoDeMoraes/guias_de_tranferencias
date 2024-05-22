from src.controllers.interface_controller import InterfaceController
from typing import Type

from typing import Dict
# import dados_da_view
# import transfer_controller
from src.models.repository.dados_de_conta import DadosDeContas
from src.models.repository.dados_de_fornecedores import DadosDeFornecedores
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository

class TransferController(InterfaceController):
    def __init__(
            self,
            contas: Type[DadosDeContas],
            data: str,
            fornecedores: Type[DadosDeFornecedores],
            origem: str,
            pagamento: Type[DadosDePagamentoRepository]
    ):
        super().__init__(contas, data, fornecedores, origem, pagamento)


    def filtrar_dados(self):
        pass

    def qua(self):
        print('qua')


if __name__ == "__main__":
    contas = DadosDeContas()
    data_pagameto = '25/05/2024'
    fornecedores = DadosDeFornecedores()
    origem = 'SRSSU'
    pagamementos = DadosDePagamentoRepository()
    a = TransferController(contas, data_pagameto, fornecedores, origem, pagamementos)
    a.qua()
    print(a.origem)

