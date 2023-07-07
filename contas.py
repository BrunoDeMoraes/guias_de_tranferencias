import os
import sqlite3

class Contas:
    def caminho_do_arquivo(self):
        caminho_py = __file__
        caminho_do_dir = caminho_py.split('\\')
        self.caminho_de_uso = ('/').join(caminho_do_dir[0:-1])

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

    def cria_bd(caminho_do_bd):
        caminho_do_banco_de_dados = caminho_do_bd
        if not os.path.exists(caminho_do_banco_de_dados):
            comando = 'CREATE TABLE contas (local text, recurso text, tipo text, banco text, agencia text, numero text, cnpj texto, endereco text, telefone text)'
            conexao(caminho_do_banco_de_dados, comando)
        else:
            print('Banco de dados localizado.')
            consulta_contas(caminho_do_bd)

    def listar_contas(self):
        self.caminho_do_arquivo()
        self.caminho_do_bd()
        self.consulta_contas()
        for i in self.registros:
            print(i)


#arquivo = caminho_do_arquivo()
#cam = caminho_do_bd(arquivo)
#cria_bd(cam)
#comando = 'INSERT INTO contas VALUES ("APS", "Emenda", "Custeio", "070", "146", "007.333-0", "00.3994.700/0006-12", "Quadra 01", "3333-4444")'
#conexao(cam, comando)
#contas = consulta_contas(cam)
#for conta in contas:
#    print(conta)

