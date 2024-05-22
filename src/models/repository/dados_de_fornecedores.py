import pandas as pd

class DadosDeFornecedores:
    def __init__(self):
        self.empresas = {}

    def fornecedores(self, fonte):
        df = pd.read_excel(fonte, sheet_name='Fornecedores')
        for indice, linha in df.iterrows():
            a = linha.to_list()
            self.empresas[a[0]] = a[1:]
        return self.empresas


    def retorna_empresa(self, empresa):
        beneficiario = self.empresas[empresa]
        return beneficiario


if __name__ == "__main__":
    fonte = '//srv-fs/HRG_GEOF/GEOF/PAGAMENTOS/Fontes/Matrix_2023_HRG.xlsx'
    a = DadosDeFornecedores()
    b = a.fornecedores(fonte)
    for indice, linha in b.items():
        print(f'{indice}')
        print(f'    {linha}\n')

    c = a.retorna_empresa('WL SERVIÇOS (701717)')
    print(f'Essa é a empresa  - {c}')