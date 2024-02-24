import mariadb

from operations import db
from operations.informationProcessing.helpers import validate_number_field, prompt_and_validate_string, \
    prompt_and_validate_custom


def create_album_helper(content_creator_id: int, album_title: str, edition: str, release_year: int):
    """ Helper function that takes album parameters and creates SQL query for creating a new album
    Args:
        content_creator_id: the id of the creator that's associated with the album
        album_title: the title of the album that's being added
        edition: the edition of the album that's being added
        release_year: the year that the created album released
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO Album (creatorId, albumName, edition, releaseYear) Values({content_creator_id}, "
                    f"'{album_title}', '{edition}', {release_year})")

        conn.commit()

        print(f"Album, '{album_title}', was added successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def create_album():
    """ Function that prompts the user for inputs that are necessary
    to create a new album
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        album_title = input("Enter in album title: ")
        edition = input("Enter in edition: ")

        release_year = input("Enter in release year: ")
        validate_number_field(release_year)
        release_year = int(release_year)

        create_album_helper(content_creator_id=content_creator_id, album_title=album_title, edition=edition,
                            release_year=release_year)
    except:
        print("Oops, something went wrong!")


def update_album_helper(field_name: str, field_value: str, content_creator_id: int, album_title: str, edition: str):
    """ Helper function that takes a field key/value pair for updating a specific attribute on an album
    Args:
        field_name:  column name of the album schema
        field_value: the value associated with the field_name
        content_creator_id: the id of the creator that's associated with the album
        album_title: the title of the album that's being updated
        edition: the edition of the album that's being updated
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"UPDATE Album SET {field_name} = {field_value} "
                    f"WHERE creatorId = {content_creator_id} AND albumName='{album_title}' AND edition = '{edition}'")

        conn.commit()

        print(f"Album, '{album_title}', was updated successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def update_album():
    """ Function that prompts the user for inputs that are necessary
    to update an existing album
    """
    content_creator_id = input("Enter in content creator id: ")
    validate_number_field(content_creator_id)
    content_creator_id = int(content_creator_id)

    album_title = input("Enter in album title: ")
    edition = input("Enter in edition: ")

    field_name = ""
    field_value = None
    print("\n\nList of fields:")
    print("album title = at")
    print("edition = e")
    print("release year = ry")

    prompt_field = input("Which of the user fields would you like to update? ")

    match prompt_field.lower():
        case "at":
            field_name, field_value = prompt_and_validate_string("albumName")
        case "e":
            field_name, field_value = prompt_and_validate_string("edition")
        case "ry":
            field_name, field_value = prompt_and_validate_custom("releaseYear",
                                                                 "\n\nWhat is the new value for release year?: ",
                                                                 validate_number_field)

    update_album_helper(field_name, field_value, content_creator_id, album_title, edition)


def delete_album_helper(content_creator_id: int, album_title: str, edition: str):
    """ Helper function that takes these parameters to delete the given album
    Args:
        content_creator_id: the id of the creator that's associated with the album
        album_title: the title of the album that's being deleted
        edition: the edition of the album that's being deleted
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"DELETE FROM Album WHERE creatorId = {content_creator_id} AND albumName = '{album_title}' "
                    f"AND edition = '{edition}'")

        conn.commit()

        print(f"Album, '{album_title}', was deleted successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def delete_album():
    """ Function that queries for key attributes of an album that's to be deleted
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        album_title = input("Enter in album title: ")
        edition = input("Enter in edition: ")

        delete_album_helper(content_creator_id=content_creator_id, album_title=album_title, edition=edition)
    except:
        print("Oops, something went wrong!")
