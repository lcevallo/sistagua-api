class Accesorio:
    def __init__(self, id, codigo, nombre, descripcion, created_at, updated_at, publish):
        self.id = id
        self.codigo=codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.created_at = created_at
        self.updated_at = updated_at
        self.publish = publish

    @property
    def data(self):
        if self.created_at:
            self.created_at = str(self.created_at.isoformat())
        if self.updated_at:
            self.updated_at = str(self.updated_at.isoformat())

        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'publish': self.publish
        }
