import sqlite3


def create_persons_table(conn, cur):
    # Create database
    cur.execute(
        """CREATE TABLE IF NOT EXISTS person(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, phone_number INT)"""
    )
    conn.commit()


def delete_persons(person_ids, conn, cur):
    # Insert Values
    cur.execute("DELETE FROM person WHERE id IN ({0})".format(",".join(person_ids)))
    conn.commit()


def insert_person_values(name, address, number, conn, cur):
    # Insert Values
    cur.execute("INSERT INTO person VALUES (?, ?, ?, ?)", (None, name, address, number))
    conn.commit()


def get_all_person_data(cur):
    # Read Values
    cur.execute("SELECT * FROM person")
    return cur.fetchall()


def get_person_by_ids(person_ids, cur):
    if person_ids:
        cur.execute("SELECT * FROM person WHERE id in ({0})".format(",".join([str(id) for id in person_ids])))
    else:
        cur.execute("SELECT * FROM person")
    return cur.fetchall()
