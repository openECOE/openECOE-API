from Grupo import Grupo
from Cronometro import Cronometro

class Estacion:
    def __init__(self, id_estacion=0, nombre='', grupos=[], cronometros=[]):
        self.__id_estacion = id_estacion
        self.__nombre = nombre
        self.__grupos = grupos
        self.__cronometros = cronometros

    def getIdEstacion(self):
        return self.__id_estacion

    def getNombre(self):
        return self.__nombre

    def getGrupos(self):
        return self.__grupos

    def getCronometros(self):
        return self.__cronometros

    def setIdEstacion(self, id_estacion):
        self.__id_estacion = id_estacion

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setGrupos(self, grupos):
        self.__grupos = grupos

    def setCronometros(self, cronometros):
        self.__cronometros = cronometros