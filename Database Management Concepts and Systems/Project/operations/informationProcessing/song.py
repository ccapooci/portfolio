from operations import db
import mariadb
from operations.informationProcessing.helpers import validate_number_field, validate_float_field, \
    prompt_and_validate_string, prompt_and_validate_custom, prompt_and_validate_date


def create_song_helper(content_creator_id: int, album_title: str, edition: str, song_title: str, track_number: int,
                       duration: int, play_count: int, release_date: str, country: str, language: str,
                       royalty_paid_status: bool, royalty_rate: float):
    """
    Helper function that takes song parameters and executes query in order to create a new song
    :param content_creator_id: the artist associated with the song
    :param album_title: the album associated with the song
    :param edition: the edition associated with the song
    :param song_title: the title of the song
    :param track_number: the track number of the song
    :param duration: the amount of minutes of the song
    :param play_count: the number of times the song has been played
    :param release_date: the release date of the song
    :param country: the country of the song
    :param language: the language of the song
    :param royalty_paid_status: the royalty paid status of the song
    :param royalty_rate: the royalty rate of the song
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO Song (creatorId, albumName, edition, songTitle, trackNumber, duration, playCount, "
                    f"releaseDate, releaseCountry, language, royaltyPaidStatus, royaltyRate) Values({content_creator_id}, "
                    f"'{album_title}', '{edition}', '{song_title}',"
                    f"{track_number}, {duration}, {play_count}, '{release_date}', '{country}',"
                    f"'{language}', {royalty_paid_status}, {royalty_rate})")

        conn.commit()

        print(f"Song, '{song_title}', was added successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def create_song():
    """
    Function that takes in parameters from the user necessary to create a new song
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        album_title = input("Enter in album title: ")
        edition = input("Enter in edition: ")

        song_title = input("Enter in song title: ")

        track_number = input("Enter in track number: ")
        validate_number_field(track_number)
        track_number = int(track_number)

        duration = input("Enter in duration: ")
        validate_number_field(duration)
        duration = int(duration)

        play_count = input("Enter in play count: ")
        validate_number_field(play_count)
        play_count = int(play_count)

        release_date = input("Enter in release date (format: 2020-01-01): ")

        country = input("Enter in country: ")

        language = input("Enter in language: ")

        royalty_paid_status = input("Enter whether song is royalty paid status (y or n): ")

        royalty_paid_status = royalty_paid_status.lower() == "y"

        royalty_rate = input("Enter in royalty rate: ")
        validate_float_field(royalty_rate)
        royalty_rate = float(royalty_rate)

        create_song_helper(content_creator_id, album_title, edition, song_title, track_number, duration, play_count,
                           release_date, country, language, royalty_paid_status, royalty_rate)
    except:
        print("Oops, something went wrong!")


def update_song_helper(field_name: str, field_value: str, content_creator_id: int, album_title: str,
                       edition: str, song_title: str):
    """
    Helepr function that takes in field key/value pair and key attribtues of the song in order to update
    via SQL creation/execution
    :param field_name: the chosen column on the song schema
    :param field_value: the value associated with field_name
    :param content_creator_id: the artist associated with the song
    :param album_title: the album title associated with the song
    :param edition: the edition of the album associated with the song
    :param song_title: the title of the song
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"UPDATE Song "
                    f"SET {field_name} = {field_value} "
                    f"WHERE creatorId = {content_creator_id} AND albumName = '{album_title}' AND "
                    f"edition = '{edition}' AND songTitle = '{song_title}'")

        conn.commit()

        print(f"Song, '{song_title}', was updated successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def update_song():
    """
    Function that prompts users for inputs necessary to update an existing song
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        album_title = input("Enter in album title: ")

        edition = input("Enter in edition: ")

        song_title = input("Enter in song title: ")

        field_name = ""
        field_value = None
        print("\n\nList of fields:")
        print("song title = st")
        print("track number = tn")
        print("duration = d")
        print("play count = pc")
        print("release date = rd")
        print("release country = rc")
        print("language = l")
        print("royalty paid status = rps")
        print("royalty rate = rr")
        prompt_field = input("Which of the song fields would you like to update? ")

        match prompt_field.lower():
            case "st":
                field_name, field_value = prompt_and_validate_string("songTitle")
            case "tn":
                field_name, field_value = prompt_and_validate_custom("trackNumber",
                                                                     "\n\nWhat is the new value for track number?: ",
                                                                     validate_number_field)
            case "d":
                field_name, field_value = prompt_and_validate_custom("duration",
                                                                     "\n\nWhat is the new value for duration?: ",
                                                                     validate_number_field)
            case "pc":
                field_name, field_value = prompt_and_validate_custom("playCount",
                                                                     "\n\nWhat is the new value for play count?: ",
                                                                     validate_number_field)
            case "rd":
                field_name, field_value = prompt_and_validate_date("releaseDate")
            case "rc":
                field_name, field_value = prompt_and_validate_string("releaseCountry")
            case "l":
                field_name, field_value = prompt_and_validate_string("language")
            case "rps":
                def royalty_status_validation(given_value):
                    if given_value.lower() != "y" and given_value.lower() != "n":
                        raise Exception("Invalid value!")

                field_name, field_value = prompt_and_validate_custom("royaltyPaidStatus",
                                                                     "\n\nEnter whether song is royalty paid status (y or "
                                                                     "n): ",
                                                                     royalty_status_validation)
                field_value = field_value.lower() == "y"
            case "rr":
                field_name, field_value = prompt_and_validate_custom("royaltyRate", "\n\nEnter in royalty rate: ",
                                                                     validate_float_field)

        update_song_helper(field_name, field_value, content_creator_id, album_title, edition, song_title)
    except:
        print("Oops, something went wrong!")


def delete_song_helper(content_creator_id: int, album_title: str, edition: str, song_title: str):
    """
    Helper function that uses parameters to build SQL query to execute in order to delete song
    :param content_creator_id: artist associated with song
    :param album_title: album title of song
    :param edition: edition of album of song
    :param song_title: title of song
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"DELETE FROM Song WHERE creatorId = {content_creator_id} AND albumName = '{album_title}' "
                    f"AND edition = '{edition}' "
                    f"AND songTitle = '{song_title}'")

        conn.commit()

        print(f"Song, '{song_title}', was deleted successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def delete_song():
    """
    Function that prompts user for inputs that are necesary to delete song
    """
    try:
        content_creator_id = input("Enter in content creator id: ")
        validate_number_field(content_creator_id)
        content_creator_id = int(content_creator_id)

        album_title = input("Enter in album title: ")

        edition = input("Enter in edition: ")

        song_title = input("Enter in song title: ")

        delete_song_helper(content_creator_id, album_title, edition, song_title)

    except:
        print("Oops, something went wrong!")


def enter_collaboration_info_helper(content_creator_id_one: int, content_creator_id_two: int, song_title: str,
                                    album_title: str, edition: str):
    """
    Helper function that takes parameters and builds SQL necessary to add collaboration tuple between artists and song
    :param content_creator_id_one: artist collaborator one
    :param content_creator_id_two: artist collaborator two
    :param song_title: song of collaboration
    :param album_title: album associated
    :param edition: edition of album associated
    """
    print("Processing your request....")

    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(f"INSERT INTO CollaboratesOn Values({content_creator_id_one}, {content_creator_id_two},"
                    f"'{song_title}', '{album_title}', '{edition}')")

        conn.commit()

        print(f"CollaboratesOn between {content_creator_id_one} and {content_creator_id_two}, was added successfully")
        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(e)
        cur.execute('ROLLBACK;')
        cur.close()
        conn.close()


def assign_collaboration_between_artists_and_song():
    """
    Function that prompts user for inputs necessary to assign collaboration between artists and songs
    """
    try:
        content_creator_id_one = input("Enter in content creator one id: ")
        validate_number_field(content_creator_id_one)
        content_creator_id_one = int(content_creator_id_one)

        content_creator_id_two = input("Enter in content creator two id: ")
        validate_number_field(content_creator_id_two)
        content_creator_id_two = int(content_creator_id_two)

        song_title = input("Enter in song title: ")

        album_title = input("Enter in album title: ")

        edition = input("Enter in edition: ")

        enter_collaboration_info_helper(content_creator_id_one, content_creator_id_two, song_title, album_title,
                                        edition)
    except:
        print("Ooops, something went wrong!")
