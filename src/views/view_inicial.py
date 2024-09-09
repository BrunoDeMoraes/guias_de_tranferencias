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

from src.constantes import PLANILHA_INEXISTENTE

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
        self.menu_configurações = tk.Menu(
            self.menu,
            tearoff=0,
            bg='#1F538D',
            fg='silver',
            borderwidth=0
        )
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

        self.calendario = Calendar(
            self.frame_calendario,
            selectmode='day',
            year=ano,
            month=mes,
            day=dia,
            locale="pt_br"
        )
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
        self.lista_de_comandos = ctk.CTkOptionMenu(
            self.frame_2,
            values=self.comandos,
            variable=self.comando
        )
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
            messagebox.showerror(
                'De novo, mano',
                'O arquivo já existe. Se quiser criar novamente, apaga lá primeiro!'
            )
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
        if self.configurar_pasta_guia():
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
            try:
                tipo_de_comando[comando_escolhido]()
                if comando_escolhido not in ['Mesclar arquivos', 'Transferência interna']:
                    messagebox.showinfo('Parece que rolou!', f'Tudo certo!!!')
            except KeyError:
                messagebox.showerror('Tem nada selecionado','Seleciona uma opção aí ou não vai rolar!')
            finally:
                self.finalizar_barra_de_progresso()


    def progresso_continuo(self):
        while self.executor:
            total = self.valor_progresso.get()
            if total == 0.99:
                continue
            else:
                self.valor_progresso.set((total + 0.01))
                time.sleep(1)


    def gerar_todas_as_guias(self):
        self.comando_atual = 'Transferências BRB'
        self.gerar_processo(transfer_constructor)
        self.comando_atual = 'TEDs'
        self.gerar_processo(ted_constructor)
        self.comando_atual = 'ISS'
        self.gerar_processo(iss_constructor)
        self.comando_atual = 'IR'
        self.gerar_processo(ir_constructor)
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
        tr = threading.Thread(target=self.selecionar_tipo_de_guia)
        tr.start()


    def inicializar_barra_de_progresso(self):
        self.executor = True
        thread_checagem_true = threading.Thread(target=self.progresso_continuo)
        thread_checagem_true.start()


    def gerar_constructor(self, constructor, dados_internos=False):

        entrada = self.dados_de_entrada(dados_internos)
        constructor(entrada)
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
        self.valor_executado.configure(
            text=f'Gerando {tipo_de_guia}: {self.comando_atual} {int(progresso * 100)}%'
        )


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


    # def transfer_text(self, resposta):
    #     self.texto = Label(self.frame_mestre, text=resposta)
    #     self.Bvoltar = Button(self.frame_mestre, text='Tela inicial', command=self.voltar)
    #     self.texto.pack()
    #     self.Bvoltar.pack()


    def voltar(self):
        self.frame_mestre.destroy()
        self.criar_widgets()


    def abrir_janela_cadastro(self):
        self.janela_de_cadastro = ctk.CTkToplevel()
        self.janela_de_cadastro.geometry('1000x300')
        self.janela_de_cadastro.title('Cadastro de contas')
        self.janela_de_cadastro.resizable(0, 0)

        self.frame_geral = ctk.CTkFrame(
            self.janela_de_cadastro
        )
        self.frame_geral.pack(padx=1, pady=1)

        self.frame_de_cadastro = ctk.CTkFrame(
            self.frame_geral
        )
        self.frame_de_cadastro.pack(padx=1, pady=1)

        self.frame_de_exclusao = ctk.CTkFrame(
            self.frame_geral
        )
        self.frame_de_exclusao.pack(padx=1, pady=1)

        self.frame_display = ctk.CTkFrame(
            self.frame_geral
        )
        self.frame_display.pack(padx=1, pady=1)

        self.frame_geral.pack(padx=1, pady=1)

        self.titulo_origem = ctk.CTkLabel(
            self.frame_de_cadastro,
            text="Origem",
            padx=50
        )

        self.origem_bd = ctk.StringVar()
        self.origem_bd.set(Interface.ORIGEM[0])
        self.lista_origem_bd = ctk.CTkOptionMenu(
            self.frame_de_cadastro,
            variable=self.origem_bd,
            values=Interface.ORIGEM
        )
        self.lista_origem_bd.configure()

        self.titulo_recurso = ctk.CTkLabel(
            self.frame_de_cadastro,
            text="Recurso"
        )

        self.recurso_bd = ctk.StringVar()
        self.recurso_bd.set(Interface.RECURSO[0])
        self.lista_recurso_bd = ctk.CTkOptionMenu(
            self.frame_de_cadastro,
            variable=self.recurso_bd,
            values=Interface.RECURSO
        )
        self.lista_recurso_bd.configure()

        self.titulo_tipo = ctk.CTkLabel(
            self.frame_de_cadastro,
            text="Tipo",
            padx=50
        )
        self.tipo_bd = ctk.StringVar()
        self.tipo_bd.set(Interface.TIPO[0])
        self.lista_tipo_bd = ctk.CTkOptionMenu(
            self.frame_de_cadastro,
            variable=self.tipo_bd,
            values=Interface.TIPO
        )
        self.lista_tipo_bd.configure()

        self.titulo_banco = ctk.CTkLabel(
            self.frame_de_cadastro,
            text="Banco"
        )

        self.bancos = []
        for banco in Interface.BANCO.keys():
            self.bancos.append(banco)
        self.banco_bd = ctk.StringVar()
        self.banco_bd.set("BRB")
        self.lista_banco_bd = ctk.CTkOptionMenu(
            self.frame_de_cadastro,
            variable=self.banco_bd,
            values=self.bancos
        )
        self.lista_banco_bd.configure()

        self.titulo_agencia = ctk.CTkLabel(
            self.frame_de_cadastro,
            text="Agência"
        )

        self.n_agencia = ctk.CTkEntry(
            self.frame_de_cadastro, width=50
        )

        self.titulo_conta = ctk.CTkLabel(
            self.frame_de_cadastro,
            text="Conta"
        )

        self.n_conta = ctk.CTkEntry(
            self.frame_de_cadastro, width=85
        )

        self.titulo_cnpj = ctk.CTkLabel(self.frame_de_cadastro, text="CNPJ")

        self.n_cnpj = ctk.CTkEntry(
            self.frame_de_cadastro, width=130
        )

        self.botao_cadastro = ctk.CTkButton(self.frame_de_cadastro, text="Cadastrar", command=self.submeter_conta)

        self.titulo_origem.grid(row=0, column=1)
        self.titulo_recurso.grid(row=0, column=2)
        self.titulo_tipo.grid(row=0, column=3)
        self.titulo_banco.grid(row=0, column=4)
        self.titulo_agencia.grid(row=0, column=5)
        self.titulo_conta.grid(row=0, column=6)
        self.titulo_cnpj.grid(row=0, column=7)

        self.lista_origem_bd.grid(row=1, column=1, padx=10)
        self.lista_recurso_bd.grid(row=1, column=2, padx=10)
        self.lista_tipo_bd.grid(row=1, column=3, padx=10)
        self.lista_banco_bd.grid(row=1, column=4, padx=10)
        self.n_agencia.grid(row=1, column=5, padx=10)
        self.n_conta.grid(row=1, column=6, padx=10)
        self.n_cnpj.grid(row=1, column=7, padx=10)

        self.botao_cadastro.grid(row=2, column=1, columnspan=7, pady=10, sticky='e', padx=10)

        self.opcoes_de_exclusao = ctk.CTkLabel(
            self.frame_de_exclusao, text="Caso deseje excluir uma conta, utilize a opção abaixo:")

        self.v_contas = ctk.StringVar()


        self.atualizar_contas()

        numeros_de_contas_tupla = self.numero_contas()
        numeros_de_contas = []
        self.v_contas.set('Selecione uma conta')
        for i in numeros_de_contas_tupla:
            numeros_de_contas.append(i[0])

        self.v_contas_bd = ctk.CTkOptionMenu(self.frame_de_exclusao, variable=self.v_contas, values=numeros_de_contas, width=200)

        self.botao_excluir = ctk.CTkButton(self.frame_de_exclusao, text="Excluir conta", command=self.excluir_conta)

        self.opcoes_de_exclusao.grid(row=0, column=1, columnspan=2)
        self.v_contas_bd.grid(row=1, column=1, padx=30)
        self.botao_excluir.grid(row=1, column=2, padx=30)

        self.display = ctk.CTkLabel(self.frame_display, text='', width=200, height=150)
        self.display.pack()

        self.v_contas.trace('w', self.atualiza_label_cadastro)


    def atualiza_label_cadastro(self, *args):
        conta = self.v_contas.get()

        dados_conta = self.pegar_conta_por_numero(conta)

        try:
            origem_tipo = dados_conta[0][0].split()
            texto = (f'Origem: {origem_tipo[0]}\n'
                     f'Tipo: {origem_tipo[1]}\n'
                     f'Recurso: {dados_conta[0][1]}\n'
                     f'Banco: {dados_conta[0][3]}\n'
                     f'Agência: {dados_conta[0][4]}\n'
                     f'Conta: {dados_conta[0][5]}\n'
                     f'CNPJ: {dados_conta[0][6]}')
            self.display.configure(text=texto)
        except IndexError:
            self.display.configure(text='')





    def atualizar_contas(self):
        if self.numero_contas() == []:
            numeros_de_contas_tupla = ["Nenhuma conta cadastrada"]
        else:
            numeros_de_contas_tupla = self.numero_contas()
        numeros_de_contas = []
        for i in numeros_de_contas_tupla:
            numeros_de_contas.append(i[0])
        self.v_contas_bd = ctk.CTkOptionMenu(
            self.frame_de_exclusao,
            variable=self.v_contas,
            values=numeros_de_contas,
            width=200
        )
        self.v_contas.set('Selecione uma conta')
        self.v_contas_bd.grid(row=1, column=1, padx=30)


    def submeter_conta(self):
        if self.n_agencia.get() == '' or self.n_conta.get() == '' or self.n_cnpj.get() == '':
            messagebox.showerror('Tem campo vazio', 'Preencha os campos agência, conta e CNPJ.')
        else:
            self.cadastrar_conta(
                self.origem_bd.get(),
                self.recurso_bd.get(),
                self.tipo_bd.get(),
                Interface.BANCO[self.banco_bd.get()],
                self.n_agencia.get(),
                self.n_conta.get(),
                self.n_cnpj.get()
            )
            self.atualizar_contas()
            self.n_agencia.delete(0, ctk.END)
            self.n_conta.delete(0, ctk.END)
            self.n_cnpj.delete(0, ctk.END)


    def numero_contas(self):
        contas = list(self.pegar_n_contas())
        return contas


    def excluir_conta(self):
        conta = self.v_contas.get()
        if conta == 'Selecione uma conta':
            messagebox.showerror('Tem nada selecionado','Seleciona uma opção aí ou não vai rolar!')
        else:
            self.deletar_conta(conta)
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
        self.caminhos = ctk.CTkToplevel()
        self.urls = self.consultar_registros(URLS)
        self.caminhos.title('Caminhos')
        self.caminhos.resizable(0, 0)
        self.frame_caminhos = ctk.CTkFrame(
            self.caminhos
        )
        self.frame_caminhos.pack(padx=1, pady=1)

        self.botao_xlsx = ctk.CTkButton(
            self.frame_caminhos, text='HRG Custeio',
            command=lambda: self.altera_caminho(self.caminho_srssu, True),
            font=('Helvetica', 12, 'bold')
        )
        self.caminho_srssu = ctk.CTkEntry(self.frame_caminhos, width=600)

        self.botao_pasta_de_certidões = ctk.CTkButton(
            self.frame_caminhos, text='APS Custeio',
            command=lambda: (
                self.altera_caminho(self.caminho_aps, True)),
            font=('Helvetica', 12, 'bold')
        )
        self.caminho_aps = ctk.CTkEntry(
            self.frame_caminhos, width=600
        )

        self.botao_log = ctk.CTkButton(
            self.frame_caminhos, text='HRG Investimento',
            command=lambda: self.altera_caminho(self.caminho_srssu_i, True),
            font=('Helvetica', 12, 'bold')
        )
        self.caminho_srssu_i = ctk.CTkEntry(self.frame_caminhos, width=600)

        self.certidões_para_pagamento = ctk.CTkButton(
            self.frame_caminhos, text='APS Investimento',
            command=lambda: (
                self.altera_caminho(self.caminho_aps_i, True)
            ),
            font=('Helvetica', 12, 'bold')
        )

        self.caminho_aps_i = ctk.CTkEntry(
            self.frame_caminhos, width=600
        )

        self.botao_pasta_guias = ctk.CTkButton(
            self.frame_caminhos, text='Pasta destino para guias',
            command=lambda: (
                self.altera_caminho(self.pasta_guias)
            ),
            font=('Helvetica', 12, 'bold'),
        )

        self.pasta_guias = ctk.CTkEntry(
            self.frame_caminhos, width=600
        )

        self.gravar_alterações = ctk.CTkButton(
            self.frame_caminhos, text='Gravar alterações',
            command=self.atualizar_caminhos,
            font=('Helvetica', 12, 'bold')
        )

        self.botao_xlsx.grid(
            row=1, column=1, columnspan=1, padx=15, pady=10, ipadx=5,
            ipady=13, sticky='we'
        )
        self.caminho_srssu.insert(0, self.urls[0][1])
        self.caminho_srssu.grid(row=1, column=2, padx=20)

        self.botao_pasta_de_certidões.grid(
            row=2, column=1, columnspan=1, padx=15, pady=10, ipadx=10,
            ipady=13, sticky='we'
        )

        self.caminho_aps.insert(0, self.urls[1][1])
        self.caminho_aps.grid(row=2, column=2, padx=20)

        self.botao_log.grid(
            row=3, column=1, columnspan=1, padx=15, pady=10, ipadx=10,
            ipady=13, sticky='we'
        )

        self.caminho_srssu_i.insert(0, self.urls[2][1])
        self.caminho_srssu_i.grid(row=3, column=2, padx=20)

        self.certidões_para_pagamento.grid(
            row=4, column=1, columnspan=1, padx=15, pady=10, ipadx=10,
            ipady=13, sticky='we'
        )

        self.caminho_aps_i.insert(0, self.urls[3][1])
        self.caminho_aps_i.grid(row=4, column=2, padx=20)

        self.botao_pasta_guias.grid(
            row=5, column=1, columnspan=1, padx=15, pady=10, ipadx=10,
            ipady=13, sticky='we'
        )

        self.pasta_guias.insert(0, self.urls[4][1])
        self.pasta_guias.grid(row=5, column=2, padx=20)

        self.gravar_alterações.grid(
            row=6, column=2, columnspan=1, padx=15, pady=10, ipadx=10,
            ipady=13
        )

    def configurar_pasta_guia(self):
        urls = self.consultar_registros(URLS)
        if not os.path.exists(urls[4][1]):
            messagebox.showerror(
                PLANILHA_INEXISTENTE[0],
                PLANILHA_INEXISTENTE[1]
            )
            return False
        else:
            return True


    def abrir_dados_de_transferencia_interna(self):
        self.dados_de_contas = ctk.CTkToplevel()
        self.dados_de_contas.title('Transferência interna')
        self.dados_de_contas.resizable(0, 0)

        self.frame_geral_contas = ctk.CTkFrame(
            self.dados_de_contas
        )
        self.frame_geral_contas.pack()
        self.frame_remetente = ctk.CTkFrame(
            self.frame_geral_contas
        )
        self.frame_remetente.pack(padx=1, pady=1)

        self.remetente = ctk.StringVar()
        numero_de_contas = self.numero_contas()
        lista_de_contas = self.listar_dados_de_conta(numero_de_contas)
        dados_filtrado = self.filtrar_dados_de_conta(lista_de_contas)

        self.remetente.set('Conta remetente')
        self.lista_remetente = ctk.CTkOptionMenu(
            self.frame_remetente,
            variable=self.remetente,
            values=dados_filtrado
        )
        self.lista_remetente.configure(width=350)
        self.lista_remetente.grid(row=1, column=1, padx=30, pady=30)

        self.valor_a_transferir_label = ctk.CTkLabel(
            self.frame_geral_contas,
            text='Valor a transferir'
        )
        self.valor_a_transferir_label.pack()

        self.valor_a_transferir = ctk.CTkEntry(
            self.frame_geral_contas, width=120,
            font=('Helvetica', 20)
        )
        self.valor_a_transferir.pack(pady=5)

        self.frame_favorecido = ctk.CTkFrame(
            self.frame_geral_contas
        )
        self.frame_favorecido.pack(padx=1, pady=1)

        self.favorecido = ctk.StringVar()
        numero_de_contas2 = self.numero_contas()
        lista_de_contas2 = self.listar_dados_de_conta(numero_de_contas2)
        dados_filtrado2 = self.filtrar_dados_de_conta(lista_de_contas2)

        self.favorecido.set('Conta favorecido')
        self.lista_favorecido = ctk.CTkOptionMenu(
            self.frame_favorecido,
            variable=self.favorecido,
            values=dados_filtrado2
        )
        self.lista_favorecido.configure(width=350)
        self.lista_favorecido.grid(row=1, column=1, padx=30, pady=30)

        self.botao_submissao = ctk.CTkButton(
            self.frame_geral_contas, text='Criar guia',
            command=self.submeter_dados_internos,
            font=('Helvetica', 12, 'bold')
        )
        self.botao_submissao.pack(pady=5)


    def submeter_dados_internos(self):
        self.gerar_constructor(interna_constructor, True)
        self.dados_de_contas.destroy()
        messagebox.showinfo(
            'Rolou',
            'Guia de transferência interna gerada!'
        )


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
    tela.resizable(0, 0)
    objeto_tela = Interface(tela)
    tela.config(menu=objeto_tela.menu)
    tela.mainloop()

