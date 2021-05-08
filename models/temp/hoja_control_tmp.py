class HojaControlTMP:
    def __init__(self, id, codigo, fk_cliente, cliente, tipo_cliente, tds, ppm, visitas, fecha_comprado):
        self.id = id
        self.codigo = codigo
        self.fk_cliente = fk_cliente
        self.cliente = cliente
        self.tipo_cliente = tipo_cliente
        self.tds = tds
        self.ppm = ppm
        self.visitas = visitas
        self.fecha_comprado = fecha_comprado
        
    @property
    def data(self):
        if self.fecha_comprado:
            self.fecha_comprado = str(self.fecha_comprado.isoformat())

        return {
            'id': self.id,
            'codigo': self.codigo,
            'fk_cliente': self.fk_cliente,
            'cliente': self.cliente,
            'tipo_cliente': self.tipo_cliente,
            'tds': self.tds,
            'ppm': self.ppm,
            'visitas': self.visitas,
            'fecha_comprado': self.fecha_comprado    
            
        }