import mariadb

from operations import db
from operations.informationProcessing.helpers import validate_number_field, prompt_and_validate_custom, \
    prompt_and_validate_string


def create_artist_helper(content_creator_id: int, subscription_status: str, artist_type: str, country: str,
                         genre: str):
    """ Helper function that takes artist parameters and creates SQL query for creating a new artist
    Args:
        content_creator_id: the id of the creator that's associated with the album
        subscription_status: the status of subscription
        artist_type: the type of artist that one is such as band, solo artist for example
        country: the country of the artist
        genre: the artist of the genre
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO Artist Values({content_creator_id}, '{subscription_status}', '{artist_type}', "
                    f"'{country}', '{genre}' )")

        conn.commit()

        print(f"Artist {content_creator_id}, was added successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def create_artist():
    """ Function that prompts users for inputs necessary to create an artist
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        subscription_status = input("Enter subscription status (A or I): ")
        if subscription_status != "A" and subscription_status != "I":
            raise Exception("A or I was not entered in!")
        artist_type = input("Enter type of artist: ")
        country = input("Enter country of artist: ")
        genre = input("Enter genre of artist: ")

        create_artist_helper(content_creator_id=content_creator_id, subscription_status=subscription_status,
                             artist_type=artist_type, country=country, genre=genre)
    except:
        print("Oops, something went wrong!")


def update_artist_helper(field_name: str, field_value: str, content_creator_id: int):
    """ Helper function that takes a field key/value pair for updating a specific attribute on an artist
    and executes query
    Args:
        field_name:  column name of the artist schema
        field_value: the value associated with the field_name
        content_creator_id: the id of the creator that's associated with the artist
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"Update Artist SET {field_name} = {field_value} WHERE creatorId={content_creator_id}")

        conn.commit()

        print(f"Artist '{content_creator_id}', was updated successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def update_artist():
    """ Function that prompts users for inputs necessary to update an attribute of an artist
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        field_name = ""
        field_value = None
        print("\n\nList of fields:")
        print("subscription status = ss")
        print("type = t")
        print("country = c")
        print("primary genre = pg")

        prompt_field = input("Which of the user fields would you like to update? ")

        match prompt_field.lower():
            case "ss":
                def validate_subscription(given_value):
                    if given_value != "A" and given_value != "I":
                        raise Exception("A or I was not entered in!")

                field_name, field_value = prompt_and_validate_custom("status",
                                                                     "\n\nEnter subscription status (A or I): ",
                                                                     validate_subscription)
            case "t":
                field_name, field_value = prompt_and_validate_string("type")
            case "c":
                field_name, field_value = prompt_and_validate_string("country")
            case "pg":
                field_name, field_value = prompt_and_validate_string("primaryGenre")

        update_artist_helper(field_name, field_value, content_creator_id)
    except:
        print("Oops, something went wrong!")


def delete_artist_helper(content_creator_id: int):
    """ Helper function that takes the content_creator_id of an artist in order to delete the artist and executes query
    Args:
        content_creator_id: the id of the creator that's associated with the artist
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"DELETE FROM Artist WHERE creatorId={content_creator_id}")

        conn.commit()

        print(f"Artist, '{content_creator_id}', was deleted successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def delete_artist():
    """ Function that prompts user for the content_creator_id of the artist to be deleted
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        delete_artist_helper(content_creator_id=content_creator_id)
    except:
        print("Oops, something went wrong!")
