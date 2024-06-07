from src.controllers.interface_controller import InterfaceController
from typing import Dict
from typing import List
from typing import Type

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


    def filtrar_dados(self) -> Dict:
        fonte = self.contas.definir_fonte(self.origem)
        pagamentos = self.pagametos.agupar_por_empresa(fonte)
        transferencias = []
        for pagamento in pagamentos.items():
            print(pagamento[1])
            transferencia = {}
            empresa = self.fornecedores.retorna_empresa(pagamento[0], fonte)
            if empresa[5] == 'BRB':
                self.soma_iss_ir(pagamento[1])
                dados_empresa = self.fornecedores.retorna_empresa(pagamento[0], fonte)
                conta_origem = self.contas.pegar_conta(self.origem, pagamento[0][-2:])
                valor_total = self.somar_indice(pagamento[1], 3)
                transferencia['Empresa'] = pagamento[0]
                transferencia['Pagamentos'] = pagamento[1]
                transferencia['Dados_empresa'] = dados_empresa
                transferencia['Conta_origem'] = conta_origem[0]
                transferencia['Valor_total'] = valor_total
                transferencias.append(transferencia)
        for p in transferencias:
            for pag in p.items():
                print(f'{pag[0]}: {pag[1]}')
            print('\n')
        return transferencias

    def somar_indice(self, pagamentos: List, indice) -> float:
        soma = 0
        for pagamento in pagamentos:
            soma += pagamento[indice]
        total = self.formartar_valor(soma)
        return soma

    # def somar_indices(self, pagamentos, *args):
    #     soma_indices = []
    #     for indice in args:
    #         soma = self.somar_indice(pagamentos, indice)
    #         soma_indices.append(soma)
    #     total = sum(soma_indices)
    #     return total

    def soma_iss_ir(self, pagamentos: list):
        for pagamento in pagamentos:
            soma = pagamento[6] + pagamento[7]
            pagamento.append(self.formartar_valor(soma))


    def formartar_valor(self, valor):
        arredondado = f"{valor:.2f}"
        virgula = arredondado.replace(".", ",")
        if len(virgula) >= 10:
            milhao = virgula[0:-9] + "." + virgula[-9:-6] + "." + virgula[-6:]
            return milhao
        elif len(virgula) >= 7:
            mil = virgula[0:-6] + "." + virgula[-6:]
            return (mil)
        else:
            return virgula
