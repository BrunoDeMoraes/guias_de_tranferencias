import os
import sqlite3
import threading
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from contas import Contas
from dados import Dados

class interface(Contas, Dados):

    ORIGEM = [("SRSSU", "SRSSU"), ("APS", "APS")]
    def __init__(self, tela):
        self.frame_mestre = LabelFrame(tela, padx=0, pady=0)
        self.frame_mestre.pack(fill="both", expand=1, padx=10, pady=10)



        local = StringVar()
        local.set("SRSSU")

        for legenda, valor in interface.ORIGEM:
            self.conta_origem = Radiobutton(self.frame_mestre, text=legenda, variable=local, value=valor)
            self.conta_origem.pack()

        self.teste = Button(self.frame_mestre, text='Executar', command=lambda: self.display(local.get()))
        self.teste.pack(padx=0, pady=0)

        self.teste2 = Button(self.frame_mestre, text='listar', command=self.carregar_dados)
        self.teste2.pack(padx=0, pady=0)

        self.frame_display = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_display.pack(padx=0, pady=0)

        self.janela = Label(self.frame_mestre, width=100, height=20, text="", bg="black", fg="white")
        self.janela.pack(padx=50, pady=(20, 80))

    def display(self, valor):
        self.janela.destroy()
        self.janela = Label(self.frame_mestre, width=100, height=20, text=f'{self.a}', bg="black", fg="green")
        self.janela.pack(padx=50, pady=(20, 80), anchor="w")

    def carregar_dados(self):
        self.listar_pagamentos()
        self.listar_contas()
        self.valores_formatados()
        self.display(self.a)

    def valores_formatados(self):
        self.a =""
        for i in self.itens_somados.values():
            self.a = self.a + f'{i}\n'
        print(self.a)


if __name__ == '__main__':
    tela = Tk()
    tela.geometry("820x500")
    tela.resizable(0, 0)
    objeto_tela = interface(tela)
    #tela.title()
    #tela.config(menu=objeto_tela.menu_certidões)
    tela.mainloop()
