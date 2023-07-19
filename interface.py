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
    ORIGEM = ["SRSSU", "APS"]
    def __init__(self, tela, relatorio):
        self.relatorio = relatorio

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

        local = StringVar()
        local.set(interface.ORIGEM[0])

        self.conta_origem = OptionMenu(self.frame_1, local, *interface.ORIGEM)
        self.conta_origem.grid(row=0, column=0)

        self.teste1 = Button(self.frame_2, text='Listar', command=self.exibir_pagamentos)
        self.teste1.grid(row=0, column=0)

        self.teste2 = Button(self.frame_2, text='Limpar', command=self.limpa_tela)
        self.teste2.grid(row=0, column=1)

        self.teste3 = Button(self.frame_2, text='Checar', command=self.gerar_guias)
        self.teste3.grid(row=0, column=3)

        self.teste3 = Button(self.frame_2, text='Contas', command=self.relatorio.listar_contas)
        self.teste3.grid(row=0, column=4)

        self.teste4 = Button(self.frame_2, text='Fornecedores', command=self.relatorio.criar_ted)
        self.teste4.grid(row=0, column=5)

    def display(self, valor):
        self.mycanvas.create_text((530, 470), text=valor, fill="green", font=("Helvetica", 10, "bold"))

    def limpa_tela(self):
        self.mycanvas.delete("all")

    def exibir_pagamentos(self):
        self.relatorio.listar_pagamentos()
        self.display(self.relatorio.formatar_pagamentos())

    def gerar_guias(self):
        if not self.relatorio.checa_carregamento():
            print('Aí não, meu patrão! Carrega os dados.')
            #msgbox de erro
        else:
            print("Vou gerar as Guias")
            #metodo para gerar guias de transferência


if __name__ == '__main__':
    rel = Relatorio()
    tela = Tk()
    tela.geometry("1100x600")
    tela.resizable(0, 0)
    objeto_tela = interface(tela, rel)
    #tela.title()
    #tela.config(menu=objeto_tela.menu_certidões)
    tela.mainloop()
