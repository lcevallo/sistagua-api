class HojaControlDetalleFiltracion:
    def __init__(self,id, fk_hoja_control_detalle, fk_filtracion, valor_filtracion, created_at, updated_at, publish, descripcion):
        self.id = id
        self.fk_hoja_control_detalle=fk_hoja_control_detalle
        self.fk_filtracion=fk_filtracion
        self.valor_filtracion=valor_filtracion
        self.created_at=created_at
        self.updated_at=updated_at
        self.publish=publish
        self.descripcion=descripcion

    @property
    def data(self):

        if self.updated_at:
            self.updated_at = str(self.updated_at.isoformat())

        if self.created_at:
            self.created_at = str(self.created_at.isoformat())

        return {
            'id': self.id,
            'fk_hoja_control_detalle': self.fk_hoja_control_detalle,
            'fk_filtracion': self.fk_filtracion,
            'cantidad': self.valor_filtracion,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'publish': self.publish,
            'descripcion': self.descripcion,
            'sinHojaControlDetalle': False
        }