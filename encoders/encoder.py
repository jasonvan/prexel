from abc import ABCMeta, abstractmethod


class Encoder(metaclass=ABCMeta):
    @abstractmethod
    def generate(self, diagram):
        """ Generate a output from the supplied diagram"""
