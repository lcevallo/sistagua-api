class ContactosEmpresa:
    def __init__(self, __id, fk_cliente_empresarial, fk_cargo, created_at, updated_at, publish):
        self.__id = __id
        self.fk_cliente_empresarial = fk_cliente_empresarial
        self.fk_cargo = fk_cargo
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
            'fk_cliente_empresarial': self.fk_cliente_empresarial,
            'fk_cargo': self.fk_cargo,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'publish': self.publish
        }