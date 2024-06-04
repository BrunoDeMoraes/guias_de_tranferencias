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
        # pagamentos = self.separar_por_origem_de_recurso()
        for pagamento in pagamentos:
            for pag in pagamento.items():
                print(f'{pag[0]}: {pag[1]}')
            print('\n')
        # print(self.produto)
            #Guia_de_transferencia()


    def filtrar_dados(self):
        fonte = self.contas.definir_fonte(self.origem)
        pagamentos = self.pagametos.agupar_por_empresa(fonte)
        transferencias = []
        for pagamento in pagamentos.items():
            transferencia = {}
            empresa = self.fornecedores.retorna_empresa(pagamento[0], fonte)
            if empresa[5] == 'BRB':
                dados_empresa = self.fornecedores.retorna_empresa(pagamento[0], fonte)
                transferencia['Empresa'] = pagamento[0]
                transferencia['Pagamentos'] = pagamento[1]
                transferencia['Dados_empresa'] = dados_empresa
                transferencias.append(transferencia)
        return transferencias


    # def separar_por_origem_de_recurso(self):
    #     fonte = self.contas.definir_fonte(self.origem)
    #     pagamentos = self.pagametos.agupar_por_empresa(fonte)
    #     for pagamento in pagamentos.items():
    #         regular_custeio = []
    #         emenda_custeio = []
    #         regular_investimento = []
    #         emenda_investimento = []
    #         for pag in pagamento:









