import sqlite3

# Create database in memory
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        course TEXT,
        score INTEGER
    )
""")

# Insert data
cursor.executemany("INSERT INTO students VALUES (?,?,?,?)", [
    (1, "Ahmad", "AI Basics", 85),
    (2, "Siti", "Python", 90),
    (3, "Raju", "LangChain", 78),
    (4, "Peter", "Math", 50),
])

conn.commit()

# Query 1 — all students
print("All students:")
cursor.execute("SELECT * FROM students")
print(cursor.fetchall())

# Query 2 — score above 80
print("\nScore above 80:")
cursor.execute("SELECT name, score FROM students WHERE score > 80")
print(cursor.fetchall())

# Query 3 — average score
print("\nAverage score:")
cursor.execute("SELECT AVG(score) FROM students")
print(cursor.fetchone())

print("\nBelow 80 score:")
cursor.execute("SELECT name, score FROM students WHERE score < 80")
print(cursor.fetchall())