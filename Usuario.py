from Permiso import Permiso

class Usuario:
    def __init__(self, id_usuario=0, nombre='', apellidos='', permisos=[]):
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__permisos = permisos

    def getIdUsuario(self):
        return self.__id_usuario

    def getNombre(self):
        return self.__id_usuario

    def getApellidos(self):
        return self.__apellidos

    def getPermisos(self):
        return self.__permisos

    def setIdUsuario(self, id_usuario):
        self.__id_usuario = id_usuario

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setApellidos(self, apellidos):
        self.__apellidos = apellidos

    def setPermisos(self, permisos):
        self.__permisos = permisos
