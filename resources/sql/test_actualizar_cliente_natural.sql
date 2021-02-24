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


CALL lc_sp_actualizar_cliente_natural('[{"id":1,"codigo":"CQ0000","ruc":"0915740350","nombre1":"Carlos","nombre2":"Alethea","apellido1":"Cerezo","apellido2":"Entwistle","correo":"aentwistle0@adobe.com","celular":"3282505047","cumple":"2006-10-30","foto":"https://icons.iconarchive.com/icons/oxygen-icons.org/oxygen/128/Places-user-identity-icon.png","publish":1}]',
                                        '[{"id":1,"fk_cliente":1,"fk_provincia":12,"fk_canton":129,"fk_parroquia":815,"direccion_domiciliaria":"1 Lakewood Gardens Alley","direccion_oficina":"3 Golf Course Plaza","telefono_convencional":"680 220 9049","publish":1}]',
                                        '[{"id":1,"fk_cliente":1,"tipo_parentesco":"Papá","sexo":"M","nombre1":"Tarrah","nombre2":"Peg","apellido1":"Birkenhead","apellido2":"Mistry","celular":"1001137344","correo":"pmistry0@dedecms.com","cumple":"1990-06-27"}]'
                                        ,@json_respuesta)

SELECT  @json_respuesta;
-- SELECT JSON_EXTRACT(@json_respuesta, '$.id_cliente'),JSON_EXTRACT(@json_respuesta, '$.id_direcciones'),JSON_EXTRACT(@json_respuesta, '$.id_parentesco');