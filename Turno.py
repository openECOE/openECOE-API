from Rueda import Rueda

class Turno:
    def __init__(self, cod_turno='', horaInicio=0, ruedas = []):
        self.__cod_turno = cod_turno
        self.__horaInicio = horaInicio
        self.__ruedas = ruedas

    def getCodTurno(self):
        return self.cod_turno

    def getHoraInicio(self):
        return  self.__horaInicio

    def getRuedas(self):
        return  self.__ruedas

    def setCodTurno(self, cod_turno):
        self.__cod_turno = cod_turno

    def setHoraInicio(self, horaInicio):
        self.__horaInicio = horaInicio

    def setRuedas(self, ruedas):
        self.__ruedas = ruedas
