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
                conta_origem_fomatado = self.formatar_dados_conta(conta_origem[0])
                valor_total = self.somar_indice(pagamento[1], 3)
                nome_empresa = self.alinhar_texto(dados_empresa[0])
                self.converter_valores_em_string(pagamento[1])
                transferencia['Empresa'] = pagamento[0]
                transferencia['Pagamentos'] = pagamento[1]
                transferencia['Dados_empresa'] = dados_empresa
                transferencia['Conta_origem'] = conta_origem_fomatado
                transferencia['Valor_total'] = self.formartar_valor(valor_total)
                transferencia['Nome_empresa'] = nome_empresa
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


    def converter_valores_em_string(self, pagamentos: List):
        for pagamento in pagamentos:
            indice = 0
            for dado in pagamento:
                print(f'Dado {dado}')
                if isinstance(dado, float):
                    valor_formatado = self.formartar_valor(dado)
                    pagamento[indice] = valor_formatado
                indice += 1


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
            if len((linha + palavra)) > 50:
                texto_alinhado.append(linha)
                linha = palavra + " "
            else:
                linha += palavra + " "
            if palavra == palavras[-1]:
                texto_alinhado.append(linha)
        return texto_alinhado