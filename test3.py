import sqlite3

connection = sqlite3.connect('C:\\Users\\rudi\\Desktop\\Scrape\\odd_scrap.db')
cursor = connection.cursor()

cursor.execute("""
DELETE FROM odd_test
WHERE odds > 0
""")

rows = cursor.fetchall()
print(rows)

connection.commit()
connection.close()

