import sqlite3

conn = sqlite3.connect("AnimalKingdom.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Animals (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    "Назва звіра" TEXT NOT NULL,
    "Тип звіра" TEXT NOT NULL
)
""")

animals = [
    ("Лев", "Ссавець"),
    ("Крокодил", "Плазун"),
    ("Орел", "Птах"),
    ("Морська черепаха", "Плазун"),
    ("Мавпа", "Ссавець"),
]

cursor.executemany(
    'INSERT INTO Animals ("Назва звіра", "Тип звіра") VALUES (?, ?)',
    animals,
)

cursor.execute(
    'UPDATE Animals SET "Назва звіра" = ? WHERE "Назва звіра" = ?',
    ("Сокіл", "Орел"),
)

print("Ссавці:")
for row in cursor.execute('SELECT * FROM Animals WHERE "Тип звіра" = ?', ("Ссавець",)):
    print(row)

print("\nУсі тварини:")
for row in cursor.execute("SELECT * FROM Animals"):
    print(row)

conn.commit()
conn.close()
