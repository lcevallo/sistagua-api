class VistaInfoClienteEmpresarial:
    def __init__(self,id, codigo, ruc, nombre_empresa, direccion, telefono, correo_empresa, nombres, apellidos, tipo, celular, cumple, correo_cargo, provincia, canton, parroquia, sector, direccion_cargo, telefono_convencional, publish):
        self.id=id
        self.codigo=codigo
        self.ruc=ruc
        self.nombre_empresa=nombre_empresa
        self.direccion=direccion
        self.telefono=telefono
        self.correo_empresa=correo_empresa
        self.nombres=nombres
        self.apellidos=apellidos
        self.tipo=tipo
        self.celular=celular
        self.cumple=cumple
        self.correo_cargo=correo_cargo
        self.provincia=provincia
        self.canton=canton
        self.parroquia=parroquia
        self.sector=sector
        self.direccion_cargo=direccion_cargo
        self.telefono_convencional=telefono_convencional
        self.publish=publish
    
    
    @property
    def data(self):
        if self.cumple:
            self.cumple = str(self.cumple.isoformat())
        return {
            'id': self.id,
            'codigo': self.codigo,
            'ruc': self.ruc,
            'nombre_empresa': self.nombre_empresa,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'correo_empresa': self.correo_empresa,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'tipo': self.tipo,
            'celular': self.celular,
            'cumple': self.cumple,
            'correo_cargo': self.correo_cargo,
            'provincia': self.provincia,
            'canton': self.canton,
            'parroquia': self.parroquia,
            'sector': self.sector,
            'direccion_cargo': self.direccion_cargo,
            'telefono_convencional': self.telefono_convencional,
            'publish': self.publish
        }