class Filtracion:
    def __init__(self, id, filtracion, created_at, updated_at, publish):
        self.id = id
        self.filtracion = filtracion
        self.created_at = created_at
        self.updated_at = updated_at
        self.publish = publish

    @property
    def data(self):
        if self.updated_at:
            self.updated_at = str(self.updated_at.utcnow())
        return {
            'id': self.id,
            'filtracion': self.filtracion,
            'created_at': str(self.created_at.utcnow()),
            'updated_at': self.updated_at,
            'publish': self.publish
        }
