https://overiq.com/mysql-connector-python-101/executing-queries-using-connector-python/

https://www.mysqltutorial.org/python-mysql-query/

Avoid HardCoding

https://overiq.com/mysql-connector-python-101/connecting-to-mysql-using-connector-python/

https://roytuts.com/query-parameter-in-rest-api-get-request-with-python-flask/


https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/

https://vslive.com/Blogs/News-and-Tips/2015/04/5-VS-Keyboard-Shortcuts.aspx#:~:text=Comment%20Code%20Block%20Ctrl%2BK,C%2FCtrl%2BK%2BU&text=If%20you%20select%20a%20block,U%20will%20uncomment%20the%20code.


https://holamundopy.blogspot.com/2016/02/separar-el-nombre-de-los-apellidos-en.html

https://sauldelgado.net/parametros-json-en-stored-procedures-de-mysql/


https://github.com/vfabianfarias/Datos-Geograficos-Ecuador


columns = cursor.description
ALTER TABLE cliente_ficha AUTO_INCREMENT = 1


DELETE from direccion_cliente;
DELETE from parentesco;
DELETE from cliente_natural;


ALTER TABLE cliente_natural AUTO_INCREMENT = 1;
ALTER TABLE direccion_cliente AUTO_INCREMENT = 1;
ALTER TABLE parentesco AUTO_INCREMENT = 1;




python test-columns.py > output_class.txt

python columns_class.py > output_class.txt


Instalaciones necesarias
https://gist.github.com/Klerith/607dd6bb60b5a70bc5e4d9c81ef6501e

https://github.com/Klerith/curso-VSCode

choco install postgresql11 --params '/Password:PoiZxc357' -y


https://coolors.co/b8336a-c695be-726da8-7d8cc4-a0d2db-b2b1d6-c490d1

//Esta pagina sirve para generar Datos aleatorios y llenarlos en la base de datos
https://www.mockaroo.com/




{"cliente_natural":[{"codigo": "C45784", "ruc": "0916780178", "apellido1": "Cerezo", "apellido2": "", "nombre1": "Andres", "nombre2": "", "celular": "0945785474", "correo": "", "cumple": "1991-2-17", "foto": ""}],
"parentesco": [{"tipo_parentesco": "Primo", "sexo": "", "nombre1": "Luis", "nombre2": "Alfredo", "apellido1": "Pincay", "apellido2": "", "celular": "0978474789", "correo": "", "cumple": ""}],
"direcciones": [{"fk_provincia": 2, "fk_canton": 17, "fk_parroquia": 119, "direccion_domiciliaria": "En un lugar de la mancha", "direccion_oficina": "", "telefono_convencional": ""}]}


UPDATE
  `cliente_natural`
SET
  `foto` = 'https://icons.iconarchive.com/icons/oxygen-icons.org/oxygen/128/Places-user-identity-icon.png'
WHERE
  `cliente_natural`.`id` <= 50


UPDATE
  `cliente_natural`
SET
  `foto` = 'https://icons.iconarchive.com/icons/hopstarter/sleek-xp-basic/128/Office-Girl-icon.png'
WHERE
  `cliente_natural`.`id` > 50


  https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html
