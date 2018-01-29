class Opcion:
    def __init__(self, id_opcion, valor=0, descripcion=''):
        self.__id_opcion = id_opcion
        self.__valor = valor
        self.__descripcion = descripcion

    def getIdOpcion(self):
        return self.__id_opcion

    def getValor(self):
        return self.__valor

    def getDescripcion(self):
        return self.__descripcion

    def setIdOpcion(self, id_opcion):
        self.__id_opcion = id_opcion

    def setValor(self, valor):
        self.__valor = valor

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion
