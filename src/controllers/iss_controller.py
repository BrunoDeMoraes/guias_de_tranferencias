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
        fonte = self.contas.definir_fonte(self.origem)
        pagamentos = self.pagametos.listar_pagamentos(fonte)
        lista_de_pagamentos = self.extrair_pagamentos(pagamentos)
        transferencias = []
        iss_somado = self.somar_indice(lista_de_pagamentos, 6)
        valor_total = self.formartar_valor(iss_somado)

        transferencias.append(valor_total)

        

        for pagamento in pagamentos.items():
            transferencia = {}
            empresa = self.fornecedores.retorna_empresa((pagamento[1][1] + '  '), fonte)
            if pagamento[1][6] != 0:
                dados_empresa = empresa
                conta_origem = self.contas.pegar_conta(self.origem, pagamento[1][5])
                conta_origem_fomatado = self.formatar_dados_conta(conta_origem[0])


                nome_empresa = self.alinhar_texto(dados_empresa[0])
                # self.converter_valores_em_string(pagamento[1])
                transferencia['Empresa'] = pagamento[0]
                transferencia['Pagamentos'] = pagamento[1]
                transferencia['Dados_empresa'] = dados_empresa
                transferencia['Conta_origem'] = conta_origem_fomatado

                transferencia['Nome_empresa'] = nome_empresa
                # transferencia['Total_extenso'] = total_extenso
                transferencia['Data_impressão'] = self.data_formatada()
                transferencias.append(transferencia)
        for p in transferencias:
            if isinstance(p, dict):
                for pag in p.items():
                    print(f'{pag[0]}: {pag[1]}')
                print('\n')
            else:
                print(f'{p}\n\n')
        return transferencias

# ['2034', 'HOSPFAR 0002 (702680)', '130883121', 1852.7, '00060-00014121/2024-09', 'RC', 22.5, 0.0, 1875.2, 'mil, oitocentos e cinquenta e dois reais e setenta centavos']