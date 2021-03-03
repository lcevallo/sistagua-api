class TipoCargo:
    def __init__(self,__id, tipo,publish):
        self.__id=__id
        self.tipo = tipo
        self.publish = publish
    
    @property
    def data(self):
        return {
            'id': self.__id,
            'tipo': self.tipo,
            'publish': self.publish
            }