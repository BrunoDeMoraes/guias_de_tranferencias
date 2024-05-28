from abc import ABC, abstractmethod

class Guia(ABC):

    @abstractmethod
    def gerar_guia(self):
        pass
