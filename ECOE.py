from Area import Area
from Alumno import Alumno
from Estacion import Estacion
from Dia import Dia
from Cronometro import Cronometro

class ECOE:
    def __init__(self, id_ecoe=0, nombre='', areas = [], alumnos=[], estaciones=[], dias=[], cronometros=[]):
        self.__id_ecoe = id_ecoe
        self.__nombre = nombre
        # TODO: Crear array de objetos Area
        self.__areas = areas
        self.__alumnos = alumnos
        self.__estaciones = estaciones
        self.__dias = dias
        self.__cronometros = cronometros

    def getIdECOE(self):
        return self.__id_ecoe

    def getNombre(self):
        return self.__nombre

    def getAreas(self):
        return self.__areas

    def getAlumnos(self):
        return self.__alumnos

    def getEstaciones(self):
        return self.__estaciones

    def getDias(self):
        return self.__dias

    def getCronometros(self):
        return self.__cronometros

    def setIdECOE(self, id_ecoe):
        self.__id_ecoe = id_ecoe

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setAreas(self, areas):
        self.__areas = areas

    def setAlumnos(self, alumnos):
        self.__alumnos = alumnos

    def setEstaciones(self, estaciones):
        self.__estaciones = estaciones

    def setDias(self, dias):
        self.__dias = dias

    def setCronometros(self, cronometros):
        self.__cronometros = cronometros