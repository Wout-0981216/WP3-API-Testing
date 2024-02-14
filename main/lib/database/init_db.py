import sqlite3

connection = sqlite3.connect('database.db')

with open('create_database_queries.sql') as f:
  connection.executescript(f.read())

connection.close()