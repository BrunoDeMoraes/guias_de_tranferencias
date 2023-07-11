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
        self.frame_mestre.pack(padx=200, pady=100)

        local = StringVar()
        local.set("SRSSU")

        for legenda, valor in interface.ORIGEM:
            self.conta_origem = Radiobutton(tela, text=legenda, variable=local, value=valor)
            self.conta_origem.pack()

        self.teste = Button(self.frame_mestre, text='Executar', command=self.carregar_dados)
        self.teste.pack()

    def carregar_dados(self):
        self.listar_pagamentos()
        self.listar_contas()
    
if __name__ == '__main__':
    tela = Tk()
    objeto_tela = interface(tela)
    tela.resizable(1, 1)
    #tela.title()
    #tela.config(menu=objeto_tela.menu_certidões)
    tela.mainloop()
