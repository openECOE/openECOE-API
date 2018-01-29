from Usuario import Usuario

class Organizacion:
    def __init__(self, id_organizacion=0, nombre='', usuarios=[]):
        self.__id_organizacion = id_organizacion
        self.__nombre = nombre
        self.__usuarios = usuarios

    def getIdOrganizacion(self):
        return self.__id_organizacion

    def getNombre(self):
        return self.__nombre

    def getUsuarios(self):
        return self.__usuarios

    def setIdOrganizacion(self, id_organizacion):
        self.__id_organizacion = id_organizacion

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setUsuarios(self, usuarios):
        self.__usuarios = usuarios