class OficinasVCE:
    def __init__(self, id, fk_cliente_empresarial, fk_provincia, fk_canton, fk_parroquia, sector, direccion,
                 telefono_convencional, provincia, canton, parroquia):
        self.id = id
        self.fk_cliente_empresarial = fk_cliente_empresarial
        self.fk_provincia = fk_provincia
        self.fk_canton = fk_canton
        self.fk_parroquia = fk_parroquia
        self.sector = sector
        self.direccion = direccion
        self.telefono_convencional = telefono_convencional
        self.provincia = provincia
        self.canton = canton
        self.parroquia = parroquia

    @property
    def data(self):
        return {
            'id': self.id,
            'fk_cliente_empresarial': self.fk_cliente_empresarial,
            'fk_provincia': self.fk_provincia,
            'fk_canton': self.fk_canton,
            'fk_parroquia': self.fk_parroquia,
            'sector': self.sector,
            'direccion': self.direccion,
            'telefono_convencional': self.telefono_convencional,
            'provincia': self.provincia,
            'canton': self.canton,
            'parroquia': self.parroquia
        }
