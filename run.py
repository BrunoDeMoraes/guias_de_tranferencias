from tkinter import *
from tkinter import ttk

import customtkinter as ctk

from src.views.view_inicial import Interface

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
