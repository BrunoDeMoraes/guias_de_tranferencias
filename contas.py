import os
import sqlite3
def caminho_do_arquivo():
    caminho_py = __file__
    caminho_do_dir = caminho_py.split('\\')
    caminho_de_uso = ('/').join(caminho_do_dir[0:-1])
    return caminho_de_uso
def caminho_do_bd(caminho_do_arquivo):
    caminho = caminho_do_arquivo
    banco_de_dados = f'{caminho}/contas.db'
    return banco_de_dados

def conexao(caminho_do_bd, comando):
    caminho_do_banco_de_dados = caminho_do_bd
    with sqlite3.connect(caminho_do_banco_de_dados) as conexao:
        direcionador = conexao.cursor()
        direcionador.execute(comando)

def consulta_contas(caminho_do_bd):
    caminho_do_banco_de_dados = caminho_do_bd
    with sqlite3.connect(caminho_do_banco_de_dados) as conexao:
        comando = 'SELECT *, oid FROM contas'
        direcionador = conexao.cursor()
        direcionador.execute(comando)
        registros = direcionador.fetchall()
        return registros
def cria_bd(caminho_do_bd):
    caminho_do_banco_de_dados = caminho_do_bd
    if not os.path.exists(caminho_do_banco_de_dados):
        comando = 'CREATE TABLE contas (local text, recurso text, tipo text, banco text, agencia text, numero text, cnpj texto, endereco text, telefone text)'
        conexao(caminho_do_banco_de_dados, comando)
    else:
        print('Banco de dados localizado.')
        consulta_contas(caminho_do_bd)


arquivo = caminho_do_arquivo()
cam = caminho_do_bd(arquivo)
#cria_bd(cam)
comando = 'INSERT INTO contas VALUES ("APS", "Emenda", "Custeio", "070", "146", "007.333-0", "00.3994.700/0006-12", "Quadra 01", "3333-4444")'
conexao(cam, comando)
contas = consulta_contas(cam)
for conta in contas:
    print(conta)


