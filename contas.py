import os
import sqlite3

class Contas:
    def caminho_do_arquivo(self):
        caminho_py = __file__
        caminho_do_dir = caminho_py.split('\\')
        self.caminho_de_uso = ('/').join(caminho_do_dir[0:-1])
        return self.caminho_de_uso

    def caminho_do_bd(self):
        caminho = self.caminho_de_uso
        self.banco_de_dados = f'{caminho}/contas.db'

    def conexao(self, comando):
        with sqlite3.connect(self.banco_de_dados) as conexao:
            direcionador = conexao.cursor()
            direcionador.execute(comando)
            return direcionador

    def consulta_contas(self):
        comando = 'SELECT *, oid FROM contas'
        direcionador = self.conexao(comando)
        self.registros = direcionador.fetchall()

    def cria_bd(self):
        if not os.path.exists(self.banco_de_dados):
            comando = 'CREATE TABLE contas (local text, recurso text, tipo text, banco text, agencia text, numero text, cnpj texto, endereco text, telefone text)'
            self.conexao(comando)
        else:
            print('Banco de dados localizado.')
            self.consulta_contas()

    def listar_contas(self):
        self.caminho_do_arquivo()
        self.caminho_do_bd()
        self.consulta_contas()
        for i in self.registros:
            print(i)
        return self.registros
