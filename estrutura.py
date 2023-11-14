import os
from datetime import date
class Estrutura():

    def criar_pastas(self, pasta_de_trabalho):
        pastas = ['fontes', 'guias']
        for pasta in pastas:
            if os.path.exists(f'{pasta_de_trabalho}/{pasta}'):
                continue
            else:
                os.makedirs(f"{pasta_de_trabalho}/{pasta}")

    def checar_fontes(self):
        pass