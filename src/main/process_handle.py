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

from src.main.constructor.transfer_constructor import transfer_constructor

class Process_handle():
    ORIGEM = ['HRG', 'APS', 'HRG (investimento)', 'APS (investimento)']
    RECURSO = ['Regular', 'Emenda']
    TIPO = ['Custeio', 'Investimento']
    BANCO = {'BRB': '070'}

    def __init__(self, tela):

        self.tela = tela
        self.menu = Menu(self.tela)
        self.menu_configurações = Menu(self.menu)
        self.menu.add_cascade(
            label='Configurações', menu=self.menu_configurações)
        self.menu_configurações.add_separator()
        self.menu_configurações.add_command(
            label='Cadastro de fornecedores', command=self.dados_de_entrada)
        self.menu_configurações.add_separator()
        self.firstview()


    def firstview(self):
        self.frame_mestre = LabelFrame(self.tela, padx=0, pady=0)
        self.frame_mestre.pack(fill="both", expand=1, padx=10, pady=10)
        self.frame_1 = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_1.pack(fill="both", padx=10, pady=0, ipady=0)

        self.frame_calendario = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_calendario.pack(fill="both", padx=10, pady=0, ipady=0)

        self.frame_2 = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_2.pack(fill="both", padx=10, pady=10)

        self.local = StringVar()
        self.local.set(Process_handle.ORIGEM[0])

        self.conta_origem = OptionMenu(self.frame_1, self.local, *Process_handle.ORIGEM)
        self.conta_origem.grid(row=0, column=0)

        self.teste4 = Button(self.frame_2, text='Gerar pagamentos', command=self.gerar_constructor)
        self.teste4.grid(row=0, column=1)

        self.teste5 = Button(self.frame_2, text='Gerar pagamentos', command=self.dados_de_entrada)
        self.teste5.grid(row=1, column=1)

        self.teste6 = Button(self.frame_2, text='Gerar pagamentos', command=self.dados_de_entrada)
        self.teste6.grid(row=2, column=1)

        self.data_hoje = date.today()
        dia = int(self.data_hoje.strftime('%d'))
        mes = int(self.data_hoje.strftime('%m'))
        ano = int(self.data_hoje.strftime('%Y'))

        self.calendario = Calendar(
            self.frame_calendario,
            selectmode='day',
            year=ano,
            month=mes,
            day=dia,
            locale="pt_br"
        )

        self.calendario.grid(row=0, column=0)

    def gerar_constructor(self):
        entrada = self.dados_de_entrada()
        transfer_constructor(entrada)
        self.tranfer_text()


    def data_de_pagamento(self):
        data_calendario = self.calendario.get_date()
        dia = data_calendario[0:2]
        mes = data_calendario[3:5]
        ano = data_calendario[6:]
        data_de_pagamento = f'{ano}-{mes}-{dia}'
        return data_de_pagamento
    def dados_de_entrada(self) -> Dict:
        entradas = {
            'origem': self.local.get(),
            'data': self.data_de_pagamento()
        }
        print(entradas)
        return entradas


    def tranfer_text(self):
        self.frame_mestre.destroy()
        self.frame_mestre = LabelFrame(self.tela, padx=0, pady=0)
        self.frame_mestre.pack(fill="both", expand=1, padx=10, pady=10)
        self.texto = Label(self.frame_mestre, text='Tá aí')
        self.Bvoltar = Button(self.frame_mestre, text='Tela inicial', command=self.voltar)
        self.texto.pack()
        self.Bvoltar.pack()


    def voltar(self):
        self.frame_mestre.destroy()
        self.firstview()


