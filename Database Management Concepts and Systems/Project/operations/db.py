"""Provide a singleton DB connection pool instance.

    Typical usage example:

        import db
        conn, cur = db.Database().get_connection()


"""
import mariadb
import os
import pandas as pd
from tabulate import tabulate
import sys
import datetime

_DEMO_DB = 'cvcapooc'

if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore')


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Database(object):
    def __init__(self):

        host = os.getenv('MDB_HOST')

        if not host:
            host = 'classdb2.csc.ncsu.edu'

        db = os.getenv('MDB_DB')
        demo_day_flag = os.getenv('MDB_DEMO_DAY')

        if db == _DEMO_DB and demo_day_flag != 'true':
            raise ValueError("Set 'MDB_DEMO_DAY' to 'true' to run against Corey's DB...")

        try:
            self._pool = mariadb.ConnectionPool(
                host=host,
                port=3306,
                user=os.getenv('MDB_USER'),
                password=os.getenv('MDB_PASS'),
                database=db,
                pool_name="wolfmedia-app",
                pool_size=20)

        except mariadb.PoolError as e:
            print(f"Error opening connection from pool: {e}")

    def connect_to_MariaDB(self):
        conn = self._pool.get_connection()
        return conn, conn.cursor()


def query_db():
    sql = input("Please enter SQL statement: ")

    conn, cur = Database().connect_to_MariaDB()

    try:
        print(tabulate(pd.read_sql(sql, conn), headers='keys', tablefmt='psql'))

        conn.close()

    except mariadb.Error as e:
        print(f'Error with query: {e}')
        conn.close()


def bulk_add_users():
    """
    Function to generate a specified number of new users for the system in case we need more subscribers/listeners/etc.
    :return: nothing, modifies db and prints confirmation
    """
    # Get number of records
    n_users = input('How many new users would you like to add to the service? ')

    # Get connection
    conn, cur = Database().connect_to_MariaDB()

    # Get largest UID
    uid_sql = ('SELECT * FROM User;')
    result = pd.read_sql(uid_sql, conn)
    max_id = result['UID'].max()

    # Check max_id value
    if max_id < 10000:
        base_max = 10000

    else:
        base_max = max_id

    # Generate insert tuples
    i = 1
    users = []
    while i <= int(n_users):
        uid = base_max + i
        email = f'user{int(uid)}@user{int(uid)}.dev'
        firstname = 'user'
        lastname = f'{int(uid)}'
        new_user_record = (uid, email, firstname, lastname, 10, 'A', None, datetime.datetime.today())
        users.append(new_user_record)

        i += 1

    # Build sql query
    sql = (f'INSERT INTO User (UID, email, firstName, lastName, subscriptionFee, statusOfSubscription, phone, '
           f'registrationDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)')

    # Attempt addition
    try:
        cur.execute('START TRANSACTION;')
        cur.executemany(sql, users)
        cur.execute('COMMIT;')

        print(f'Successfully added {n_users} new users to the system!')
        conn.close()

    except mariadb.Error as e:
        print(f'Error inserting new users: {e}')
        conn.close()


if __name__ == '__main__':
    # query_db()
    bulk_add_users()