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
    ORIGEM = ["SRSSU", "SRSSU - (APS)"]
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
        self.frame_de_cadastro = LabelFrame(
            self.janela_de_cadastro, padx=0, pady=0
        )
        self.frame_de_cadastro.pack(padx=1, pady=1)

        self.local_origem = Entry(self.frame_de_cadastro, width=70)

        self.recurso = Entry(
            self.frame_de_cadastro, width=70
        )

        self.tipo_recurso = Entry(self.frame_de_cadastro, width=70)

        self.n_banco = Entry(self.frame_de_cadastro, width=70)

        self.n_agencia = Entry(
            self.frame_de_cadastro, width=70
        )
        self.n_conta = Entry(
            self.frame_de_cadastro, width=70
        )

        self.n_cnpj = Entry(
            self.frame_de_cadastro, width=70
        )


        self.local_origem.grid(row=1, column=2, padx=20)
        self.recurso.grid(row=2, column=2, padx=20)
        self.tipo_recurso.grid(row=3, column=2, padx=20)
        self.n_banco.grid(row=4, column=2, padx=20)
        self.n_agencia.grid(row=5, column=2, padx=20)
        self.n_conta.grid(row=6, column=2, padx=20)
        self.n_cnpj.grid(row=7, column=2, padx=20)


if __name__ == '__main__':
    rel = Relatorio()
    tela = Tk()
    tela.geometry("1100x600")
    tela.resizable(False, False)
    objeto_tela = interface(tela, rel)
    #tela.title()
    tela.config(menu=objeto_tela.menu)
    tela.mainloop()
