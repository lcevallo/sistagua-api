class Canton:
    def __init__(self, _id, canton, id_provincia):
        self._id = _id
        self.canton = canton
        self.id_provincia = id_provincia

    @property
    def data(self):
        return {
            'id': self._id,
            'canton': self.canton,
            'id_provincia': self.id_provincia
        }
