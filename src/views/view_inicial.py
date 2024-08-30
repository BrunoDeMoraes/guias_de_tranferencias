import tkinter as tk
import customtkinter as ctk

import os
import sqlite3
# from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import threading
import time

import PyPDF2
from tkcalendar import Calendar
from datetime import date
from typing import Dict

from src.comandos_sql import URLS
from src.comandos_sql import ATUALIZAR_CAMINHOS
from src.comandos_sql import CAMINHOS_ATUALIZADOS

from src.models.repository.dados_de_conta import DadosDeContas
from src.main.constructor.transfer_constructor import transfer_constructor
from src.main.constructor.ted_constructor import ted_constructor
from src.main.constructor.iss_constructor import iss_constructor
from src.main.constructor.ir_constructor import ir_constructor
from src.main.constructor.interna_constructor import interna_constructor

from src.utils.funções_suporte import caminho_do_arquivo, inverter_barra


class Interface(DadosDeContas):
    ORIGEM = ['HRG Custeio',
              'APS Custeio',
              'HRG Investimento',
              'APS Investimento',
              'SRSSU Custeio',
              'SRSSU Investimento'
              ]
    RECURSO = ['Regular', 'Emenda']
    TIPO = ['Custeio', 'Investimento']
    BANCO = {'BRB': '070'}


    def __init__(self, tela):
        self.tela = tela
        self.menu = tk.Menu(self.tela)
        self.menu_configurações = tk.Menu(self.menu, tearoff=0, bg='black', fg='white')
        self.menu.add_cascade(
            label='Configurações', menu=self.menu_configurações)
        self.menu_configurações.add_separator()
        self.menu_configurações.add_command(
            label='Contas', command=self.abrir_janela_cadastro)
        self.menu_configurações.add_separator()
        self.menu_configurações.add_command(
            label='Origens', command=self.abrir_caminhos)
        self.criar_widgets()


    def criar_widgets(self):
        self.frame_mestre = ctk.CTkFrame(self.tela, corner_radius=5)
        self.frame_mestre.pack()

        self.frame_1 = ctk.CTkFrame(self.frame_mestre)
        self.frame_1.pack(fill="both", padx=0, pady=0, ipady=0)

        self.frame_calendario = ctk.CTkFrame(self.frame_mestre)
        self.frame_calendario.pack(fill="both", padx=0, pady=5, ipady=0)

        self.frame_2 = ctk.CTkFrame(self.frame_mestre)
        self.frame_2.pack(fill="both", padx=0, pady=0)

        self.frame_barra = ctk.CTkFrame(self.frame_mestre)
        self.frame_barra.pack(fill="both", padx=0, pady=5)

        self.local = ctk.StringVar()
        self.local.set(Interface.ORIGEM[0])

        self.conta_origem = ctk.CTkOptionMenu(
            self.frame_1,
            width=170,
            values=Interface.ORIGEM,
            variable=self.local,
            # dynamic_resizing=False,
        )
        self.conta_origem.grid(row=0, column=0, sticky='w', pady=10)

        self.data_hoje = date.today()
        dia = int(self.data_hoje.strftime('%d'))
        mes = int(self.data_hoje.strftime('%m'))
        ano = int(self.data_hoje.strftime('%Y'))

        self.calendario = Calendar(self.frame_calendario, selectmode='day', year=ano, month=mes, day=dia, locale="pt_br")
        self.calendario.pack(pady=20)

        self.comandos = [
            'Criar todas as guias',
            'Gerar transferencias',
            'Gerar TEDs',
            'Gerar ISS',
            'Gerar IR',
            'Transferência interna',
            'Mesclar arquivos'
        ]
        self.comando = ctk.StringVar()
        self.comando.set('Escolha um comando')
        self.lista_de_comandos = ctk.CTkOptionMenu(self.frame_2, values=self.comandos, variable=self.comando)
        self.lista_de_comandos.pack(pady=10)

        self.comando_atual = f''

        self.botao_gerar_guia = ctk.CTkButton(
            self.frame_2, text='Gerar guias',
            command=self.selecionar_tipo_de_guia_thread,
        )
        self.botao_gerar_guia.pack(pady=20)

        self.valor_progresso = ctk.DoubleVar()

        self.valor_progresso.trace('w', self.atualizar_progresso)


        self.valor_executado = ctk.CTkLabel(
            self.frame_barra,
            text=f''
        )
        self.valor_executado.grid(row=0, column=1)

        self.criar_barra_de_progresso()


    def mesclar_arquivos(self):
        caminho_para_salvar_arquivos = filedialog.askdirectory()
        url_arquivos = []
        self.inicializar_barra_de_progresso()
        for raiz, diretorios, arquivos in os.walk(caminho_para_salvar_arquivos):
            for arquivo in arquivos:
                if arquivo.endswith('.pdf'):
                    caminho_completo = os.path.join(raiz, arquivo)
                    url = inverter_barra(caminho_completo)
                    url_arquivos.append(url)
        if os.path.exists(f'{caminho_para_salvar_arquivos}/Mesclados {self.data_de_pagamento()}.pdf'):
            self.finalizar_barra_de_progresso()
            messagebox.showerror('De novo, mano', 'O arquivo já existe. Se quiser criar novamente, apaga lá primeiro!')
        else:
            with open(
                    (
                            f'{caminho_para_salvar_arquivos}/Mesclados {self.data_de_pagamento()}.pdf'
                    ), 'wb'
            ) as arquivo_final:
                criador_de_pdf = PyPDF2.PdfWriter()
                for url_arquivo in url_arquivos:
                    with open(url_arquivo, 'rb') as arquivo_aberto:
                        arquivo_lido = PyPDF2.PdfReader(
                            arquivo_aberto
                        )
                        for página in range(len(arquivo_lido.pages)):
                            página_do_pdf = arquivo_lido.pages[página]
                            criador_de_pdf.add_page(página_do_pdf)
                        criador_de_pdf.write(arquivo_final)
                self.finalizar_barra_de_progresso()
                messagebox.showinfo('Rolou', 'Mesclagem concluída com sucesso!')


    def selecionar_tipo_de_guia(self):
        tipo_de_comando = {
            'Criar todas as guias': self.gerar_todas_as_guias,
            'Transferência interna': self.abrir_dados_de_transferencia_interna,
            'Gerar transferencias': lambda: self.gerar_processo(transfer_constructor),
            'Gerar TEDs': lambda: self.gerar_processo(ted_constructor),
            'Gerar ISS': lambda: self.gerar_processo(iss_constructor),
            'Gerar IR': lambda: self.gerar_processo(ir_constructor),
            'Mesclar arquivos': self.mesclar_arquivos
        }
        comando_escolhido = self.comando.get()
        print(f'Esse é o comando {comando_escolhido}')
        tipo_de_comando[comando_escolhido]()
        if comando_escolhido not in ['Mesclar arquivos', 'Transferência interna']:
            messagebox.showinfo('Parece que rolou!', f'Tudo certo!!!')


    def progresso_continuo(self):
        while self.executor:
            total = self.valor_progresso.get()
            if total == 0.99:
                continue
            else:
                self.valor_progresso.set((total + 0.01))
                time.sleep(1)
        print('Thread encerrada')


    def gerar_todas_as_guias(self):
        self.comando_atual = 'Transferências BRB'
        self.gerar_processo(transfer_constructor)
        self.comando_atual = 'TEDs'
        self.gerar_processo(ted_constructor)
        self.comando_atual = 'ISS'
        self.gerar_processo(iss_constructor)
        self.comando_atual = 'IR'
        self.gerar_processo(ir_constructor)
        self.finalizar_barra_de_progresso()
        self.comando_atual = ''


    def gerar_processo(self, constructor):
        self.inicializar_barra_de_progresso()
        self.gerar_constructor(constructor)


    def finalizar_barra_de_progresso(self):
        self.valor_progresso.set(1)
        self.executor = False
        time.sleep(1)
        self.valor_progresso.set(0)
        self.valor_executado.configure(text='')


    def selecionar_tipo_de_guia_thread(self):
        print('iniciando thred')
        tr = threading.Thread(target=self.selecionar_tipo_de_guia)
        tr.start()
        print('finalizando thread')


    def inicializar_barra_de_progresso(self):
        self.executor = True
        thread_checagem_true = threading.Thread(target=self.progresso_continuo)
        thread_checagem_true.start()


    def gerar_constructor(self, constructor, dados_internos=False):
        entrada = self.dados_de_entrada(dados_internos)
        print(f'Essa é a entrada {entrada}')
        resposta = constructor(entrada)
        print(f'Essa é a resposta {resposta}')
        self.finalizar_barra_de_progresso()


    def criar_barra_de_progresso(self):
        self.barra = ctk.CTkProgressBar(
            self.frame_barra,
            orientation='horizontal',
            width=300,
            # height=20,
            # length=270,
            mode='determinate',
            variable=self.valor_progresso,
        )
        self.barra.grid(row=1, column=1)
        self.barra['value'] = 0


    def atualizar_progresso(self, *args):
        progresso = self.valor_progresso.get()
        tipo_de_guia = self.definir_guia_atual()
        self.barra['value'] = progresso
        self.valor_executado.configure(text=f'Gerando {tipo_de_guia}: {self.comando_atual} {int(progresso * 100)}%')


    def definir_guia_atual(self):
        comando_de_guia = self.comando.get()
        comando_de_guia_sepaarado = comando_de_guia.split()
        tipo_de_guia = ' '.join(comando_de_guia_sepaarado[1:])
        return tipo_de_guia



    def dados_de_entrada(self, dados_internos) -> Dict:
        if dados_internos == True:
            entradas = {
                'origem': self.local.get(),
                'data': self.data_de_pagamento(),
                'remetente': self.remetente.get()[-7:],
                'valor': self.valor_a_transferir.get(),
                'favorecido': self.favorecido.get()[-7:]
            }
        else:
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
        self.texto = Label(self.frame_mestre, text=resposta)
        self.Bvoltar = Button(self.frame_mestre, text='Tela inicial', command=self.voltar)
        self.texto.pack()
        self.Bvoltar.pack()


    def voltar(self):
        self.frame_mestre.destroy()
        self.criar_widgets()


    def abrir_janela_cadastro(self):
        self.janela_de_cadastro = Toplevel()
        self.janela_de_cadastro.title('Cadastro de contas')
        self.janela_de_cadastro.resizable(True, True)

        self.frame_geral = LabelFrame(
            self.janela_de_cadastro, padx=50, pady=30
        )
        self.frame_geral.pack(padx=1, pady=1)

        self.frame_de_cadastro = LabelFrame(
            self.frame_geral, padx=10, pady=0
        )
        self.frame_de_cadastro.pack(padx=1, pady=1)

        self.frame_de_exclusao = LabelFrame(
            self.frame_geral, padx=10, pady=0
        )
        self.frame_de_exclusao.pack(padx=1, pady=1)

        self.frame_display = LabelFrame(
            self.frame_geral, padx=10, pady=0
        )
        self.frame_display.pack(padx=1, pady=1)

        self.frame_geral.pack(padx=1, pady=1)

        self.titulo_origem = Label(self.frame_de_cadastro, text="Origem")

        self.origem_bd = StringVar()
        self.origem_bd.set(Interface.ORIGEM[0])
        self.lista_origem_bd = OptionMenu(self.frame_de_cadastro, self.origem_bd, *Interface.ORIGEM)
        self.lista_origem_bd.config(width=15)

        self.titulo_recurso = Label(self.frame_de_cadastro, text="Recurso")

        self.recurso_bd = StringVar()
        self.recurso_bd.set(Interface.RECURSO[0])
        self.lista_recurso_bd = OptionMenu(self.frame_de_cadastro, self.recurso_bd, *Interface.RECURSO)
        self.lista_recurso_bd.config(width=15)

        self.titulo_tipo = Label(self.frame_de_cadastro, text="Tipo")
        self.tipo_bd = StringVar()
        self.tipo_bd.set(Interface.TIPO[0])
        self.lista_tipo_bd = OptionMenu(self.frame_de_cadastro, self.tipo_bd, *Interface.TIPO)
        self.lista_tipo_bd.config(width=15)

        self.titulo_banco = Label(self.frame_de_cadastro, text="Banco")

        self.bancos = []
        for banco in Interface.BANCO.keys():
            self.bancos.append(banco)
        self.banco_bd = StringVar()
        self.banco_bd.set("BRB")
        self.lista_banco_bd = OptionMenu(self.frame_de_cadastro, self.banco_bd, *self.bancos)
        self.lista_banco_bd.config(width=15)

        self.titulo_agencia = Label(self.frame_de_cadastro, text="Agência")

        self.n_agencia = Entry(
            self.frame_de_cadastro, width=10
        )

        self.titulo_conta = Label(self.frame_de_cadastro, text="Conta")

        self.n_conta = Entry(
            self.frame_de_cadastro, width=15
        )

        self.titulo_cnpj = Label(self.frame_de_cadastro, text="CNPJ")

        self.n_cnpj = Entry(
            self.frame_de_cadastro, width=20
        )

        self.botao_cadastro = Button(self.frame_de_cadastro, text="Cadastrar", command=self.submeter_conta)

        self.titulo_origem.grid(row=0, column=1)
        self.titulo_recurso.grid(row=0, column=2)
        self.titulo_tipo.grid(row=0, column=3)
        self.titulo_banco.grid(row=0, column=4)
        self.titulo_agencia.grid(row=0, column=5)
        self.titulo_conta.grid(row=0, column=6)
        self.titulo_cnpj.grid(row=0, column=7)

        self.lista_origem_bd.grid(row=1, column=1)
        self.lista_recurso_bd.grid(row=1, column=2)
        self.lista_tipo_bd.grid(row=1, column=3)
        self.lista_banco_bd.grid(row=1, column=4)
        self.n_agencia.grid(row=1, column=5)
        self.n_conta.grid(row=1, column=6)
        self.n_cnpj.grid(row=1, column=7)

        self.botao_cadastro.grid(row=2, column=1, columnspan=7, pady=10, sticky=E)

        self.opcoes_de_exclusao = Label(
            self.frame_de_exclusao, text="Caso deseje excluir uma conta, utilize a opção abaixo:")

        self.v_contas = StringVar()

        self.atualizar_contas()

        numeros_de_contas = self.numero_contas()
        self.v_contas.set('Selecione uma conta')
        self.v_contas_bd = OptionMenu(self.frame_de_exclusao, self.v_contas, *numeros_de_contas)
        self.v_contas_bd.config(width=20)

        self.botao_excluir = Button(self.frame_de_exclusao, text="Excluir conta", command=self.excluir_conta)

        self.opcoes_de_exclusao.grid(row=0, column=1, columnspan=2)
        self.v_contas_bd.grid(row=1, column=1, padx=30)
        self.botao_excluir.grid(row=1, column=2, padx=30)

        self.display = Label(self.frame_display, text='', width=30, height=8)
        self.display.pack()

        self.v_contas.trace('w', self.atualiza_label_cadastro)


    def atualiza_label_cadastro(self, *args):
        conta = self.v_contas.get()[2:-3]
        dados_conta = self.pegar_conta_por_numero(conta)
        origem_tipo = dados_conta[0][0].split()
        texto = (f'Origem: {origem_tipo[0]}\n'
                 f'Tipo: {origem_tipo[1]}\n'
                 f'Recurso: {dados_conta[0][1]}\n'
                 f'Banco: {dados_conta[0][3]}\n'
                 f'Agência: {dados_conta[0][4]}\n'
                 f'Conta: {dados_conta[0][5]}\n'
                 f'CNPJ: {dados_conta[0][6]}')
        self.display.config(text=texto)


    def atualizar_contas(self):
        if self.numero_contas() == []:
            a = ["Nenhuma conta cadastrada"]
        else:
            a = self.numero_contas()
        self.v_contas.set('Selecione uma conta')
        self.v_contas_bd = OptionMenu(self.frame_de_exclusao, self.v_contas, *a)
        self.v_contas_bd.config(width=20)
        self.v_contas_bd.grid(row=1, column=1, padx=30)


    def submeter_conta(self):
        self.cadastrar_conta(self.origem_bd.get(), self.recurso_bd.get(), self.tipo_bd.get(), Interface.BANCO[self.banco_bd.get()], self.n_agencia.get(), self.n_conta.get(), self.n_cnpj.get())
        self.atualizar_contas()
        self.n_agencia.delete(0, END)
        self.n_conta.delete(0, END)
        self.n_cnpj.delete(0, END)


    def numero_contas(self):
        contas = list(self.pegar_n_contas())
        return contas


    def excluir_conta(self):
        conta = self.v_contas.get()
        self.deletar_conta(conta[1:-2])
        self.atualizar_contas()


    def altera_caminho(self, entrada, xlsx=False):
        if xlsx == True:
            caminho = filedialog.askopenfilename(
                initialdir=self.caminho_do_arquivo(),
                filetypes=(('Arquivos', '*.xlsx'), ("Tudo", '*.*'))
            )
        else:
            caminho = filedialog.askdirectory(
                initialdir=self.caminho_do_arquivo()
            )
        entrada.delete(0, 'end')
        entrada.insert(0, caminho)


    def itens_para_atualização(self):
        itens = [
            [Interface.ORIGEM[0],
             '1',
             self.caminho_srssu.get()],
            [Interface.ORIGEM[1],
             '2',
             self.caminho_aps.get()],
            [Interface.ORIGEM[2],
             '3',
             self.caminho_srssu_i.get()],
            [Interface.ORIGEM[3],
             '4',
             self.caminho_aps_i.get()],
            ['Guias',
             5,
             self.pasta_guias.get()]
        ]
        return itens


    def atualizar_caminhos(self):
        resposta = messagebox.askyesno(
            ATUALIZAR_CAMINHOS[0], ATUALIZAR_CAMINHOS[1]
        )
        itens_para_atualizacao = self.itens_para_atualização()

        if resposta:
            arquivo = self.caminho_do_arquivo()
            with sqlite3.connect(f'{arquivo}/guias.db') as conexao:
                direcionador = conexao.cursor()
                for item in itens_para_atualizacao:
                    linha_update = (
                        f"UPDATE urls SET url = :nova_url WHERE variavel = '{item[0]}'"
                    )
                    direcionador.execute(linha_update, {'nova_url': item[2]})
                conexao.commit()
            self.caminhos.destroy()
            messagebox.showinfo(
                CAMINHOS_ATUALIZADOS[0],
                (CAMINHOS_ATUALIZADOS[1])
            )
        else:
            self.caminhos.destroy()


    def abrir_caminhos(self):
        self.caminhos = Toplevel()
        self.urls = self.consultar_registros(URLS)
        self.caminhos.title('Caminhos')
        self.caminhos.resizable(False, False)
        self.frame_caminhos = LabelFrame(
            self.caminhos, padx=0, pady=0
        )
        self.frame_caminhos.pack(padx=1, pady=1)

        self.botao_xlsx = Button(
            self.frame_caminhos, text='HRG Custeio',
            command=lambda: self.altera_caminho(self.caminho_srssu, True),
            padx=0, pady=0, bg='green', fg='white',
            font=('Helvetica', 8, 'bold'), bd=1
        )
        self.caminho_srssu = Entry(self.frame_caminhos, width=70)

        self.botao_pasta_de_certidões = Button(
            self.frame_caminhos, text='APS Custeio',
            command=lambda: (
                self.altera_caminho(self.caminho_aps, True)),
            padx=0, pady=0, bg='green', fg='white',
            font=('Helvetica', 8, 'bold'), bd=1
        )
        self.caminho_aps = Entry(
            self.frame_caminhos, width=70
        )

        self.botao_log = Button(
            self.frame_caminhos, text='HRG Investimento',
            command=lambda: self.altera_caminho(self.caminho_srssu_i, True), padx=0,
            pady=0, bg='green', fg='white', font=('Helvetica', 8, 'bold'),
            bd=1
        )
        self.caminho_srssu_i = Entry(self.frame_caminhos, width=70)

        self.certidões_para_pagamento = Button(
            self.frame_caminhos, text='APS Investimento',
            command=lambda: (
                self.altera_caminho(self.caminho_aps_i, True)
            ),
            padx=0, pady=0, bg='green', fg='white',
            font=('Helvetica', 8, 'bold'), bd=1
        )

        self.caminho_aps_i = Entry(
            self.frame_caminhos, width=70
        )

        self.botao_pasta_guias = Button(
            self.frame_caminhos, text='Pasta destino para guias',
            command=lambda: (
                self.altera_caminho(self.pasta_guias)
            ),
            padx=0, pady=0, bg='green', fg='white',
            font=('Helvetica', 8, 'bold'), bd=1
        )

        self.pasta_guias = Entry(
            self.frame_caminhos, width=70
        )

        self.gravar_alterações = Button(
            self.frame_caminhos, text='Gravar alterações',
            command=self.atualizar_caminhos, padx=10, pady=10, bg='green',
            fg='white', font=('Helvetica', 8, 'bold'), bd=1
        )

        self.botao_xlsx.grid(
            row=1, column=1, columnspan=1, padx=15, pady=10, ipadx=5,
            ipady=13, sticky=W + E
        )
        self.caminho_srssu.insert(0, self.urls[0][1])
        self.caminho_srssu.grid(row=1, column=2, padx=20)

        self.botao_pasta_de_certidões.grid(
            row=2, column=1, columnspan=1, padx=15, pady=10, ipadx=10,
            ipady=13, sticky=W + E
        )

        self.caminho_aps.insert(0, self.urls[1][1])
        self.caminho_aps.grid(row=2, column=2, padx=20)

        self.botao_log.grid(
            row=3, column=1, columnspan=1, padx=15, pady=10, ipadx=10,
            ipady=13, sticky=W + E
        )

        self.caminho_srssu_i.insert(0, self.urls[2][1])
        self.caminho_srssu_i.grid(row=3, column=2, padx=20)

        self.certidões_para_pagamento.grid(
            row=4, column=1, columnspan=1, padx=15, pady=10, ipadx=10,
            ipady=13, sticky=W + E
        )

        self.caminho_aps_i.insert(0, self.urls[3][1])
        self.caminho_aps_i.grid(row=4, column=2, padx=20)

        self.botao_pasta_guias.grid(
            row=5, column=1, columnspan=1, padx=15, pady=10, ipadx=10,
            ipady=13, sticky=W + E
        )

        self.pasta_guias.insert(0, self.urls[4][1])
        self.pasta_guias.grid(row=5, column=2, padx=20)

        self.gravar_alterações.grid(
            row=6, column=2, columnspan=1, padx=15, pady=10, ipadx=10,
            ipady=13
        )


    def abrir_dados_de_transferencia_interna(self):
        self.dados_de_contas = Toplevel()
        self.dados_de_contas.title('Transferência interna')
        self.dados_de_contas.resizable(True, True)

        self.frame_geral_contas = LabelFrame(
            self.dados_de_contas, padx=0, pady=0
        )
        self.frame_geral_contas.pack()
        self.frame_remetente = LabelFrame(
            self.frame_geral_contas, padx=0, pady=0
        )
        self.frame_remetente.pack(padx=1, pady=1)

        self.remetente = StringVar()
        numero_de_contas = self.numero_contas()
        lista_de_contas = self.listar_dados_de_conta(numero_de_contas)
        dados_filtrado = self.filtrar_dados_de_conta(lista_de_contas)

        self.remetente.set('Conta remetente')
        self.lista_remetente = OptionMenu(self.frame_remetente, self.remetente, *dados_filtrado)
        self.lista_remetente.config(width=50)
        self.lista_remetente.grid(row=1, column=1, padx=30, pady=30)

        self.valor_a_transferir_label = Label(self.frame_geral_contas, text='Valor a transferir')
        self.valor_a_transferir_label.pack()

        self.valor_a_transferir = Entry(self.frame_geral_contas, width=10, font=('Helvetica', 14))
        self.valor_a_transferir.pack(pady=5)

        self.frame_favorecido = LabelFrame(
            self.frame_geral_contas, padx=0, pady=0
        )
        self.frame_favorecido.pack(padx=1, pady=1)

        self.favorecido = StringVar()
        numero_de_contas2 = self.numero_contas()
        lista_de_contas2 = self.listar_dados_de_conta(numero_de_contas2)
        dados_filtrado2 = self.filtrar_dados_de_conta(lista_de_contas2)

        self.favorecido.set('Conta favorecido')
        self.lista_favorecido = OptionMenu(self.frame_favorecido, self.favorecido, *dados_filtrado2)
        self.lista_favorecido.config(width=50)
        self.lista_favorecido.grid(row=1, column=1, padx=30, pady=30)

        self.botao_submissao = Button(
            self.frame_geral_contas, text='Criar guia',
            command=self.submeter_dados_internos,
            bg='blue', fg='white', font=('Helvetica', 8, 'bold'), bd=1
        )
        self.botao_submissao.pack(pady=5)


    def submeter_dados_internos(self):
        self.gerar_constructor(interna_constructor, True)
        self.dados_de_contas.destroy()
        messagebox.showinfo('Rolou', 'Guia de transferência interna gerada!')


    def filtrar_dados_de_conta(self, lista_de_dados_conta):
        lista_filtrada = []
        for lista in lista_de_dados_conta:
            item = f'{lista[0]} {lista[1]} - conta: {lista[5]}'
            lista_filtrada.append(item)
        return lista_filtrada


    def listar_dados_de_conta(self, lista_de_contas):
        lista_de_dados_conta = []
        for conta in lista_de_contas:
            dados_de_conta = self.pegar_conta_por_numero(conta[0])
            conta_id = dados_de_conta[0]
            lista_de_dados_conta.append(conta_id)
        return lista_de_dados_conta




if __name__ == '__main__':
    tela = ctk.CTk()
    style = ttk.Style()
    style.configure("TButton",
                         bg="red",  # Cor de fundo dos botões
                         fg="black",  # Cor do texto dos botões
                         font=("Times", 10))
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    tela.title('Teste CTk')
    tela.geometry("330x440")
    tela.resizable(1, 1)
    objeto_tela = Interface(tela)
    tela.config(menu=objeto_tela.menu)
    tela.mainloop()




































# from datetime import date
# from tkinter import *
# from tkinter import ttk
# from tkcalendar import Calendar
# from typing import Dict
#
# from src.constantes import *
# from src.main.constructor.transfer_constructor import transfer_constructor
#
# class ViewInicial(Frame):
#     def __init__(self, gerador):
#         super().__init__(gerador)
#         self.pack(expand=True, fill='both')
#         self.criar_widgets()
#
#
#     def criar_widgets(self):
#         self.frame_mestre = LabelFrame(self, padx=0, pady=0)
#
#         self.frame_1 = LabelFrame(self.frame_mestre, padx=0, pady=0)
#         self.frame_calendario = LabelFrame(self.frame_mestre, padx=0, pady=0)
#         self.frame_2 = LabelFrame(self.frame_mestre, padx=0, pady=0)
#
#         self.local = StringVar()
#         self.local.set(ORIGEM[0])
#         self.conta_origem = OptionMenu(self.frame_1, self.local, ORIGEM)
#
#         self.teste4 = Button(self.frame_2, text='Gerar pagamentos', command=lambda: self.gerar_constructor(transfer_constructor))
#         self.teste5 = Button(self.frame_2, text='Gerar pagamentos', command=self.dados_de_entrada)
#         self.teste6 = Button(self.frame_2, text='Gerar pagamentos', command=self.dados_de_entrada)
#
#         self.data_hoje = date.today()
#         dia = int(self.data_hoje.strftime('%d'))
#         mes = int(self.data_hoje.strftime('%m'))
#         ano = int(self.data_hoje.strftime('%Y'))
#
#         self.calendario = Calendar(
#             self.frame_calendario,
#             selectmode='day',
#             year=ano,
#             month=mes,
#             day=dia,
#             locale="pt_br"
#         )
#         self.criar_layout()
#
#
#     def criar_layout(self):
#         self.frame_mestre.pack(fill="both", expand=1, padx=10, pady=10)
#         self.frame_1.pack(fill="both", padx=10, pady=0, ipady=0)
#         self.frame_calendario.pack(fill="both", padx=10, pady=0, ipady=0)
#         self.frame_2.pack(fill="both", padx=10, pady=10)
#         self.conta_origem.grid(row=0, column=0)
#         self.teste4.grid(row=0, column=1)
#         self.teste5.grid(row=1, column=1)
#         self.teste6.grid(row=2, column=1)
#         self.calendario.grid(row=0, column=0)
#
#
#     def gerar_constructor(self, constructor):
#         entrada = self.dados_de_entrada()
#         resposta = constructor(entrada)
#         self.transfer_text(resposta)
#
#
#     def dados_de_entrada(self) -> Dict:
#         entradas = {
#             'origem': self.local.get(),
#             'data': self.data_de_pagamento()
#         }
#         return entradas
#
#
#     def data_de_pagamento(self):
#         data_calendario = self.calendario.get_date()
#         dia = data_calendario[0:2]
#         mes = data_calendario[3:5]
#         ano = data_calendario[6:]
#         data_de_pagamento = f'{ano}-{mes}-{dia}'
#         return data_de_pagamento
#
#
#     def transfer_text(self, resposta):
#         self.frame_mestre.destroy()
#
#         # self.frame_mestre = LabelFrame(self, padx=0, pady=0)
#         # self.frame_mestre.pack(fill="both", expand=1, padx=10, pady=10)
#
#         # self.texto = Label(self.frame_mestre, text=resposta)
#         # self.texto.pack()
#
#         # self.Bvoltar = Button(self.frame_mestre, text='Tela inicial', command=self.voltar)
#         # self.Bvoltar.pack()
#         #
#         self.frame_barra = LabelFrame(self, padx=0, pady=0, bg='red')
#         self.frame_barra.pack(padx=10, pady=10)
#
#         self.barra = ttk.Progressbar(self.frame_barra, orient=HORIZONTAL, length=300)
#         self.barra['value'] = 80
#         self.barra.pack()
#
#         self.valor_executado = Label(
#             self.frame_barra,
#             text=f'Total executado xx'
#         )
#         self.valor_executado.pack()
#
#
#     def voltar(self):
#         self.frame_mestre.destroy()
#         self.criar_widgets()
#
#
