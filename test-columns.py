import myconnutils

connection = myconnutils.getConnection()
cursor = connection.cursor()

query = "SELECT  * FROM `filtracion` LIMIT 2"

cursor.execute(query)

columns = cursor.description
columna = []

for col in columns:
    columna.append(col[0])

connection.close()

print(columna)