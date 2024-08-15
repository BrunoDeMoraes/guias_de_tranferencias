import os
import sqlite3
from src.comandos_sql import CONSULTA_TABELAS

from src.comandos_sql import URLS
from src.comandos_sql import TABELAS

class DadosDeContas:

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

    def definir_fonte(self, fonte):
        caminhos = self.consultar_registros(URLS)
        origens = {}
        for caminho in caminhos:
            origens[caminho[0]] = caminho[1]
        return origens[fonte]

    def consultar_tabelas(self):
        tabs = self.consultar_registros(CONSULTA_TABELAS)
        return tabs

    def pegar_conta(self, origem, codigo):
        especificador = self.CODIGOS[codigo]
        comando = f"SELECT * FROM contas WHERE origem = '{origem}' AND recurso = '{especificador[0]}' AND tipo = '{especificador[1]}';"
        direcionador = self.conexao(comando)
        registro = direcionador.fetchall()
        return registro

    def pegar_conta_por_numero(self, numero):
        comando = f"SELECT * FROM contas WHERE numero = '{numero}';"
        direcionador = self.conexao(comando)
        registro = direcionador.fetchall()
        return registro


    def pegar_n_contas(self):
        comando = f"SELECT numero FROM contas"
        direcionador = self.conexao(comando)
        registro = direcionador.fetchall()
        return registro

    def criar_bd(self, tabelas):
        banco_de_dados = self.caminho_do_bd()
        if not os.path.exists(banco_de_dados):
            for tabela in tabelas:
                self.conexao(tabela)
            self.configura_bd()
        else:
            print('Banco de dados localizado.')


    def configura_bd(self):
        caminho = self.caminho_do_arquivo()
        enderecos = {
            'HRG Custeio': '-',
            'APS Custeio': '-',
            'HRG Investimento': '-',
            'APS Investimento': '-',
            'SRSSU Custeio': '-',
            'SRSSU Investimento': '-'
        }
        for endereco in enderecos:
            comando = 'INSERT INTO urls VALUES (:variavel, :url)'
            substituto = {"variavel": endereco, "url": enderecos[endereco]}
            caminho_do_banco_de_dados = self.caminho_do_bd()
            with sqlite3.connect(caminho_do_banco_de_dados) as conexao:
                direcionador = conexao.cursor()
                direcionador.execute(comando, substituto)


    def cadastrar_conta(self, origem, recurso, tipo, banco, agencia, numero, cnpj):
        comando = ('INSERT INTO contas VALUES (:origem, :recurso, :tipo, :banco, :agencia, :numero, :cnpj)',
                   {'origem': origem, 'recurso': recurso, 'tipo': tipo, 'banco': banco, 'agencia': agencia, 'numero': numero, 'cnpj': cnpj}
                   )
        banco_de_dados = self.caminho_do_bd()
        self.conexao(comando[0], comando[1])

    def deletar_conta(self, conta):
        comando = f'DELETE FROM contas WHERE numero = {conta}'
        banco_de_dados = self.caminho_do_bd()
        self.conexao(comando)


if __name__ == '__main__':
    c = DadosDeContas()
    c.criar_bd(TABELAS)
