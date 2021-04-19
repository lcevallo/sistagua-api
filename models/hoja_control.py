class HojaControl:
    def __init__(self, id, fk_cliente, tipo_cliente, codigo, tds, ppm, visitas, fecha_comprado, created_at, updated_at, publish):
        self.id = id
        self.fk_cliente = fk_cliente
        self.tipo_cliente = tipo_cliente
        self.codigo = codigo
        self.tds = tds
        self.ppm = ppm
        self.visitas = visitas
        self.fecha_comprado = fecha_comprado
        self.created_at = created_at
        self.updated_at = updated_at
        self.publish = publish

    @property
    def data(self):

        if self.updated_at:
            self.updated_at = str(self.updated_at.isoformat())

        if self.created_at:
            self.created_at = str(self.created_at.isoformat())
            
        if self.fecha_comprado:
            self.fecha_comprado = str(self.fecha_comprado.isoformat())

        return {
             'id': self.id,
             'fk_cliente': self.fk_cliente,
             'tipo_cliente': self.tipo_cliente,
             'codigo': self.codigo,
             'tds': self.tds,
             'ppm': self.ppm,
             'visitas': self.visitas,
             'fecha_comprado': self.fecha_comprado,
             'created_at': self.created_at,
             'updated_at': self.updated_at,
             'publish': self.publish
        }
