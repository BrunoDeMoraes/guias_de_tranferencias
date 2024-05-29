from src.controllers.interface_controller import InterfaceController
from typing import Type

from typing import Dict
# import dados_da_view
# import transfer_controller
from src.models.repository.dados_de_conta import DadosDeContas
from src.models.repository.dados_de_fornecedores import DadosDeFornecedores
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository
from src.views.guia_de_transferencia import Guia_de_transferencia

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


    def construir_guia(self):
        pagamentos = self.filtrar_dados()
        for pagamento in pagamentos.items():
            print(f'{pagamento[0]}\n')
            for pag in pagamento[1]:
                print(f'{pag}')
            print('\n')
            #Guia_de_transferencia()


    def filtrar_dados(self):
        fonte = self.contas.definir_fonte(self.origem)
        pagamentos = self.pagametos.agupar_por_empresa(fonte).items()
        transferencias = {}
        for pagamento in pagamentos:
            empresa = self.fornecedores.retorna_empresa(pagamento[0], fonte)
            if empresa[5] == 'BRB':
                transferencias[pagamento[0]] = pagamento[1]
        return transferencias






