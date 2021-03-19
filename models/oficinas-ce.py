class OficinasCE:
    def __init__(self,id, fk_cliente_empresarial, fk_provincia, fk_canton, fk_parroquia, sector, direccion, telefono_convencional, created_at, updated_at, publish):
        self.id=id
        self.fk_cliente_empresarial=fk_cliente_empresarial
        self.fk_provincia=fk_provincia
        self.fk_canton=fk_canton
        self.fk_parroquia=fk_parroquia
        self.sector=sector
        self.direccion=direccion
        self.telefono_convencional=telefono_convencional
        self.created_at=created_at
        self.updated_at=updated_at
        self.publish=publish
        
    @property
    def data(self):
        if self.created_at:
            self.created_at = str(self.created_at.isoformat())
        
        if self.updated_at:
            self.updated_at = str(self.updated_at.isoformat())
               
        return {
                'id': self.id,
                'fk_cliente_empresarial': self.fk_cliente_empresarial,
                'fk_provincia': self.fk_provincia,
                'fk_canton': self.fk_canton,
                'fk_parroquia': self.fk_parroquia,
                'sector': self.sector,
                'direccion': self.direccion,
                'telefono_convencional': self.telefono_convencional,
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'publish': self.publish
        }