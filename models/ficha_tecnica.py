class FichaTecnica:
    def __init__(self, __id, fk_cliente, tds, ppm, visitas, fecha_comprado, created_at, updated_at, publish):
        self.__id= __id
        self.fk_cliente=fk_cliente
        self.tds=tds
        self.ppm=ppm
        self.visitas=visitas
        self.fecha_comprado=fecha_comprado
        self.created_at=created_at
        self.updated_at=updated_at
        self.publish=publish
    
    @property
    def data(self):
        if self.created_at:
            self.created_at = str(self.created_at.utcnow())
        if self.updated_at:
            self.updated_at = str(self.updated_at.utcnow())

        return {
            'id': self.__id,
            'fk_cliente': self.fk_cliente,
            'tds': self.tds,
            'ppm': self.ppm,
            'visitas': self.visitas,
            'fecha_comprado': self.fecha_comprado,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'publish': self.publish
        }