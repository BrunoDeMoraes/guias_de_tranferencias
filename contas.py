import os
import sqlite3

class Contas:
    def caminho_do_arquivo(self):
        caminho_py = __file__
        caminho_do_dir = caminho_py.split('\\')
        caminho_de_uso = ('/').join(caminho_do_dir[0:-1])
        return caminho_de_uso

    def caminho_do_bd(self):
        caminho = self.caminho_do_arquivo()
        banco_de_dados = f'{caminho}/contas.db'
        return banco_de_dados

    def conexao(self, comando):
        banco_de_dados = self.caminho_do_bd()
        with sqlite3.connect(banco_de_dados) as conexao:
            direcionador = conexao.cursor()
            direcionador.execute(comando)
            return direcionador

    def listar_contas(self):
        comando = 'SELECT *, oid FROM contas'
        direcionador = self.conexao(comando)
        registros = direcionador.fetchall()
        for i in registros:
         print(i)
        return registros

    def criar_bd(self):
        if not os.path.exists(self.caminho_do_bd):
            comando = 'CREATE TABLE contas (local text, recurso text, tipo text, banco text, agencia text, numero text, cnpj texto, endereco text, telefone text)'
            self.conexao(comando)
        else:
            print('Banco de dados localizado.')
            self.listar_contas()
