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
        self.frame_1.pack(fill="both", expand=1, padx=10, pady=(10, 2))

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

        self.janela = Label(self.frame_display, text="", bg="black", fg="white", padx=10, pady=0, justify=LEFT, font=("Helvetica", 10))
        self.janela.pack(ipadx=0, ipady=0)

        local = StringVar()
        local.set("SRSSU")

        for legenda, valor in interface.ORIGEM:
            self.conta_origem = Radiobutton(self.frame_1, text=legenda, variable=local, value=valor)
            self.conta_origem.pack()

        self.teste = Button(self.frame_1, text='Executar', command=lambda: self.display(local.get()))
        self.teste.pack(padx=0, pady=0)

        self.teste2 = Button(self.frame_1, text='listar', command=self.carregar_dados)
        self.teste2.pack(padx=0, pady=0)

    def display(self, valor):
        self.janela.destroy()
        self.janela = Label(self.frame_display, text=valor, bg="black", fg="green", padx=10, pady=0, justify=LEFT, font=("Helvetica", 10))
        self.janela.pack(ipadx=0, ipady=0)

    def carregar_dados(self):
        self.listar_pagamentos()
        self.listar_contas()
        self.valores_formatados()
        self.display(self.a)

    def valores_formatados(self):
        self.a =""
        for i in self.itens_somados.values():
            self.a = self.a + f'\n{i}\n'
        print(self.a)


if __name__ == '__main__':
    tela = Tk()
    tela.geometry("1000x600")
    tela.resizable(1, 1)
    objeto_tela = interface(tela)
    #tela.title()
    #tela.config(menu=objeto_tela.menu_certidões)
    tela.mainloop()
