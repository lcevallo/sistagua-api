class HojaControlDetalle:
    def __init__(self, id, fk_hoja_control, factura, fecha_mantenimiento, recibo, hoja_control, descripcion, persona_autoriza, firma_url, cedula_autoriza, persona_dio_mantenimiento, cedula_dio_mantenimiento, ppm, tds, created_at, updated_at, publish):
        self.id = id
        self.fk_hoja_control = fk_hoja_control
        self.factura = factura
        self.fecha_mantenimiento = fecha_mantenimiento
        self.recibo = recibo
        self.hoja_control = hoja_control
        self.descripcion = descripcion
        self.persona_autoriza = persona_autoriza
        self.firma_url = firma_url
        self.cedula_autoriza = cedula_autoriza
        self.persona_dio_mantenimiento = persona_dio_mantenimiento
        self.cedula_dio_mantenimiento = cedula_dio_mantenimiento
        self.ppm = ppm
        self.tds = tds
        self.created_at = created_at
        self.updated_at = updated_at
        self.publish = publish

    @property
    def data(self):

        if self.updated_at:
            self.updated_at = str(self.updated_at.isoformat())

        if self.created_at:
            self.created_at = str(self.created_at.isoformat())

        return {
            'id': self.id,
            'fk_hoja_control': self.fk_hoja_control,
            'factura': self.factura,
            'fecha_mantenimiento': self.fecha_mantenimiento,
            'recibo': self.recibo,
            'hoja_control': self.hoja_control,
            'descripcion': self.descripcion,
            'persona_autoriza': self.persona_autoriza,
            'firma_url': self.firma_url,
            'cedula_autoriza': self.cedula_autoriza,
            'persona_dio_mantenimiento': self.persona_dio_mantenimiento,
            'cedula_dio_mantenimiento': self.cedula_dio_mantenimiento,
            'ppm': self.ppm,
            'tds': self.tds,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'publish': self.publish
        }