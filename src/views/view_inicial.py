from datetime import date
from tkinter import *
from tkcalendar import Calendar
from typing import Dict

from src.constantes import *
from src.main.constructor.transfer_constructor import transfer_constructor

class ViewInicial(Frame):
    def __init__(self, gerador):
        super().__init__(gerador)
        self.pack(expand=True, fill='both')
        self.criar_widgets()


    def criar_widgets(self):
        self.frame_mestre = LabelFrame(self, padx=0, pady=0)

        self.frame_1 = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_calendario = LabelFrame(self.frame_mestre, padx=0, pady=0)
        self.frame_2 = LabelFrame(self.frame_mestre, padx=0, pady=0)

        self.local = StringVar()
        self.local.set(ORIGEM[0])
        self.conta_origem = OptionMenu(self.frame_1, self.local, ORIGEM)

        self.teste4 = Button(self.frame_2, text='Gerar pagamentos', command=lambda: self.gerar_constructor(transfer_constructor))
        self.teste5 = Button(self.frame_2, text='Gerar pagamentos', command=self.dados_de_entrada)
        self.teste6 = Button(self.frame_2, text='Gerar pagamentos', command=self.dados_de_entrada)

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
        self.criar_layout()


    def criar_layout(self):
        self.frame_mestre.pack(fill="both", expand=1, padx=10, pady=10)
        self.frame_1.pack(fill="both", padx=10, pady=0, ipady=0)
        self.frame_calendario.pack(fill="both", padx=10, pady=0, ipady=0)
        self.frame_2.pack(fill="both", padx=10, pady=10)
        self.conta_origem.grid(row=0, column=0)
        self.teste4.grid(row=0, column=1)
        self.teste5.grid(row=1, column=1)
        self.teste6.grid(row=2, column=1)
        self.calendario.grid(row=0, column=0)


    def gerar_constructor(self, constructor):
        entrada = self.dados_de_entrada()
        resposta = constructor(entrada)
        self.transfer_text(resposta)


    def dados_de_entrada(self) -> Dict:
        entradas = {
            'origem': self.local.get(),
            'data': self.data_de_pagamento()
        }
        return entradas


    def data_de_pagamento(self):
        data_calendario = self.calendario.get_date()
        dia = data_calendario[0:2]
        mes = data_calendario[3:5]
        ano = data_calendario[6:]
        data_de_pagamento = f'{ano}-{mes}-{dia}'
        return data_de_pagamento


    def transfer_text(self, resposta):
        self.frame_mestre.destroy()
        self.frame_mestre = LabelFrame(self, padx=0, pady=0)
        self.frame_mestre.pack(fill="both", expand=1, padx=10, pady=10)
        self.texto = Label(self.frame_mestre, text=resposta)
        self.Bvoltar = Button(self.frame_mestre, text='Tela inicial', command=self.voltar)
        self.texto.pack()
        self.Bvoltar.pack()


    def voltar(self):
        self.frame_mestre.destroy()
        self.criar_widgets()


