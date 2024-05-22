from abc import ABC, abstractmethod
from typing import Dict
from typing import Type

from src.models.repository.dados_de_fornecedores import DadosDeFornecedores as DFor
from src.models.repository.dados_de_conta import DadosDeContas as DCon
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository as DPag


class InterfaceController(ABC):
    def __init__(
            self,
            contas: Type[DCon],
            data: str,
            fornecedores: Type[DFor],
            origem: str,
            pagamento: Type[DPag]
    ):

        self.contas = contas
        self.data = data
        self.fornecedores = fornecedores
        self.origem = origem
        self.pagametos = pagamento


    @abstractmethod
    def filtrar_dados(self):
        pass


if __name__ == "__main__":
    pass