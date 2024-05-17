import os
import sqlite3
import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import date
from typing import Dict

from src.views.view_inicial import ViewInicial


class Gerador_de_views(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x500")
        self.resizable(False, False)

        self.view_inicial = ViewInicial(self)

        self.mainloop()



    # def __init__(self, tela):
    #     self.tela = tela
    #     self.menu = Menu(self.tela)
    #     self.menu_configurações = Menu(self.menu)
    #     self.menu.add_cascade(
    #         label='Configurações', menu=self.menu_configurações)
    #     self.menu_configurações.add_separator()
    #     self.menu_configurações.add_command(
    #         label='Cadastro de fornecedores', command=self.dados_de_entrada)
    #     self.menu_configurações.add_separator()
    #     self.firstview()


    # def firstview(self):
    #     self.frame_mestre = LabelFrame(self.tela, padx=0, pady=0)
    #     self.frame_mestre.pack(fill="both", expand=1, padx=10, pady=10)
    #     self.frame_1 = LabelFrame(self.frame_mestre, padx=0, pady=0)
    #     self.frame_1.pack(fill="both", padx=10, pady=0, ipady=0)
    #
    #     self.frame_calendario = LabelFrame(self.frame_mestre, padx=0, pady=0)
    #     self.frame_calendario.pack(fill="both", padx=10, pady=0, ipady=0)
    #
    #     self.frame_2 = LabelFrame(self.frame_mestre, padx=0, pady=0)
    #     self.frame_2.pack(fill="both", padx=10, pady=10)
    #
    #     self.local = StringVar()
    #     self.local.set(Gerador_de_views.ORIGEM[0])
    #
    #     self.conta_origem = OptionMenu(self.frame_1, self.local, *Gerador_de_views.ORIGEM)
    #     self.conta_origem.grid(row=0, column=0)
    #
    #     self.teste4 = Button(self.frame_2, text='Gerar pagamentos', command=self.gerar_constructor)
    #     self.teste4.grid(row=0, column=1)
    #
    #     self.teste5 = Button(self.frame_2, text='Gerar pagamentos', command=self.dados_de_entrada)
    #     self.teste5.grid(row=1, column=1)
    #
    #     self.teste6 = Button(self.frame_2, text='Gerar pagamentos', command=self.dados_de_entrada)
    #     self.teste6.grid(row=2, column=1)
    #
    #     self.data_hoje = date.today()
    #     dia = int(self.data_hoje.strftime('%d'))
    #     mes = int(self.data_hoje.strftime('%m'))
    #     ano = int(self.data_hoje.strftime('%Y'))
    #
    #     self.calendario = Calendar(
    #         self.frame_calendario,
    #         selectmode='day',
    #         year=ano,
    #         month=mes,
    #         day=dia,
    #         locale="pt_br"
    #     )
    #
    #     self.calendario.grid(row=0, column=0)














    # def voltar(self):
    #     self.frame_mestre.destroy()
    #     self.firstview()

