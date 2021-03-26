class ContactosEmpresaV:
    def __init__(self, __id, fk_cliente_empresarial, fk_cargo, publish, nombres, apellidos, celular, cumple, correo,
                 fk_tipo_cargo):
        self.__id = __id
        self.fk_cliente_empresarial = fk_cliente_empresarial
        self.fk_cargo = fk_cargo
        self.publish = publish
        self.nombres = nombres
        self.apellidos = apellidos
        self.celular = celular
        self.cumple = cumple
        self.correo = correo
        self.fk_tipo_cargo = fk_tipo_cargo

    @property
    def data(self):
        if self.cumple:
            self.cumple = str(self.cumple.isoformat())

        return {
            'id': self.__id,
            'fk_cliente_empresarial': self.fk_cliente_empresarial,
            'fk_cargo': self.fk_cargo,
            'publish': self.publish,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'celular': self.celular,
            'cumple': self.cumple,
            'correo': self.correo,
            'fk_tipo_cargo': self.fk_tipo_cargo
        }
