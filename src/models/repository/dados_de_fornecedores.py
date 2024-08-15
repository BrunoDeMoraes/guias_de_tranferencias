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


    def retorna_empresa(self, empresa, fonte):
        self.fornecedores(fonte)
        if empresa[-1] == ')':
            beneficiario = self.empresas[empresa]
        else:
            beneficiario = self.empresas[empresa[0:-2]]
        return beneficiario


if __name__ == "__main__":
    fonte = '//srv-fs/HRG_GEOF/GEOF/PAGAMENTOS/Fontes/Matrix_2023_HRG.xlsx'
    a = DadosDeFornecedores()
    b = a.fornecedores(fonte)
    c = a.retorna_empresa('WL SERVIÇOS (701717)')