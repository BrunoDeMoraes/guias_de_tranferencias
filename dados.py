import pandas as pd
from num2words import num2words

from typing import Dict

class Dados:

    def dados_de_pagamento(self, fonte):
        df = pd.read_excel(fonte, sheet_name='Controle', skiprows=[0])
        filtro = df.loc[df['Nº DANFE'].notna() & df['Nº TED'].isna()]
        dados = filtro.filter(
            ['Cotação', 'Item', 'Empresa', 'Nº DANFE', 'V. Total', 'Nº TED', 'Nº de processo SEI', 'Conta', 'ISS', 'IR', 'Liquido']
        )
        return dados

    def valor_por_extenso(self, itens_somados):
        for chave, valor in sorted(itens_somados.items()):
            extenso = num2words(valor[3], lang='pt_BR', to='currency')
            extenso2 = num2words(valor[6], lang='pt_BR', to='currency')
            extenso3 = num2words(valor[7], lang='pt_BR', to='currency')

            valor.append(extenso)
            valor.append(extenso2)
            valor.append(extenso3)

    def listar_pagamentos(self, fonte):
        pagamentos = self.dados_de_pagamento(fonte)
        duplicados = pagamentos[pagamentos.duplicated(subset=['Cotação', 'Empresa', 'Nº DANFE'], keep=False)]
        itens_somados = {}
        checagem = []
        for indice, linha in duplicados.iterrows():
            palavra_checagem = str(linha['Cotação']) + '-' + str(linha['Empresa']) + '-' + str(linha['Nº DANFE'])
            if palavra_checagem in checagem:
                continue
            else:
                checagem.append(palavra_checagem)
                duplicados_subset1 = duplicados[
                    (duplicados['Cotação'] == linha['Cotação']) &
                    (duplicados['Empresa'] == linha['Empresa']) &
                    (duplicados['Nº DANFE'] == linha['Nº DANFE'])
                ]
                soma = duplicados_subset1['Liquido'].sum()
                soma_iss = duplicados_subset1['ISS'].sum()
                soma_ir = duplicados_subset1['IR'].sum()
                descricao = palavra_checagem.split('-')
                itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], soma, linha['Nº de processo SEI'], linha['Conta'], soma_iss, soma_ir]
        for indice, linha in pagamentos.iterrows():
            palavra_checagem = str(linha['Cotação']) + '-' + str(linha['Empresa']) + '-' + str(linha['Nº DANFE'])
            if palavra_checagem in checagem:
                continue
            else:
                checagem.append(palavra_checagem)
                descricao = palavra_checagem.split('-')
                itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], linha['Liquido'],
                                                   linha['Nº de processo SEI'], linha['Conta'], linha['ISS'],
                                                   linha['IR'], linha['V. Total']]
        self.valor_por_extenso(itens_somados)
        return itens_somados


    def aglutinar_por_empresa(self, fonte) -> Dict:
        pagamentos = self.listar_pagamentos(fonte)
        pagamento_por_empresa = {}
        for pagamento in pagamentos.values():
            #print(pagamento)
            if pagamento[1] not in pagamento_por_empresa.keys():
                pagamento_por_empresa[pagamento[1]] = []
                pagamento_por_empresa[pagamento[1]].append(pagamento)
            else:
                pagamento_por_empresa[pagamento[1]].append(pagamento)


        return pagamento_por_empresa

    def soma_valor_liquido(self, fonte):
        lista_de_pagamentos = self.aglutinar_por_empresa(fonte)
        for item in lista_de_pagamentos.values():
            total_liquido = 0
            for lista in item:
                total_liquido += lista[3]
            item.append(total_liquido)

        for item in lista_de_pagamentos.items():
            print(f'{item[0]} - {item[1][-1]}')
        return lista_de_pagamentos

    def fornecedores(self, fonte):
        df = pd.read_excel(fonte, sheet_name='Fornecedores')
        empresas = {}
        for indice, linha in df.iterrows():
            a = linha.to_list()
            empresas[a[0]] = a[1:]
            #print(empresas)
        return empresas


if __name__ == "__main__":
    teste = Dados()
    teste.soma_valor_liquido('//srv-fs/HRG_GEOF/GEOF/PAGAMENTOS/Fontes/Matrix_2023_HRG.xlsx')
