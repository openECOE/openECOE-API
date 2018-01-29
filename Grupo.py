from Preguntas import Pregunta

class Grupo:
    def __init__(self, id_grupo, nombre='', preguntas=[]):
        self.__id_grupo = id_grupo
        self.__nombre = nombre
        self.__preguntas = preguntas

    def getIdGrupo(self):
        return self.__id_grupo

    def getNombre(self):
        return self.__nombre

    def getPreguntas(self):
        return self.__preguntas

    def setIdGrupo(self, id_grupo):
        self.__id_grupo = id_grupo

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setPreguntas(self, preguntas):
        self.__preguntas = preguntas

