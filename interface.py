import os
import sqlite3
import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from contas import Contas
from dados import Dados

class interface(Contas, Dados):

    ORIGEM = [("SRSSU", "SRSSU"), ("APS", "APS")]
    def __init__(self, tela):
        self.frame_mestre = LabelFrame(tela, padx=0, pady=0)
        self.frame_mestre.pack(fill="both", expand=1, padx=10, pady=10)

        self.frame_1 = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_1.pack(fill="both", padx=10, pady=(2, 2), ipady=10)

        self.frame_2 = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_2.pack(fill="both", expand=1, padx=10, pady=10)

        self.mycanvas = Canvas(self.frame_2, bg="black")
        self.mycanvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.rolagem = ttk.Scrollbar(self.frame_2, orient=VERTICAL, command=self.mycanvas.yview)
        self.rolagem.pack(side=RIGHT, fill=Y)

        self.mycanvas.config(yscrollcommand=self.rolagem.set)
        self.mycanvas.bind('<Configure>', lambda e: self.mycanvas.config(scrollregion=(0, 0, 2000, 5000)))
        self.mycanvas.bind("<MouseWheel>", lambda event: self.mycanvas.yview_scroll(-int(event.delta / 60), "units"))

        self.frame_display = Frame(self.mycanvas, padx=0, pady=0)
        self.frame_display.pack(padx=0, pady=0)

        self.mycanvas.create_window((0, 0), window=self.frame_display, anchor="nw")

        local = StringVar()
        local.set("SRSSU")

        contador = 0
        for legenda, valor in interface.ORIGEM:
            self.conta_origem = Radiobutton(self.frame_1, text=legenda, variable=local, value=valor)
            self.conta_origem.grid(row=0, column=contador)
            contador += 1

        self.teste1 = Button(self.frame_1, text='Listar', command=self.carregar_dados)
        self.teste1.grid(row=1, column=0)

        self.teste2 = Button(self.frame_1, text='Limpar', command=self.limpa_tela)
        self.teste2.grid(row=1, column=1)



    def display(self, valor):
        self.mycanvas.create_text((500, 470), text=valor, fill="green", font=("Helvetica", 10))

    def carregar_dados(self):
        self.listar_pagamentos()
        self.listar_contas()
        self.valores_formatados()
        self.display(self.a)

    def limpa_tela(self):
        self.mycanvas.delete("all")

    def valores_formatados(self):
        self.a =""
        for i in self.itens_somados.values():
            self.a = self.a + f'\n{i}\n'
        print(self.a)


if __name__ == '__main__':
    tela = Tk()
    tela.geometry("1100x600")
    tela.resizable(0, 0)
    objeto_tela = interface(tela)
    #tela.title()
    #tela.config(menu=objeto_tela.menu_certidões)
    tela.mainloop()
