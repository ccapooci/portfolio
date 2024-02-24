# INSERT INTO PodcastEpisode Values('Blind smartphone camera test results', 'Waveform Podcast', 60, '2023-1-1', 100)
import mariadb

from operations import db
from operations.informationProcessing.helpers import validate_number_field, prompt_and_validate_string, \
    prompt_and_validate_custom, prompt_and_validate_date


def create_podcast_episode_helper(title: str, podcast_name: str, duration: int, release_date: str,
                                  advertisement_count: int):
    """ Helper function that takes podcast episode parameters and creates SQL query for creating a new podcast episode
    Args:
        title: title of podcast episode to be added
        podcast_name: name of podcast
        duration: duration of podcast episode to be added
        release_date: release date of podcast episode to be added
        advertisement_count: the number of advertisement present in podcast episode to be added
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO PodcastEpisode (title, podcastName, duration, releaseDate, advertisementCount) "
                    f"Values('{title}', '{podcast_name}', "
                    f"{duration}, '{release_date}', {advertisement_count})")

        conn.commit()

        print(f"Podcast Episode, '{title}', was added successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def create_podcast_episode():
    """ Function that prompts user for inputs necessary to create a new podcast episode
    """
    try:
        title = input("Enter episode title: ")
        podcast_name = input("Enter podcast name: ")

        duration = input("Enter in episode duration: ")
        validate_number_field(duration)
        duration = int(duration)

        release_date = input("Enter in release date (format: 2020-01-01): ")

        advertisement_count = input("Enter in advertisement count: ")
        validate_number_field(advertisement_count)
        advertisement_count = int(advertisement_count)

        create_podcast_episode_helper(title=title, podcast_name=podcast_name, duration=duration,
                                      release_date=release_date,
                                      advertisement_count=advertisement_count)
    except:
        print("Oops, something went wrong!")


def update_podcast_episode_helper(field_name: str, field_value: str, podcast_name: str, title: str):
    """ Helper function that takes podcast episode parameters and creates SQL query for updating an
     existing podcast episode
    Args:
        field_name: a column of the podcast episode schema
        field_value: the value associated with the chosen column
        title: title of podcast episode to be added
        podcast_name: name of podcast
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"UPDATE PodcastEpisode SET {field_name} = {field_value} "
                    f"WHERE podcastName = '{podcast_name}' AND title = '{title}'")

        conn.commit()

        print(f"PodcastEpisode, '{title}', was updated successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def update_podcast_episode():
    """ Function that takes an input of a key/value pair for a column to update for an existing podcast episode
    """
    try:
        title = input("Enter episode title: ")
        podcast_name = input("Enter podcast name: ")

        field_name = ""
        field_value = None
        print("\n\nList of fields:")
        print("title = t")
        print("duration = d")
        print("releaseDate = rd")
        print("advertisementCount = ac")

        prompt_field = input("Which of the user fields would you like to update? ")

        match prompt_field.lower():
            case "t":
                field_name, field_value = prompt_and_validate_string("title")
            case "d":
                field_name, field_value = prompt_and_validate_custom("duration",
                                                                     "\n\nWhat is the new value for duration?: ",
                                                                     validate_number_field)
            case "rd":
                field_name, field_value = prompt_and_validate_date("releaseDate")
            case "ac":
                field_name, field_value = prompt_and_validate_custom("advertisementCount",
                                                                     "\n\nWhat is the new value for advertisementCount?: ",
                                                                     validate_number_field)

        update_podcast_episode_helper(field_name=field_name, field_value=field_value,
                                      podcast_name=podcast_name, title=title)
    except:
        print("Oops, something went wrong!")


def delete_podcast_episode_helper(podcast_name: str, title: str):
    """ Helper function that takes the podcast name and title of episode to delete an existing podcast episode
    Args:
        title: title of podcast episode to be added
        podcast_name: name of podcast
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"DELETE FROM PodcastEpisode WHERE podcastName = '{podcast_name}' "
                    f"AND title = '{title}'")

        conn.commit()

        print(f"PodcastEpisode, '{title}', was deleted successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def delete_podcast_episode():
    """ Function that prompts user for the episode title and podcast name in order to delete an existing podcast
    episode
    """
    title = input("Enter episode title: ")
    podcast_name = input("Enter podcast name: ")

    delete_podcast_episode_helper(podcast_name=podcast_name, title=title)
