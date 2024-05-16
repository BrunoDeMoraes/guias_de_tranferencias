from typing import Dict
# import dados_da_view
# import transfer_controller
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository

def transfer_constructor(entrada: Dict):

    fonte = '//srv-fs/HRG_GEOF/GEOF/PAGAMENTOS/Fontes/Matrix_2023_HRG.xlsx'
    teste = DadosDePagamentoRepository()
    pagamentos = teste.agupar_por_empresa(fonte)

    print(f'Esta é a entrada {entrada}')


    #dados_de_entrada(origem, data_de_pagamento)
    #
    #
    #
    # enviar_dados_pra_view((self, pagamento, empresa, conta, origem, data_pagamento))







