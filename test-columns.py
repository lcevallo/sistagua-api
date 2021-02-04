import myconnutils

connection = myconnutils.getConnection()
cursor = connection.cursor()

query = "SELECT * FROM `ficha_tecnica` LIMIT 2"

cursor.execute(query)

columns = cursor.description
#1 init
columna = []
#2 self
columna_self = []
#3 @property
columan_json = []

#esto es para los querys selects demas
columan_row = []

#Para postman
columna_postman = []

#esto es para valor
columna_valor = []

#esto es para las variables Stored prodecure
columns_sp = []

str1 = " " 

for col in columns:
    columna.append(col[0]+',')
    columna_self.append("self."+ str(col[0])+"="+str(col[0])+ '\n')
    columan_json.append("'"+col[0]+ "': self."+ str(col[0])+ ',\n')
    columan_row.append("row['"+col[0]+ "'],\n")
    columna_valor.append("valor['"+col[0]+ "'],\n")
    columna_postman.append('"'+str(col[0])+'": '+'"'+str(col[0])+'"'+ ", \n")
    #columns_sp.append("DECLARE v"+ str(col[0]).capitalize()+',\n')
    #columns_sp.append("SET v"+ str(col[0]).capitalize()+"=  JSON_UNQUOTE(JSON_EXTRACT(pParametroJson, CONCAT('$[', vIndex, ']."+str(col[0])+"')));\n")
    columns_sp.append("v"+ str(col[0]).capitalize()+',')

connection.close()

# print(columna)
print(str1.join(columna_postman))