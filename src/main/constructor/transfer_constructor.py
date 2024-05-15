from typing import Dict
# import dados_da_view
# import transfer_controller
from src.controllers.dados_de_pagamento_controller import DadosDePagamentoController

def transfer_constructor(entrada: Dict):

    fonte = '//srv-fs/HRG_GEOF/GEOF/PAGAMENTOS/Fontes/Matrix_2023_HRG.xlsx'
    teste = DadosDePagamentoController()
    pagamentos = teste.aglutinar_por_empresa(fonte)


    #dados_de_entrada(origem, data_de_pagamento)
    #
    #
    #
    # enviar_dados_pra_view((self, pagamento, empresa, conta, origem, data_pagamento))







