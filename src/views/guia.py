from abc import ABC, abstractmethod


class Guia(ABC):

    def mm(self, medida):
        return (medida/0.352777)
    @abstractmethod
    def gerar_guia(self):
        pass

    def gerar_linhas(self):
        pass

