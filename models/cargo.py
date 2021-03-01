class Cargo:
    def __init__(self,__id, fk_tipo_cargo,nombres, apellidos, celular, correo, publish):
          self.__id=__id
          self.fk_tipo_cargo = fk_tipo_cargo
          self.nombres = nombres
          self.apellidos = apellidos
          self.celular = celular
          self.correo = correo
          self.publish=publish
    
    @property
    def data(self):
        return {
            'id': self.__id,
            'fk_tipo_cargo': self.fk_tipo_cargo,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'celular': self.celular,
            'correo': self.correo,
            'publish': self.publish
               }