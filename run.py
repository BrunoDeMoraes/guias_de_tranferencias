from tkinter import *

from src.views.Gerador_de_view import Interface

if __name__ == '__main__':
    # Gerador_de_views()

    tela = Tk()
    tela.geometry("300x500")
    tela.resizable(0, 0)
    objeto_tela = Interface(tela)
    tela.title()
    tela.config(menu=objeto_tela.menu)
    tela.mainloop()
