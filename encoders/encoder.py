from abc import ABCMeta, abstractmethod


class Encoder(metaclass=ABCMeta):
    @abstractmethod
    def create_class(self, diagram):
        """ Generate a class from the supplied diagram"""
