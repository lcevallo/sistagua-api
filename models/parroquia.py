class Parroquia:
    def __init__(self, _id, parroquia, id_canton):
        self._id = _id
        self.parroquia = parroquia
        self.id_canton = id_canton

    @property
    def data(self):
        return {
            'id': self._id,
            'parroquia': self.parroquia,
            'id_canton': self.id_canton
        }
