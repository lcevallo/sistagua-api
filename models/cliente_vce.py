class ClienteVCE:
    def __init__(self, id, codigo, ruc, nombres, direccion, telefono, correo, publish):
        self.id = id
        self.codigo = codigo
        self.ruc = ruc
        self.nombres = nombres
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.publish = publish

    @property
    def data(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'ruc': self.ruc,
            'nombres': self.nombres,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'correo': self.correo,
            'publish': self.publish
        }
