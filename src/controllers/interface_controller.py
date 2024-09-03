from abc import ABC, abstractmethod
from datetime import date
from num2words import num2words

from typing import Dict
from typing import List
from typing import Type

from src.models.repository.dados_de_fornecedores import DadosDeFornecedores
from src.models.repository.dados_de_conta import DadosDeContas
from src.models.repository.dados_de_pagamento_repository import DadosDePagamentoRepository


class InterfaceController(ABC):
    def __init__(
            self,
            contas: Type[DadosDeContas],
            data: str,
            fornecedores: Type[DadosDeFornecedores],
            origem: str,
            pagamento: Type[DadosDePagamentoRepository]
    ):

        self.contas = contas
        self.data = data
        self.fornecedores = fornecedores
        self.origem = origem
        self.pagametos = pagamento
        self.produto = {}
        self.consuta_urls = list(self.contas.conexao('SELECT * FROM urls'))
        self.pasta_guias = self.consuta_urls[4][1]


    def somar_indice(self, pagamentos: List, indice) -> float:
        soma = 0
        for pagamento in pagamentos:
            soma += pagamento[indice]
        return soma


    def listar_pagamentos_de_imposto(self, pagamentos: Dict, indice: int):
        lista_de_pagamentos = self.extrair_pagamentos(pagamentos)
        pagamentos_validos = []
        for pagamento in lista_de_pagamentos:
            if pagamento[indice] != 0:
                pagamentos_validos.append(pagamento)
        return pagamentos_validos


    def extrair_pagamentos(self, dicionário_de_pagamentos: Dict):
        lista_de_pagamentos = []
        for pagamento in dicionário_de_pagamentos.items():
            lista_de_pagamentos.append(pagamento[1])
        return lista_de_pagamentos


    def converter_valores_em_string(self, pagamentos: List):
        for pagamento in pagamentos:
            self.converter_valores_em_string_lista_simples(pagamento)


    def converter_valores_em_string_lista_simples(self, pagamento):
        indice = 0
        for dado in pagamento:
            if isinstance(dado, float) or isinstance(dado, int):
                valor_formatado = self.formartar_valor(dado)
                pagamento[indice] = valor_formatado
            indice += 1


    def formatar_empresa(self, pagamentos: list) -> None:
        for pagamento in pagamentos:
            palavras = pagamento[1].split()
            fornecedor = ' '.join(palavras[:-1])
            if len(fornecedor) > 25:
                pagamento[1] = f'{fornecedor[:22]}...'
            else:
                pagamento[1] = fornecedor


    def soma_iss_ir(self, pagamentos: list):
        for pagamento in pagamentos:
            soma = pagamento[6] + pagamento[7]
            pagamento.append(self.formartar_valor(soma))


    def formatar_dados_conta(self, conta_origem):
        conta_lista = list(conta_origem)
        conta = self.formatar_conta(conta_lista[5])
        conta_lista[5] = conta
        cnpj = self.formatar_cnpj(conta_lista[6])
        conta_lista[6] = cnpj
        return conta_lista


    def formatar_conta(self, conta):
        conta_formatada = f"{conta[:-4]}.{conta[-4:-1]}-{conta[-1]}"
        return conta_formatada


    def formatar_cnpj(self, cnpj):
        mascara = f"{cnpj[-14:-12]}.{cnpj[-12:-9]}.{cnpj[-9:-6]}/{cnpj[-6:-2]}-{cnpj[-2:]}"
        return mascara


    def formartar_valor(self, valor):
        arredondado = f"{valor:.2f}"
        virgula = arredondado.replace(".", ",")
        if len(virgula) >= 10:
            milhao = virgula[0:-9] + "." + virgula[-9:-6] + "." + virgula[-6:]
            return f'R$ {milhao}'
        elif len(virgula) >= 7:
            mil = virgula[0:-6] + "." + virgula[-6:]
            return f'R$ {mil}'
        else:
            return f'R$ {virgula}'


    def alinhar_texto(self, texto: str):
        palavras = texto.split(" ")
        linha = ""
        texto_alinhado = []
        for palavra in palavras:
            if len((linha + palavra)) > 60:
                texto_alinhado.append(linha)
                linha = palavra + " "
            else:
                linha += palavra + " "
            if palavra == palavras[-1]:
                texto_alinhado.append(linha)
        return texto_alinhado

    def valor_por_extenso(self, valor):
        extenso = num2words(valor, lang='pt_BR', to='currency')
        valor_extenso = self.alinhar_texto(extenso)
        return valor_extenso


    def data_formatada(self):
        data = date.today()
        data_formatada = data.strftime('%d/%m/%Y')
        texto_data = f"Impresso em {data_formatada}"
        return texto_data


    @abstractmethod
    def filtrar_dados(self):
        pass


if __name__ == "__main__":
    pass