import os
class Estrutura():

    def criar_pastas(self, pasta_de_trabalho):
        pastas = [
            'fontes',  'guias/gama/transferências',
            'guias/gama/TED', 'guias/APS/transferências',
            'guias/APS/TEDs'
        ]

        for pasta in pastas:
            if os.path.exists(f'{pasta_de_trabalho}/{pasta}'):
                continue
            else:
                os.makedirs(f"{pasta_de_trabalho}/{pasta}")

    def checar_fontes(self):
        pass