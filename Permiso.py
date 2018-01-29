class Permiso:
    def __init__(self, id_tipo_permiso, id_permiso, id_objeto):
        self.__id_tipo_permiso = id_tipo_permiso
        self.__id_permiso = id_permiso
        self.__id_objeto = id_objeto

    def getIdTipoPermiso(self):
        return self.__id_permiso

    def getIdPermiso(self):
        return self.__id_permiso

    def getIdObjeto(self):
        return self.__id_objeto

    def setIdTipoPermiso(self, id_tipo_permiso):
        self.__id_tipo_permiso = id_tipo_permiso

    def setIdPermiso(self, id_permiso):
        self.__id_permiso = id_permiso

    def setIdObjeto(self, id_objeto):
        self.__id_objeto = id_objeto
