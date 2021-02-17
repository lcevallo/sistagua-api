import sys
sys.path.append("..")
import myconnutils

connection = myconnutils.getConnection()
cursor = connection.cursor()

query = "SELECT * FROM `cliente_natural` LIMIT 1"

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


for col in columns:
    columna.append(col[0] + ',')
    columna_self.append("self." + str(col[0]) + "=" + str(col[0]) + '\n')
    columan_json.append("'" + col[0] + "': self." + str(col[0]) + ',\n')
    columan_row.append("row['"+col[0]+ "'],\n")

print(str1.join(columna))
print(str1.join(columna_self))
print(str1.join(columan_json))
print(str1.join(columan_row))

# python utils/columns_class.py > output_class.txt