from Turno import Turno


class Dia:
    def __init__(self, cod_dia='', fecha='', turnos = []):
        self.__cod_dia = cod_dia
        self.__fecha = fecha
        self.__turnos = turnos

    def getCodDia(self):
        return self.__cod_dia

    def getFecha(self):
        return self.__fecha

    def getTurnos(self):
        return self.__turnos

    def setCodDia(self, cod_dia):
        self.__cod_dia = cod_dia

    def setFecha(self, fecha):
        self.__fecha = fecha

    def setTurnos(self, turnos):
        self.__turnos = turnos