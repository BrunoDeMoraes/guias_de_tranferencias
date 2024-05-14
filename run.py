from tkinter import *


from src.main.process_handle import Process_handle

if __name__ == '__main__':
    tela = Tk()
    tela.geometry("300x500")
    tela.resizable(0, 0)
    objeto_tela = Process_handle(tela)
    tela.title()
    tela.config(menu=objeto_tela.menu)
    tela.mainloop()

