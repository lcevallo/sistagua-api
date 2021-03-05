import sys
sys.path.append("..")
import myconnutils

connection = myconnutils.getConnection()
cursor = connection.cursor()

query = "SELECT * FROM `oficinas_empresa` LIMIT 1"

cursor.execute(query)

str1 = " "

columns = cursor.description
#1 init
columna = []
#2 self
columna_self = []

#3 @property
columan_json = []

#4 instanciar con el new Cliente_Natural ()
columan_row = []


columna_json_arrayagg = []


columna_postman = []


for col in columns:
    columna.append(col[0] + ',')
    columna_json_arrayagg.append("'"+col[0] + "',"+col[0] +",")
    
    columna_self.append("self." + str(col[0]) + "=" + str(col[0]) + '\n')
    columan_json.append("'" + col[0] + "': self." + str(col[0]) + ',\n')
    
    columna_postman.append('"'+col[0] + '" : "' +col[0] +'"')
    columan_row.append("row['"+col[0]+ "'],\n")

print(str1.join(columna))
print("SELECT JSON_ARRAYAGG(JSON_OBJECT("+str1.join(columna_json_arrayagg)+")) from ")
print(str1.join(columna_self))
print(str1.join(columan_json))
print ('Para el postman')
print(columna_postman)

print ('-------*----------')
print(str1.join(columan_row))

# python utils/columns_class.py > output_class.txt