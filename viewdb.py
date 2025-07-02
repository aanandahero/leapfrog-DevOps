import sqlite3

conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Show all users
print("\nUsers:")
for row in cursor.execute("SELECT * FROM user;"):
    print(row)

# Show all jobs
print("\nJobs:")
for row in cursor.execute("SELECT * FROM job;"):
    print(row)

conn.close()
