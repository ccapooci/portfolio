import mariadb

from operations import db
from operations.informationProcessing.helpers import validate_number_field, prompt_and_validate_string, \
    prompt_and_validate_custom, validate_phone_field


def create_podcast_host_helper(content_creator_id: int, email: str, phone_number: str, city: str):
    """ Helper function that takes podcast host parameters and creates SQL query for creating a new podcast host
    Args:
        content_creator_id: the id of the associated podcast host
        email: the email of the podcast host
        phone_number: the phone number of the podcast host
        city: the city of the podcast host
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO PodcastHost Values({content_creator_id}, '{email}', '{phone_number}', '{city}')")

        conn.commit()

        print(f"PodcastHost {content_creator_id}, was added successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def create_podcast_host():
    """ Function that prompts users for inputs necessary to create a new podcast host
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        email = input("Enter in email: ")

        phone_number = input("Enter digit phone number up to 16 digits: ")
        if len(phone_number) > 16:
            raise Exception("This phone number is too long")

        city = input("Enter city: ")

        create_podcast_host_helper(content_creator_id=content_creator_id, email=email, phone_number=phone_number,
                                   city=city)
    except:
        print("Oops, something went wrong!")


def update_podcast_host_helper(field_name: str, field_value: str, content_creator_id: int):
    """ Helper function that takes a column key/value pair and creates SQL query for updating an existing podcast host
    Args:
        content_creator_id: the id of the associated podcast host
        field_name: a column of the podcast host schema
        field_value: the value associated with the field_name
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"UPDATE PodcastHost SET {field_name} = {field_value} "
                    f"WHERE creatorId = {content_creator_id}")

        conn.commit()

        print(f"PodcastHost, '{content_creator_id}', was updated successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def update_podcast_host():
    """ Function that prompts user for inputs necessary to update an existing podcast host
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        field_name = ""
        field_value = None
        print("\n\nList of fields:")
        print("email = e")
        print("phone = p")
        print("city = c")

        prompt_field = input("Which of the user fields would you like to update? ")

        match prompt_field.lower():
            case "e":
                field_name, field_value = prompt_and_validate_string("email")
            case "p":
                field_name, field_value = prompt_and_validate_custom("phone",
                                                                     "\n\nEnter digit phone number up to 16 digits: ",
                                                                     validate_phone_field)
            case "c":
                field_name, field_value = prompt_and_validate_string("city")

        update_podcast_host_helper(field_name=field_name, field_value=field_value,
                                   content_creator_id=content_creator_id)
    except:
        print("Oops, something went wrong!")


def delete_podcast_host_helper(content_creator_id: int):
    """ Helper function that takes content_creator_id and creates SQL query for deleting an existing podcast host
    Args:
        content_creator_id: the id of the associated podcast host
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"DELETE FROM PodcastHost WHERE creatorId={content_creator_id}")

        conn.commit()

        print(f"PodcastHost, '{content_creator_id}', was deleted successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def delete_podcast_host():
    """ Function that prompts user for content_creator_id necessary to delete an existing podcast host
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        delete_podcast_host_helper(content_creator_id=content_creator_id)
    except:
        print("Oops, something went wrong!")
