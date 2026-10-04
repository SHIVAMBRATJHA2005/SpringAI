import sqlite3

connection = sqlite3.connect("students.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    cgpa REAL,
    age INTEGER
)
""")

students = [
    (1, "Rahul", "CSE", 8.2, 21),
    (2, "Amit", "AIML", 7.8, 22),
    (3, "Priya", "CSE", 9.1, 21),
    (4, "Ankit", "ECE", 8.5, 22),
    (5, "Sneha", "AIML", 9.0, 21),
    (6, "Ravi", "CSE", 7.9, 23)
]

cursor.executemany("""
INSERT OR IGNORE INTO students
(id, name, department, cgpa, age)
VALUES (?, ?, ?, ?, ?)
""", students)

connection.commit()
connection.close()

print("Database created successfully!")
