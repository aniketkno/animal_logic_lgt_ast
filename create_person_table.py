import sqlite3

def create_connection(db_name):
    conn = sqlite3.connect(f"{db_name}.db")
    cur = conn.cursor()
    return conn, cur



def create_persons_table(conn, cur):
    # Create database
    cur.execute(
        """CREATE TABLE IF NOT EXISTS person(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, phone_number INT)"""
    )
    conn.commit()

def insert_person_values(name, address, number, conn, cur):
    # Insert Values
    cur.execute("INSERT INTO person VALUES (?, ?, ?, ?)", (None, name, address, number))
    conn.commit()



persons = [["Mario Speedwagon", "7982 Schoolhouse Street, Hagerstown, MD 21740", "(509) 808-0424"],
           ["Petey Cruiser", "416 Glenholme Lane, East Haven, CT 06512", "(826) 824-8580"],
           ["Anna Sthesia", "40 Whitemarsh Drive, Washington, PA 15301", "(903) 778-3765"],
           ["Paul Molive", "7860 Campfire Road, Mahwah, NJ 07430", "(956) 864-8906"],
           ["Anna Mull", "9 53rd Court, Mobile, AL 36605", "(631) 956-0784"],
           ["Gail Forcewind", "9 Silver Spear St., Corpus Christi, TX 7841", "(423) 206-1061"]]

conn, cur = create_connection("person")
create_persons_table(conn, cur)
for person in persons:
    print(person)
    insert_person_values(person[0], person[1], person[2], conn, cur)