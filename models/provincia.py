class Provincia:
    def __init__(self, _id, provincia):
        self._id = _id
        self.provincia = provincia

    @property
    def data(self):
        return {
            'id': self._id,
            'provincia': self.provincia
        }
