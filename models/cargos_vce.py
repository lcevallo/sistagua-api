class CargosVCE:
    def __init__(self, id, nombres, apellidos, celular, cumple, correo, tipo,
                 fk_cliente_empresarial, fk_cargo):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.celular = celular
        self.cumple = cumple
        self.correo = correo
        self.tipo = tipo
        self.fk_cliente_empresarial = fk_cliente_empresarial
        self.fk_cargo = fk_cargo

    @property
    def data(self):

        if self.cumple:
            self.cumple = str(self.cumple.isoformat())

        return {
            'id': self.id,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'celular': self.celular,
            'cumple': self.cumple,
            'correo': self.correo,
            'tipo': self.tipo,
            'fk_cliente_empresarial': self.fk_cliente_empresarial,
            'fk_cargo': self.fk_cargo
        }
