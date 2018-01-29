class Alarma:
    def __init__(self, tiempo=0, sonido=''):
        self.__tiempo = tiempo
        self.__sonido = sonido

    def getTiempo(self):
        return self.__tiempo

    def getSonido(self):
        return  self.__sonido

    def setTiempo(self, tiempo):
        self.__tiempo = tiempo

    def setSonido(self, sonido):
        self.__sonido = sonido