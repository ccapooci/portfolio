import mariadb
import os
import sys
"""
Getting into mariadb requires the following: /mnt/apps/public/CSC/Mysql-Shell/bin/mysql -u MDB_USER -p -h classdb2.csc.ncsu.edu                                                                                                           2 -p -h classdb2.csc.ncsu.edu

"""

def connect_to_MariaDB():
    try:
        host = os.getenv('MDB_HOST')

        if not host:
            host = 'classdb2.csc.ncsu.edu'

        # Project
        conn = mariadb.connect(
            user=os.getenv('MDB_USER'),
            password=os.getenv('MDB_PASS'),
            host=host,
            database=os.getenv('MDB_DB'),
            port=3306
        )
        # print('Connection successful!')
        return conn, conn.cursor()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
