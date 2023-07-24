import os
import sqlite3

class Contas:

    CODIGOS = {
        "RC": ('Regular','Custeio'),
        "RI": ('Regular','Investimento'),
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
        # for i in registros:
        #  print(i)
        #  print(type(registros))
        return registros

    def pegar_conta(self, origem, codigo):
        especificador = self.CODIGOS[codigo]
        comando = f"SELECT * FROM contas WHERE local = '{origem}' AND recurso = '{especificador[0]}' AND tipo = '{especificador[1]}';"
        direcionador = self.conexao(comando)
        registro = direcionador.fetchall()
        # for i in registro:
        #  print(i)
        #  print(type(registro))
        return registro

    def criar_bd(self):
        banco_de_dados = self.caminho_do_bd()
        if not os.path.exists(banco_de_dados):
            comando = 'CREATE TABLE contas (local text, recurso text, tipo text, banco text, agencia text, numero text, cnpj texto, endereco text, telefone text)'
            self.conexao(comando)
        else:
            print('Banco de dados localizado.')
            self.listar_contas()
