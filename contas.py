import os
import sqlite3

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
        banco_de_dados = f'{caminho}/contas.db'
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

    def listar_contas(self):
        comando = ('SELECT * FROM contas')
        direcionador = self.conexao(comando)
        registros = direcionador.fetchall()
        # for i in registros:
        #  print(i)
        #  print(type(registros))
        return registros

    def pegar_conta(self, origem, codigo):
        print(origem)
        especificador = self.CODIGOS[codigo]
        comando = f"SELECT * FROM contas WHERE origem = '{origem}' AND recurso = '{especificador[0]}' AND tipo = '{especificador[1]}';"
        print(comando)
        direcionador = self.conexao(comando)
        registro = direcionador.fetchall()
        # for i in registro:
        #  print(i)
        #  print(type(registro))
        return registro

    def pegar_n_cotas(self):
        comando = f"SELECT numero FROM contas"
        direcionador = self.conexao(comando)
        registro = direcionador.fetchall()
        return registro

    def criar_bd(self):
        banco_de_dados = self.caminho_do_bd()
        if not os.path.exists(banco_de_dados):
            comando = 'CREATE TABLE contas (origem text, recurso text, tipo text, banco text, agencia text, numero text, cnpj texto)'
            self.conexao(comando)
        else:
            print('Banco de dados localizado.')
            #self.listar_contas()

    def cadastrar_conta(self, origem, recurso, tipo, banco, agencia, numero, cnpj):
        comando = ('INSERT INTO contas VALUES (:origem, :recurso, :tipo, :banco, :agencia, :numero, :cnpj)',
                   {'origem': origem, 'recurso': recurso, 'tipo': tipo, 'banco': banco, 'agencia': agencia, 'numero': numero, 'cnpj': cnpj}
                   )
        banco_de_dados = self.caminho_do_bd()
        self.conexao(comando[0], comando[1])

