import sqlite3


def search_in_database(search_value):
    database_path = "user.db"

    table = "verbs_table"

    column = "infinitive"

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table} WHERE {column} = ?"

    cursor.execute(query, (search_value,))

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return None

    return rows
