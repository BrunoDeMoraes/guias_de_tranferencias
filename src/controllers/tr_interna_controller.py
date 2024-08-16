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
        transferencias = []
        transferencia = {}

        numero_remetente = self.remetente[0]
        numero_favorecida = self.favorecido
        conta_origem = self.contas.pegar_conta_por_numero(numero_remetente)
        conta_favorecido = self.contas.pegar_conta_por_numero(numero_favorecida)
        conta_origem_fomatado = self.formatar_dados_conta(conta_origem[0])
        conta_destino_formatado = self.formatar_dados_conta(conta_favorecido[0])
        valor_total = self.valor[0]
        total_extenso = self.valor_por_extenso(valor_total)
        nome_empresa = [f'{conta_destino_formatado[0]} {conta_destino_formatado[1]}']

        transferencia['Conta_origem'] = conta_origem_fomatado
        transferencia['Conta_destino'] = conta_destino_formatado
        transferencia['Nome_empresa'] = nome_empresa
        transferencia['Valor_total'] = self.formartar_valor(float(valor_total))
        transferencia['Total_extenso'] = total_extenso
        transferencia['Data_impressão'] = self.data_formatada()
        transferencia['Empresa'] = f' - {conta_destino_formatado[0].split()[0]} {conta_destino_formatado[1][0]}{conta_destino_formatado[2][0]} {valor_total} - TI'
        transferencia['Pagamentos'] = []
        transferencia['Data_de_pagamento'] = self.data
        transferencia['Tipo'] = f'{conta_origem_fomatado[0].split()[0]} {conta_origem_fomatado[1][0]}{conta_origem_fomatado[2][0]}'
        transferencia['Pasta_guias'] = self.pasta_guias
        transferencias.append(transferencia)
        return transferencias

