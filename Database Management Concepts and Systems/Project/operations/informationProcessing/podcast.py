import mariadb

from operations import db
from operations.informationProcessing.helpers import validate_float_field, prompt_and_validate_string, \
    prompt_and_validate_custom


def create_podcast_helper(podcast_name: str, language: str, country: str, rating: float):
    """ Helper function that takes podcast parameters and creates SQL query for creating a new podcast
    Args:
        podcast_name: name of podcast to be added
        language: language of podcast to be added
        country: country of the podcast to be added
        rating: rating of the podcast to be added
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO Podcast (podcastName, language, country, rating) "
                    f"Values('{podcast_name}', '{language}', '{country}', {rating})")

        conn.commit()

        print(f"Podcast {podcast_name}, was added successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def create_podcast():
    """ Function that prompts for inputs necessary to create a new podcast
    """
    try:
        podcast_name = input("Enter podcast name: ")
        language = input("Enter language: ")
        country = input("Enter country: ")

        rating = input("Enter in rating: ")
        validate_float_field(rating)
        rating = float(rating)

        create_podcast_helper(podcast_name=podcast_name, language=language, country=country, rating=rating)
    except:
        print("Oops, something went wrong!")


def update_podcast_helper(field_name: str, field_value: str, podcast_name: str):
    """ Helper function that takes field name/value pair and creates SQL query for updating an existing podcast
    Args:
        field_name:  column name of the podcast schema
        field_value: the value associated with the field_name
        podcast_name: the name of the podcast to be updated
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"UPDATE Podcast SET {field_name} = {field_value} "
                    f"WHERE podcastName = '{podcast_name}'")

        conn.commit()

        print(f"Podcast, '{podcast_name}', was updated successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def update_podcast():
    """ Function that prompts users for inputs necessary to update a field of an existing podcast
    """
    podcast_name = input("Enter in podcast name: ")

    field_name = ""
    field_value = None
    print("\n\nList of fields:")
    print("podcast name = pn")
    print("language = l")
    print("country = c")
    print("rating = r")

    try:
        prompt_field = input("Which of the user fields would you like to update? ")

        match prompt_field.lower():
            case "pn":
                field_name, field_value = prompt_and_validate_string("podcastName")
            case "l":
                field_name, field_value = prompt_and_validate_string("language")
            case "c":
                field_name, field_value = prompt_and_validate_string("country")
            case "r":
                field_name, field_value = prompt_and_validate_custom("rating",
                                                                     "\n\nWhat is the new value for release year?: ",
                                                                     validate_float_field)

        update_podcast_helper(field_name, field_value, podcast_name=podcast_name)
    except:
        print("Oops, something went wrong!")


def delete_podcast_helper(podcast_name: str):
    """ Helper function that takes a podcast name pair and creates SQL query for deleting an existing podcast
    Args:
        podcast_name: the name of the podcast to be deleted
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"DELETE FROM Podcast WHERE podcastName = '{podcast_name}'")

        conn.commit()

        print(f"Podcast, '{podcast_name}', was deleted successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def delete_podcast():
    """ Function that prompts user for a podcast name necessary to delete that podcast
    """
    podcast_name = input("Enter in podcast name: ")

    delete_podcast_helper(podcast_name=podcast_name)
