from tkinter import *

from src.views.Gerador_de_view import Interface

if __name__ == '__main__':
    tela = Tk()
    tela.geometry("300x450")
    tela.resizable(1, 1)
    objeto_tela = Interface(tela)
    tela.title()
    tela.config(menu=objeto_tela.menu)
    tela.mainloop()
