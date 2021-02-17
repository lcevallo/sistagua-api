class Cliente_Natural:
    def __init__(self, __id, codigo, ruc, nombre1, nombre2, apellido1, apellido2, correo, celular, cumple, foto, publish):
        self.__id = __id
        self.codigo = codigo
        self.ruc = ruc
        self.nombre1 = nombre1
        self.nombre2 = nombre2
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.correo = correo
        self.celular = celular
        self.cumple = cumple
        self.foto = foto
        self.publish = publish

    @property
    def data(self):
        if self.cumple:
            self.cumple = str(self.cumple.isoformat())

        return {
            'id': self.__id,
            'codigo': self.codigo,
            'ruc': self.ruc,
            'nombre1': self.nombre1,
            'nombre2': self.nombre2,
            'apellido1': self.apellido1,
            'apellido2': self.apellido2,
            'correo': self.correo,
            'celular': self.celular,
            'cumple': self.cumple,
            'foto': self.foto,
            'publish': self.publish
        }