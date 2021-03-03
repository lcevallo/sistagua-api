class ClienteEmpresarial:
    def __init__(self,__id, codigo, ruc, nombres, direccion, telefono, correo, created_at, updated_at, publish):
        self.__id = __id
        self.codigo = codigo
        self.ruc = ruc
        self.nombres = nombres
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
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
            'id': self.__id,
            'codigo': self.codigo,
            'ruc': self.ruc,
            'nombres': self.nombres,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'correo': self.correo,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'publish': self.publish
        }
