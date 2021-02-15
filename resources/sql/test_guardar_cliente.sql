CALL sistagua_bd.lc_sp_guardar_cliente_natural(
    '[{ "codigo": "C0001",
        "ruc": "0705114775",
        "apellido1": "Cerezo",
        "apellido2": "",
        "nombre1": "CArlos",
        "nombre2": "",
        "celular": "0994898148",
        "correo": "",
        "cumple": "1990-04-24",
        "foto": ""
    }]','[{
      "tipo_parentesco": "sdfsdf",
      "sexo": "M",
      "nombre1": "",
      "nombre2": "",
      "apellido1": "dfsdf",
      "apellido2": "",
      "celular": "fsdfsdfsdf",
      "correo": "fsdfsdfsdf",
      "cumple": ""
    },
    {
      "tipo_parentesco": "sdfsdf",
      "sexo": "M",
      "nombre1": "",
      "nombre2": "",
      "apellido1": "dfsdf",
      "apellido2": "",
      "celular": "fsdfsdfsdf",
      "correo": "fsdfsdfsdf",
      "cumple": ""
    }
    ]',
    '[
      {
      "fk_provincia": 3,
      "fk_canton": 27,
      "fk_parroquia": 175,
      "direccion_domiciliaria": "Vía Arcapamba",
      "direccion_oficina": "",
      "telefono_convencional": ""
     }
   ]',
   @json_respuesta
);
SELECT @json_respuesta;


DELETE from parentesco;
DELETE from direccion_cliente;
DELETE from cliente_natural;

ALTER TABLE cliente_natural AUTO_INCREMENT = 1;
ALTER TABLE direccion_cliente AUTO_INCREMENT = 1;
ALTER TABLE parentesco AUTO_INCREMENT = 1;