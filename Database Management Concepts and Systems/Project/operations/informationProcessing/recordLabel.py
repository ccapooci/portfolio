import mariadb

from operations import db
from operations.informationProcessing.helpers import validate_number_field


def create_record_label_helper(label_name: str):
    """
    Function that takes a label name and injects into creation query for record label
    :param label_name:
    :return:
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO RecordLabel (labelName) Values('{label_name}')")

        conn.commit()

        print(f"Record Label, '{label_name}', was added successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def create_record_label():
    """ Function that takes a record label name from user and creates SQL query for creating a new record label
    """
    label_name = input("Enter in label name: ")
    create_record_label_helper(label_name=label_name)


def update_record_label_helper(new_label_name: str, label_name: str):
    """
    Function that takes new_label_name and permeates patch SQL query
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"UPDATE RecordLabel set labelName = '{new_label_name}' where labelName = '{label_name}'")

        conn.commit()

        print(f"Record Label, '{label_name}', was updated successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def update_record_label():
    """ Function that takes a record label name and a new record label name and creates SQL query for
    updating an existing record label
    """
    label_name = input("Enter in label name: ")
    new_label_name = input("Enter updated label name: ")
    update_record_label_helper(new_label_name=new_label_name, label_name=label_name)


def delete_record_label_helper(label_name: str):
    """
    Take a label name and injects into deletion query
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"DELETE FROM RecordLabel WHERE labelName = '{label_name}'")

        conn.commit()

        print(f"Record Label, '{label_name}', was deleted successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def delete_record_label():
    """ Function that takes a record label name and creates SQL query for deleting an existing record label
    """
    label_name = input("Enter in label name: ")
    delete_record_label_helper(label_name=label_name)


def assign_record_label_to_song_helper(label_name: str, content_creator_id: int, song_title: str,
                                       album_title: str, edition: str):
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO Owns Values({content_creator_id}, '{label_name}', '{song_title}', "
                    f"'{album_title}', '{edition}')")

        conn.commit()

        print(f"Assignment between artists and songs was successful")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def assign_record_label_to_song():
    """ Function that takes parameters and creates SQL query for creating an association between record label and song
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)

        label_name = input("Enter in label name: ")

        song_title = input("Enter in song title: ")

        album_title = input("Enter in album title: ")

        edition = input("Enter in edition: ")

        assign_record_label_to_song_helper(label_name=label_name, song_title=song_title, album_title=album_title,
                                           edition=edition)


    except:
        print("Oops, something went wrong!")


def update_contracted_artist_helper(label_name: str, content_creator_id: int):
    """
    With the given parameters, build SQL query to create new Contracts tuple
    :param label_name: name of RecordLabel
    :param content_creator_id: id of ContentCreator
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO Contracts (creatorId, recordLabelName) Values({content_creator_id}, '{label_name}')")

        conn.commit()

        print(f"Contract between artist and record label was successful")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def update_contracted_artist():
    """ Function that takes parameters for contract relationship between content creator and record label
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)

        label_name = input("Enter in label name: ")

        update_contracted_artist_helper(label_name=label_name, content_creator_id=content_creator_id)


    except:
        print("Oops, something went wrong!")
