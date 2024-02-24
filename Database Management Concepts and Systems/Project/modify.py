from operations import db
import mariadb

conn, cur = db.Database().connect_to_MariaDB()

try:

    cur.execute("ALTER TABLE Song ADD CONSTRAINT FOREIGN KEY (albumName) REFERENCES Album(albumName);")
    conn.commit()
    print('Update successful!')

    cur.close()
    conn.close()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    conn.close()
