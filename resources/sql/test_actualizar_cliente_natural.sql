CALL sistagua_bd.`lc_sp_actualizar_cliente_natural`(
    '[{ 
        "id": "5",
        "codigo": "C0005",
        "ruc": "0705114775",
        "apellido1": "Lasso",
        "apellido2": "",
        "nombre1": "Guillermo",
        "nombre2": "",
        "celular": "0994898148",
        "correo": "",
        "cumple": "1965-04-24",
        "foto": ""
    }]','[{
      "id": "5",
      "fk_cliente": "5",
      "tipo_parentesco": "Esposa",
      "sexo": "F",
      "nombre1": "QuienSabe",
      "nombre2": "",
      "apellido1": "Doe",
      "apellido2": "",
      "celular": "0978457459",
      "correo": "fsdfsdfsdf",
      "cumple": ""
    },
    {
      "fk_cliente": "5",  
      "tipo_parentesco": "Sobrino",
      "sexo": "M",
      "nombre1": "John",
      "nombre2": "",
      "apellido1": "Doe",
      "apellido2": "",
      "celular": "0979457459",
      "correo": "fsdfsdfsdf",
      "cumple": ""
    }
    ]',
    '[
      {
       "id": "5",
      "fk_cliente": "5",    
      "fk_provincia": 3,
      "fk_canton": 27,
      "fk_parroquia": 175,
      "direccion_domiciliaria": "Vía Russa Mada",
      "direccion_oficina": "",
      "telefono_convencional": ""
     }
   ]',
   @json_respuesta
);
SELECT  @json_respuesta;
-- SELECT JSON_EXTRACT(@json_respuesta, '$.id_cliente'),JSON_EXTRACT(@json_respuesta, '$.id_direcciones'),JSON_EXTRACT(@json_respuesta, '$.id_parentesco');