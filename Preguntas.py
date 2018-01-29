from Opcion import Opcion
from Area import Area

class Pregunta:
    def __init__(self, referencia='', tipoPregunta='', areaPregunta = Area(), opcion=[]):
        self.__referencia = referencia
        self.__tipoPregunta = tipoPregunta
        self.__areaPregunta = areaPregunta
        self.__opcion = opcion

    def getReferencia(self):
        return self.__referencia

    def getTipoPregunta(self):
        return self.__tipoPregunta

    def getAreaPregunta(self):
        return self.__areaPregunta

    def getOpcion(self):
        return self.__opcion

    def setReferencia(self, referencia):
        self.__referencia = referencia

    def setTipoPregunta(self, tipoPregunta):
        self.__tipoPregunta = tipoPregunta

    def setAreaPregunta(self, areaPregunta):
        self.__areaPregunta = areaPregunta

    def setOpcion(self, opcion):
        self.__opcion = opcion