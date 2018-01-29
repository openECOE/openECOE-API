from Alarma import Alarma

class Cronometro:
    def __init__(self, id_cronometro=0, nombre='', tiempoTotal=0, alarmas = []):
        self.__id_cronometro = id_cronometro
        self.__nombre = nombre
        self.__tiempoTotal = tiempoTotal
        self.__alarmas = alarmas

    def getCronometro(self):
        return self.__id_cronometro

    def getNombre(self):
        return  self.__nombre

    def getTiempoTotal(self):
        return  self.__tiempoTotal

    def getAlarmas(self):
        return  self.__alarmas

    def setCronometro(self, id_cronometro):
        self.__id_cronometro = id_cronometro

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setTiempoTotal(self, tiempoTotal):
        self.__tiempoTotal = tiempoTotal

    def setAlarmas(self, alarmas):
        self.__alarmas = alarmas