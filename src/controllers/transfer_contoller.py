from src.controllers.interface_controller import InterfaceController
from typing import Type
from typing import List

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


    def construir_guia(self):
        pagamentos = self.filtrar_dados()
        for pagamento in pagamentos:
            for pag in pagamento.items():
                print(f'{pag[0]}: {pag[1]}')
            print('\n')


    def filtrar_dados(self):
        fonte = self.contas.definir_fonte(self.origem)
        pagamentos = self.pagametos.agupar_por_empresa(fonte)
        transferencias = []
        for pagamento in pagamentos.items():
            transferencia = {}
            empresa = self.fornecedores.retorna_empresa(pagamento[0], fonte)
            if empresa[5] == 'BRB':
                dados_empresa = self.fornecedores.retorna_empresa(pagamento[0], fonte)
                conta_origem = self.contas.pegar_conta(self.origem, pagamento[0][-2:])
                valor_total = self.valor_total(pagamento[1])
                transferencia['Empresa'] = pagamento[0]
                transferencia['Pagamentos'] = pagamento[1]
                transferencia['Dados_empresa'] = dados_empresa
                transferencia['Conta_origem'] = conta_origem
                transferencia['Valor_total'] = valor_total
                transferencias.append(transferencia)
        return transferencias

    def valor_total(self, pagamentos: List) -> float:
        total = 0
        for pagamento in pagamentos:
            total += pagamento[3]
        return total















