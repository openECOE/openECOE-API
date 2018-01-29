from Alumno import Alumno

class Rueda:
    def __init__(self, cod_rueda=0, descripcion='', alumnos = []):
        self.__cod_rueda = cod_rueda
        self.__descripcion = descripcion
        self.__alumnos = alumnos

    def getCodRueda(self):
        return self.__cod_rueda

    def getDescripcion(self):
        return  self.__descripcion

    def getAlumnos(self):
        return  self.__alumnos

    def setCodRueda(self, cod_rueda):
        self.__cod_rueda = cod_rueda

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def setAlumnos(self, tiempoTotal):
        self.__alumnos = tiempoTotal
