from abc import ABCMeta, abstractmethod

#Basically Encoder is an interface, we cannot create an instance of it, only use it as a superclass
class Encoder(metaclass=ABCMeta):
    @abstractmethod
    def generate(self, diagram):
        """ Generate a output from the supplied diagram"""
