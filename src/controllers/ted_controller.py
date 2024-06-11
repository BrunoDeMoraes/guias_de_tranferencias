from src.controllers.interface_controller import InterfaceController
from typing import Dict
from typing import Type

from src.models.repository.dados_de_fornecedores import DadosDeFornecedores
from src.models.repository.dados_de_conta import DadosDeContas
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository

class TedController(InterfaceController):
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
            if empresa[5] != 'BRB':
                self.soma_iss_ir(pagamento[1])
                dados_empresa = self.fornecedores.retorna_empresa(pagamento[0], fonte)
                conta_origem = self.contas.pegar_conta(self.origem, pagamento[0][-2:])
                conta_origem_fomatado = self.formatar_dados_conta(conta_origem[0])
                valor_total = self.somar_indice(pagamento[1], 3)
                total_extenso = self.valor_por_extenso(valor_total)
                nome_empresa = self.alinhar_texto(dados_empresa[0])
                self.converter_valores_em_string(pagamento[1])
                transferencia['Empresa'] = pagamento[0]
                transferencia['Pagamentos'] = pagamento[1]
                transferencia['Dados_empresa'] = dados_empresa
                transferencia['Conta_origem'] = conta_origem_fomatado
                transferencia['Valor_total'] = self.formartar_valor(valor_total)
                transferencia['Nome_empresa'] = nome_empresa
                transferencia['Total_extenso'] = total_extenso
                transferencia['Data_impressão'] = self.data_formatada()
                transferencias.append(transferencia)
        for p in transferencias:
            for pag in p.items():
                print(f'{pag[0]}: {pag[1]}')
            print('\n')
        return transferencias
