from src.controllers.interface_controller import InterfaceController
from typing import Dict
from typing import Type

from src.models.repository.dados_de_conta import DadosDeContas
from src.models.repository.dados_de_fornecedores import DadosDeFornecedores
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository

class TrInternaController(InterfaceController):
    def __init__(
            self,
            contas: Type[DadosDeContas],
            data: str,
            fornecedores: Type[DadosDeFornecedores],
            origem: str,
            pagamento: Type[DadosDePagamentoRepository],
            remetente: str,
            valor: str,
            favorecido: str
    ):
        super().__init__(contas, data, fornecedores, origem, pagamento)
        self.remetente = remetente
        self.valor = valor
        self.favorecido = favorecido


    def filtrar_dados(self) -> Dict:
        # print(self.contas)
        # print(self.data)
        # print(self.fornecedores)
        # print(self.origem)
        # print(self.pagametos)
        # print(self.remetente)
        # print(self.valor)
        # print(self.favorecido)

        transferencias = []
        transferencia = {}

        numero_remetente = self.remetente[0][2:-3]
        numero_favorecida = self.favorecido[2:-3]
        conta_origem = self.contas.pegar_conta_por_numero(numero_remetente)
        conta_favorecido = self.contas.pegar_conta_por_numero(numero_favorecida)

        conta_origem_fomatado = self.formatar_dados_conta(conta_origem[0])
        conta_destino_formatado = self.formatar_dados_conta(conta_favorecido[0])
        valor_total = self.valor[0]
        total_extenso = self.valor_por_extenso(valor_total)
        nome_empresa = [f'{conta_destino_formatado[0]} {conta_destino_formatado[1]}']

        print(conta_origem_fomatado)
        print(conta_destino_formatado)

        transferencia['Conta_origem'] = conta_origem_fomatado
        transferencia['Conta_destino'] = conta_destino_formatado
        transferencia['Nome_empresa'] = nome_empresa
        transferencia['Valor_total'] = self.formartar_valor(float(valor_total))
        transferencia['Total_extenso'] = total_extenso
        transferencia['Data_impressão'] = self.data_formatada()
        transferencia['Empresa'] = 'Interna'
        transferencia['Pagamentos'] = []

        transferencias.append(transferencia)

        return transferencias





        # fonte = self.contas.definir_fonte(self.origem)
        # pagamentos = self.pagametos.agupar_por_empresa(fonte)
        # # for pagamento in pagamentos.items():
        # empresa = self.fornecedores.retorna_empresa(pagamento[0], fonte)
        # # if empresa[5] == 'BRB':
        # # self.soma_iss_ir(pagamento[1])
        # # print(self.origem)
        # print(conta_origem)
        # valor_total = self.somar_indice(pagamento[1], 3)
        # nome_empresa = self.alinhar_texto(dados_empresa[0])
        # self.converter_valores_em_string(pagamento[1])

        #
        # transferencia['Pagamentos'] = pagamento[1]
        # transferencia['Dados_empresa'] = dados_empresa


        # transferencia['Nome_empresa'] = nome_empresa


        #
        # for p in transferencias:
        #     for pag in p.items():
        #         print(f'{pag[0]}: {pag[1]}')
        #     print('\n')
