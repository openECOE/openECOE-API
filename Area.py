class Area:
    def __init__(self, id_area=0, nombre=''):
        self.__id_area = id_area
        self.__nombre = nombre

    def getIdArea(self):
        return self.__id_area

    def getNombre(self):
        return  self.__nombre

    def setIdArea(self, id_area):
        self.__id_area = id_area

    def setNombre(self, nombre):
        self.__nombre = nombre