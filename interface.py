import os
import sqlite3
import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

#from contas import Contas
#from dados import Dados
from relatorio import Relatorio

class interface():
    ORIGEM = ["SRSSU", "SRSSU - APS"]
    RECURSO = ["Regular", "Emenda"]
    TIPO = ["Custeio", "Investimento"]
    BANCO = {"BRB": "070"}

    def __init__(self, tela, relatorio):
        self.relatorio = relatorio

        self.menu = Menu(tela)
        self.menu_configurações = Menu(self.menu)
        self.menu.add_cascade(
            label='Configurações', menu=self.menu_configurações)
        self.menu_configurações.add_separator()
        self.menu_configurações.add_command(
            label='Cadastro de fornecedores', command=self.abrir_janela_caminhos)
        self.menu_configurações.add_separator()

        self.frame_mestre = LabelFrame(tela, padx=0, pady=0)
        self.frame_mestre.pack(fill="both", expand=1, padx=10, pady=10)

        self.frame_1 = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_1.pack(fill="both", padx=10, pady=0, ipady=0)

        self.frame_2 = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_2.pack(fill="both", padx=10, pady=10)

        self.frame_3 = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_3.pack(fill="both", expand=1, padx=10, pady=10)

        self.mycanvas = Canvas(self.frame_3, bg="black")
        self.mycanvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.rolagem = ttk.Scrollbar(self.frame_3, orient=VERTICAL, command=self.mycanvas.yview)
        self.rolagem.pack(side=RIGHT, fill=Y)

        self.mycanvas.config(yscrollcommand=self.rolagem.set)
        self.mycanvas.bind('<Configure>', lambda e: self.mycanvas.config(scrollregion=(0, 0, 2000, 3000)))
        self.mycanvas.bind("<MouseWheel>", lambda event: self.mycanvas.yview_scroll(-int(event.delta / 60), "units"))

        self.frame_display = Frame(self.mycanvas, padx=0, pady=0)
        self.frame_display.pack(padx=0, pady=0)

        self.mycanvas.create_window((0, 0), window=self.frame_display, anchor="nw")

        self.local = StringVar()
        self.local.set(interface.ORIGEM[0])

        self.conta_origem = OptionMenu(self.frame_1, self.local, *interface.ORIGEM)
        self.conta_origem.grid(row=0, column=0)

        self.teste1 = Button(self.frame_2, text='Listar', command=self.exibir_pagamentos)
        self.teste1.grid(row=0, column=0)

        self.teste2 = Button(self.frame_2, text='Limpar', command=self.limpar_tela)
        self.teste2.grid(row=0, column=1)

        self.teste3 = Button(self.frame_2, text='Fornecedores', command=self.exibir_fornecedores)
        self.teste3.grid(row=0, column=3)

        self.teste3 = Button(self.frame_2, text='Contas', command=self.exibir_contas)
        self.teste3.grid(row=0, column=4)

        self.teste4 = Button(self.frame_2, text='Gerar pagamentos', command=self.imprimir_teds)
        self.teste4.grid(row=0, column=5)

    def maior_string(self, lista):
        maior = ""
        for opcao in lista:
            if len(opcao) <= len(maior):
                continue
            else:
                maior = opcao
        return len(maior)

    def ajustar_optionmenu(self, lista):
        tamanho = self.maior_string(lista)
        print(tamanho)
        nova_lista = []
        for palavra in lista:
            palavra_ajustada = (" " * (tamanho - len(palavra))) + palavra + (" " * (tamanho - len(palavra)))
            nova_lista.append(palavra_ajustada)
        print(nova_lista)
        return nova_lista

    def display(self, valor):
        self.mycanvas.create_text((530, 470), text=valor, fill="green", font=("Helvetica", 10, "bold"))

    def limpar_tela(self):
        self.mycanvas.delete("all")

    def exibir_pagamentos(self):
        self.display(self.relatorio.formatar_relatorio(self.relatorio.pagamentos.values()))

    def exibir_fornecedores(self):
        self.display(self.relatorio.formatar_relatorio(self.relatorio.empresas.values()))

    def exibir_contas(self):
        self.display(self.relatorio.formatar_relatorio(self.relatorio.contas))

    def imprimir_teds(self):
        origem = self.local.get()
        self.relatorio.gerar_teds(origem)

    def abrir_janela_caminhos(self):
        self.janela_de_cadastro = Toplevel()
        self.janela_de_cadastro.title('Lista de caminhos')
        self.janela_de_cadastro.resizable(True, True)

        self.frame_geral = LabelFrame(
            self.janela_de_cadastro, padx=100, pady=30
        )
        self.frame_geral.pack(padx=1, pady=1)


        self.frame_de_cadastro = LabelFrame(
            self.frame_geral, padx=50, pady=0
        )
        self.frame_de_cadastro.pack(padx=1, pady=1)

        self.frame_geral.pack(padx=1, pady=1)

        origem_ajustada = self.ajustar_optionmenu(interface.ORIGEM)
        self.origem_bd = StringVar()
        self.origem_bd.set(origem_ajustada[0])
        self.lista_origem_bd = OptionMenu(self.frame_de_cadastro, self.origem_bd, *origem_ajustada)


        recurso_ajustado = self.ajustar_optionmenu(interface.RECURSO)
        self.recurso_bd = StringVar()
        self.recurso_bd.set(recurso_ajustado[0])
        self.lista_recurso_bd = OptionMenu(self.frame_de_cadastro, self.recurso_bd, *recurso_ajustado)

        self.tipo_bd = StringVar()
        self.tipo_bd.set(interface.TIPO[0])
        self.lista_tipo_bd = OptionMenu(self.frame_de_cadastro, self.tipo_bd, *interface.TIPO)

        self.bancos = []
        for banco in interface.BANCO.keys():
            self.bancos.append(banco)
        self.banco_bd = StringVar()
        self.banco_bd.set("BRB")
        self.lista_banco_bd = OptionMenu(self.frame_de_cadastro, self.banco_bd, *self.bancos)


        self.n_banco = Entry(self.frame_de_cadastro, width=15)

        self.n_agencia = Entry(
            self.frame_de_cadastro, width=15
        )
        self.n_conta = Entry(
            self.frame_de_cadastro, width=15
        )

        self.n_cnpj = Entry(
            self.frame_de_cadastro, width=20
        )

        self.lista_origem_bd.grid(row=0, column=1, padx=10)
        self.lista_recurso_bd.grid(row=0, column=2, padx=10)
        self.lista_tipo_bd.grid(row=0, column=3, padx=10)
        self.lista_banco_bd.grid(row=0, column=4, padx=10)
        self.n_agencia.grid(row=1, column=1, padx=10)
        self.n_conta.grid(row=2, column=1, padx=10)
        self.n_cnpj.grid(row=3, column=1, padx=10)


if __name__ == '__main__':
    rel = Relatorio()
    tela = Tk()
    tela.geometry("1100x600")
    tela.resizable(False, False)
    objeto_tela = interface(tela, rel)
    #tela.title()
    tela.config(menu=objeto_tela.menu)
    tela.mainloop()
