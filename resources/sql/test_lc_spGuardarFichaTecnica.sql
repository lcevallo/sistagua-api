CALL sistagua_bd.lc_spGuardarFichaTecnica(0,'[ { 
 "factura": "#R456JUR", 
 "fecha_mantenimiento": "2016-02-04", 
 "recibo": "Juan Garces", 
 "ficha_tecnica": "FT-245784", 
 "descripcion": "Se ha cambiado la valvula TE45 para poder usar una nueva con mayor capacidad", 
 "persona_recepta": "Juan Garces", 
 "firma_url": "http://ikki.png", 
 "cedula_receptor": "0915748795", 
 "persona_dio_mantenimiento": "Rafael Valdez",
 "cedula_dio_mantenimiento": "0915748789"
 },
 {
 
 "factura": "#R456J787", 
 "fecha_mantenimiento": "2016-03-04", 
 "recibo": "Juan Piguave", 
 "ficha_tecnica": "FT-784", 
 "descripcion": "Se ha cambiado el oxigeno", 
 "persona_recepta": "Juan Cevallos", 
 "firma_url": "http://ikki2.png", 
 "cedula_receptor": "0915748777", 
 "persona_dio_mantenimiento": "Rafael Valdez", 
 "cedula_dio_mantenimiento": "0915747895"
 },
 {
 
 "factura": "#FERST56", 
 "fecha_mantenimiento": "2017-05-04", 
 "recibo": "Juan Garces II", 
 "ficha_tecnica": "FT-7847458", 
 "descripcion": "Ahora se daño esta huevada", 
 "persona_recepta": "Gabriel Cevallos", 
 "firma_url": "http://bulbaousr.png", 
 "cedula_receptor": "0915748795", 
 "persona_dio_mantenimiento": "Rafael Valdez", 
 "cedula_dio_mantenimiento": "0915747877"
 }]',
@json_respuesta);
SELECT @json_respuesta;