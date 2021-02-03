class Cliente:
    def __init__(self, __id, correo, nombre, apellidos, cedula, telefono, created_at,updated_at,publish):
        self.__id = __id
        self.correo = correo
        self.nombre = nombre
        self.apellidos = apellidos
        self.cedula = cedula
        self.telefono = telefono
        self.created_at = created_at
        self.updated_at = updated_at
        self.publish = publish

    @property
    def data(self):
        if self.created_at:
            self.created_at = str(self.created_at.utcnow())
        if self.updated_at:
            self.updated_at = str(self.updated_at.utcnow())

        return {
            'id': self.__id,
            'correo': self.correo,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'cedula': self.cedula,
            'telefono': self.telefono,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'publish': self.publish
        }
