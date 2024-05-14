import pandas as pd

from tkinter import messagebox


from num2words import num2words

from typing import Dict

class TransferController():
    # dados_de_pagamento_individual
    colunas = ['Cotação',
               'Item',
               'Empresa',
               'Nº DANFE',
               'V. Total',
               'Nº TED',
               'Nº de processo SEI',
               'Conta',
               'ISS',
               'IR',
               'Liquido'
               ]

    itens_somados = {}

    def carregar_dados_de_pagamento(self, fonte):
        try:
            df = pd.read_excel(fonte, sheet_name='Controle', skiprows=[0])
            filtro = df.loc[df['Nº DANFE'].notna() & df['Nº TED'].isna()]
            dados = filtro.filter(TransferController.colunas)
            return dados
        except FileNotFoundError:
            messagebox.showerror(
                'Tem planilha aqui não!',
                f'Não foi encontrado a planilha referente ao cominho .\nAcesse "Configurações >URLs" e aponte para o desejado e depois pressione "Gravar alterações".'
            )

    def filtrar_danfe(self, fonte):
        pagamentos = self.carregar_dados_de_pagamento(fonte)
        duplicados = pagamentos[
            pagamentos.duplicated(
                subset=['Cotação', 'Empresa', 'Nº DANFE'], keep=False
            )
        ]
        return duplicados

    def listar_pagamentos(self, fonte):
        checagem = []
        duplicados = self.filtrar_danfe(fonte)
        for indice, linha in duplicados.iterrows():
            palavra_checagem = (
                    str(linha['Cotação']) +
                    '-' +
                    str(linha['Empresa']) +
                    '-' +
                    str(linha['Nº DANFE'])
            )
            if palavra_checagem in checagem:
                continue
            else:

                checagem.append(palavra_checagem)
                descricao = palavra_checagem.split('-')

                duplicados_subset1 = duplicados[
                    (duplicados['Cotação'] == linha['Cotação']) &
                    (duplicados['Empresa'] == linha['Empresa']) &
                    (duplicados['Nº DANFE'] == linha['Nº DANFE'])
                ]
                soma = duplicados_subset1['Liquido'].sum()
                soma_iss = duplicados_subset1['ISS'].sum()
                soma_ir = duplicados_subset1['IR'].sum()
                soma_valor_total = duplicados_subset1['V. Total'].sum()
                TransferController.itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], soma, linha['Nº de processo SEI'], linha['Conta'], soma_iss, soma_ir, soma_valor_total]

        pagamentos = self.carregar_dados_de_pagamento(fonte)
        for indice, linha in pagamentos.iterrows():
            palavra_checagem = str(linha['Cotação']) + '-' + str(linha['Empresa']) + '-' + str(linha['Nº DANFE'])
            if palavra_checagem in checagem:
                continue
            else:
                checagem.append(palavra_checagem)
                descricao = palavra_checagem.split('-')
                TransferController.itens_somados[palavra_checagem] = [descricao[0], descricao[1], descricao[2], linha['Liquido'],
                                                   linha['Nº de processo SEI'], linha['Conta'], linha['ISS'],
                                                   linha['IR'], linha['V. Total']]
        self.valor_por_extenso(TransferController.itens_somados)
        return TransferController.itens_somados


    def valor_por_extenso(self, itens_somados):
        for chave, valor in sorted(itens_somados.items()):
            extenso = num2words(valor[3], lang='pt_BR', to='currency')
            valor.append(extenso)

    # dados_da_emprsa
    # dados_conta

if __name__ == "__main__":
    fonte = '//srv-fs/HRG_GEOF/GEOF/PAGAMENTOS/Fontes/Matrix_2023_HRG.xlsx'
    teste = TransferController()

    pagamentos = teste.listar_pagamentos(fonte)
    print(pagamentos)
