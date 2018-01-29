class Alumno:
    def __init__(self, id_alumno='', nombre='', DNI=''):
        self.__id_alumno = id_alumno
        self.__nombre = nombre
        self.__DNI = DNI

    def getIdAlumno(self):
        return self.__id_alumno

    def getNombre(self):
        return  self.__nombre

    def getDNI(self):
        return  self.__DNI


    def setIdAlumno(self, idAlumno):
        self.__id_alumno = idAlumno

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setDNI(self, DNI):
        self.__DNI = DNI