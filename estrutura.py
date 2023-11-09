import os
class Estrutura():

    def criar_pastas(self, pasta_de_trabalho):
        pastas = ['imagens', 'fontes', 'guias']
        for pasta in pastas:
            if os.path.exists(f'{pasta_de_trabalho}/{pasta}'):
                continue
            else:
                os.makedirs(f"{pasta_de_trabalho}/{pasta}")