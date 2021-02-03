import myconnutils

connection = myconnutils.getConnection()
cursor = connection.cursor()

query = "SELECT  * FROM `accesorios` LIMIT 2"

cursor.execute(query)

columns = cursor.description
columna = []
columna_self = []
columan_json = []
columan_row = []
str1 = " " 

for col in columns:
    columna.append(col[0])
    columna_self.append("self."+ str(col[0])+"="+str(col[0]))
    columan_json.append("'"+col[0]+ "': self."+ str(col[0])+ ',\n')
    columan_row.append("row['"+col[0]+ "'],\n")

connection.close()

# print(columna)
print(str1.join(columan_row))