import sqlite3

def load_sql():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    with open("data-sqlite3.sql", "r") as file:
        sql_script = file.read()

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    
    print("SQL db file dumped")

if __name__ == "__main__":
    load_sql()
