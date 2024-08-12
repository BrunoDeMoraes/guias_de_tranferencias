from abc import ABC, abstractmethod
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from typing import Dict
from typing import List

from src.utils.funções_suporte import caminho_do_arquivo


class Guia(ABC):
    def __init__(self, dados: Dict, logo):
        self.contador = 0
        self.altura = 0
        self.dados = dados
        self.pasta_principal = caminho_do_arquivo()
        self.imagens = f'{self.pasta_principal}/Imagens/'
        self.cnv = canvas.Canvas(f'{self.pasta_principal}/guias/{self.dados["Data_de_pagamento"]}/{self.dados["Conta_origem"][0].split()[0]}/{self.dados["Empresa"]}.pdf')
        self.cnv.setPageSize(A4)
        self.logo = logo


    def inserir_logo(self, coordenadas):
        self.cnv.drawImage(
            f'{self.imagens}{self.logo}',
            self.mm(coordenadas[0]),
            self.mm(coordenadas[1] - self.contador),
            width=self.mm(coordenadas[2]),
            height=self.mm(coordenadas[3])
        )


    def mm(self, medida):
        return (medida/0.352777)


    def gerar_linhas(self, linhas, contador):
            for linha in linhas:
                self.cnv.line(
                    self.mm(linha[0]),
                    self.mm(linha[1] - contador),
                    self.mm(linha[2]),
                    self.mm(linha[3] - contador)
                )


    def inserir_pontilhado(self, coordenadas):
        self.cnv.setDash([3, 1])
        self.cnv.line(self.mm(coordenadas[0]), self.mm(coordenadas[1]), self.mm(coordenadas[2]), self.mm(coordenadas[3]))


    def gerar_retangulos(self, retangulos, contador):
        for coordenda in retangulos:
            self.cnv.rect(
                self.mm(coordenda[0]),
                self.mm(coordenda[1] - contador),
                width=self.mm(coordenda[2]),
                height=self.mm(coordenda[3])
            )


    def inserir_strings(
            self,
            fonte: str,
            tamanho: int,
            coordenadas: List,
            contador,
            entrada=None,
    ):
        self.cnv.setFont(fonte, tamanho)
        for coordenada in coordenadas:
            texto = self.selecionar_tipo_de_entrada(entrada, coordenada)
            self.cnv.drawString(
                self.mm(coordenada[0]),
                self.mm(coordenada[1] - contador),
                f'{texto}'
            )


    def selecionar_tipo_de_entrada(self, entrada, coordenada):
        if entrada == None:
            return coordenada[2]
        elif (
                isinstance(entrada, list) or
                isinstance(entrada, tuple) or
                isinstance(entrada, dict)
        ):
            return entrada[coordenada[2]]
        else:
            print('Deu alguma merda')


    def gerar_area_de_pagamentos(self, linhas_pagamento, retangulo_pagamentos, times8_pagamento, corretor, tamanho_fonte=9):
        for pagamento in self.dados['Pagamentos']:
            self.gerar_linhas(linhas_pagamento, self.altura)
            self.gerar_retangulos(retangulo_pagamentos, self.altura)
            self.inserir_strings(
            'Times-Roman',
                tamanho_fonte,
                times8_pagamento,
                self.altura,
                pagamento
            )
            self.altura += corretor
        self.altura = 0


    def gerar_linhas_texto_alinhado(self, fonte, tamanho, coordenadas, entrada, fator):
        self.cnv.setFont(fonte, tamanho)
        corretor = 0
        for linha in self.dados[entrada]:
            self.cnv.drawString(
                self.mm(coordenadas[0]),
                self.mm((coordenadas[1] - self.contador) - corretor),
                linha
            )
            corretor += fator
