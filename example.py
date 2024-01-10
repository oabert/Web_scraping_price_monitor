import sqlite3

# Establish a connection with sqlite
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Query all(*) data based on condition
# cursor.execute("SELECT * FROM price WHERE") # Query all(*) data
cursor.execute("SELECT * FROM price WHERE price='$539.80'")
result_rows = cursor.fetchall()
print(result_rows)

# Query some data
# cursor.execute("SELECT price, item  FROM price WHERE price='$539.80'")
# result_rows = cursor.fetchall()
# print(result_rows)

# Insert new rows
new_rows = [('Item #207120', '$225.00'),
            ('Item #208448', '$195.00')]

cursor.executemany("INSERT INTO price VALUES(?,?)", new_rows)
connection.commit()
connection.close()
