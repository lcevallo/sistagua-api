class TipoCargo:
    def __init__(self,__id, tipo):
          self.__id=__id
          self.tipo = tipo
    
    @property
    def data(self):
        return {
            'id': self.__id,
            'tipo': self.tipo
               }