from src.controllers.interface_controller import InterfaceController
from typing import Dict
from typing import Type

from src.models.repository.dados_de_conta import DadosDeContas
from src.models.repository.dados_de_fornecedores import DadosDeFornecedores
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository

class IssController(InterfaceController):
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
        transferencias = []

        regular_custeio = []
        regular_investimento = []
        emenda_custeio = []
        emenda_investimento = []
        contas = {
            'RC': regular_custeio,
            'RI': regular_investimento,
            'EC': emenda_custeio,
            'EI': emenda_investimento
        }

        fonte = self.contas.definir_fonte(self.origem)
        pagamentos = self.pagametos.listar_pagamentos(fonte)
        lista_de_pagamentos = self.listar_pagamentos_de_imposto(pagamentos, 6)


        for pagamento in lista_de_pagamentos:
            contas[pagamento[5]].append(pagamento)


        for conta in contas.items():
            transferencia = {}
            if len(conta[1]) == 0:
                continue
            else:
                imposto_somado = self.somar_indice(conta[1], 6)
                valor_total = self.formartar_valor(imposto_somado)
                total_extenso = self.valor_por_extenso(imposto_somado)
                conta_origem = self.contas.pegar_conta(self.origem, conta[0])
                conta_origem_fomatado = self.formatar_dados_conta(conta_origem[0])
                pagamentos_por_origem = conta[1]
                for lista in pagamentos_por_origem:
                    fornecedor = self.fornecedores.retorna_empresa(lista[1], fonte)[4]
                    lista.append(fornecedor)
                self.converter_valores_em_string(pagamentos_por_origem)
                self.formatar_empresa(pagamentos_por_origem)

                transferencia['Empresa'] = (f'ISS-{conta[0]}')
                transferencia['Pagamentos'] = pagamentos_por_origem
                transferencia['Conta_origem'] = conta_origem_fomatado
                transferencia['Valor_total'] = valor_total
                transferencia['Total_extenso'] = total_extenso
                transferencia['Data_impressão'] = self.data_formatada()
                transferencia['Data_de_pagamento'] = self.data
                transferencia['Tipo'] = ''
                transferencias.append(transferencia)

        for p in transferencias:
            if isinstance(p, dict):
                for pag in p.items():
                    print(f'{pag[0]}: {pag[1]}')
                print('\n')
            else:
                print(f'{p}\n\n')
        print(transferencias)
        return transferencias
