class DireccionCliente:
    def __init__(self,__id, fk_cliente, fk_provincia, fk_canton, fk_parroquia, direccion_domiciliaria, direccion_oficina, telefono_convencional, publish):
        self.__id=__id
        self.fk_cliente=fk_cliente
        self.fk_provincia=fk_provincia
        self.fk_canton=fk_canton
        self.fk_parroquia=fk_parroquia
        self.direccion_domiciliaria=direccion_domiciliaria
        self.direccion_oficina=direccion_oficina
        self.telefono_convencional=telefono_convencional
        self.publish=publish
    
    @property
    def data(self):
        return {
            'id': self.__id,
            'fk_cliente': self.fk_cliente,
            'fk_provincia': self.fk_provincia,
            'fk_canton': self.fk_canton,
            'fk_parroquia': self.fk_parroquia,
            'direccion_domiciliaria': self.direccion_domiciliaria,
            'direccion_oficina': self.direccion_oficina,
            'telefono_convencional': self.telefono_convencional,
            'publish': self.publish
        }
