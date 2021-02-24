class Filtracion:
    def __init__(self, id, nombre,descripcion, created_at, updated_at, publish):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
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
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'publish': self.publish
        }
