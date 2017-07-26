from abc import ABCMeta, abstractmethod


class Encoder(metaclass=ABCMeta):
    @abstractmethod
    def generate_class(self, diagram):
        """ Generate a class from the supplied diagram"""
