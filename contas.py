import os
import sqlite3
from comandos_sql import CONSULTA_TABELAS

from comandos_sql import URLS

class Contas:

    CODIGOS = {
        "RC": ('Regular', 'Custeio'),
        "RI": ('Regular', 'Investimento'),
        "EI": ('Emenda', 'Investimento'),
        "EC": ('Emenda', 'Custeio')
    }
    def caminho_do_arquivo(self):
        caminho_py = __file__
        caminho_do_dir = caminho_py.split('\\')
        caminho_de_uso = ('/').join(caminho_do_dir[0:-1])
        return caminho_de_uso

    def caminho_do_bd(self):
        caminho = self.caminho_do_arquivo()
        banco_de_dados = f'{caminho}/guias.db'
        return banco_de_dados

    def conexao(self, *args):
        banco_de_dados = self.caminho_do_bd()
        with sqlite3.connect(banco_de_dados) as conexao:
            direcionador = conexao.cursor()
            if len(args) > 1:
                direcionador.execute(args[0], args[1])
            else:
                direcionador.execute(args[0])
            return direcionador

    def consultar_registros(self, comando):
        direcionador = self.conexao(comando)
        registros = direcionador.fetchall()
        return registros

    def consultar_tabelas(self):
        tabs = self.consultar_registros(CONSULTA_TABELAS)
        return tabs

    def pegar_conta(self, origem, codigo):
        print(origem)
        especificador = self.CODIGOS[codigo]
        comando = f"SELECT * FROM contas WHERE origem = '{origem}' AND recurso = '{especificador[0]}' AND tipo = '{especificador[1]}';"
        print(comando)
        direcionador = self.conexao(comando)
        registro = direcionador.fetchall()
        return registro

    def pegar_n_contas(self):
        comando = f"SELECT numero FROM contas"
        direcionador = self.conexao(comando)
        registro = direcionador.fetchall()
        print(f"ncontas {registro}")
        return registro

    def criar_bd(self, tabelas):
        banco_de_dados = self.caminho_do_bd()
        if not os.path.exists(banco_de_dados):
            for tabela in tabelas:
                self.conexao(tabela)
        else:
            print('Banco de dados localizado.')
            #self.consultar_registros()

    def configura_bd(self):
        caminho = self.caminho_do_arquivo()
        enderecos = {
            'SRSSU': f'{caminho}/SRSSU.xlsx',
            'SRSSU - APS': f'{caminho}/SRSSU - APS.xlsx',
            'SRSSU (Investimento)': f'{caminho}/SRSSU (Investimento).xlsx',
            'SRSSU - APS (Investimento)': f'{caminho}/SRSSU - APS (Investimento).xlsx',

        }
        for endereco in enderecos:
            comando = 'INSERT INTO urls VALUES (:variavel, :url)'
            substituto = {"variavel": endereco, "url": enderecos[endereco]}
            caminho_do_banco_de_dados = self.caminho_do_bd()
            with sqlite3.connect(caminho_do_banco_de_dados) as conexao:
                direcionador = conexao.cursor()
                direcionador.execute(comando, substituto)
        #self.consulta_urls()


    def cadastrar_conta(self, origem, recurso, tipo, banco, agencia, numero, cnpj):
        comando = ('INSERT INTO contas VALUES (:origem, :recurso, :tipo, :banco, :agencia, :numero, :cnpj)',
                   {'origem': origem, 'recurso': recurso, 'tipo': tipo, 'banco': banco, 'agencia': agencia, 'numero': numero, 'cnpj': cnpj}
                   )
        banco_de_dados = self.caminho_do_bd()
        self.conexao(comando[0], comando[1])

    def deletar_conta(self, conta):
        comando = f'DELETE FROM contas WHERE numero = {conta}'
        banco_de_dados = self.caminho_do_bd()
        print(comando)
        self.conexao(comando)
        print("Conta excluída")


if __name__ == '__main__':
    c = Contas()
    # a = c.consultar_registros(("SELECT name FROM sqlite_master WHERE type='table';"))
    # for i in a:
    #     print(i)
    #c.configura_bd()
    d = c.consultar_registros(URLS)
    print(d)

