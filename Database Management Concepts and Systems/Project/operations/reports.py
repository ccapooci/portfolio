"""Module for report operations and associated API functions.
"""
from operations import db
import mariadb
from tabulate import tabulate

def get_timestamps(month, year):
    """ Get the start and stop timestamps for an entire month in the format of
    YYYY-MM-DD HH:MM:SS.

    The month and year attributes are expected to be populated as integers.

    Args: 
        month: The month to generate two timestamps for. The timestamps being
        the beginning of the month and the beginning of the next month.
        year: The year of the month.

    Returns: 
        Two strings that represent timestamps in the format of YYYY-MM-DD HH:MM:SS.
    """
    start_timestamp = "" + str(year) + "-" + str(month) + "-01 00:00:00"

    if(month == 12):
        month = 1
        year = year + 1
    else:
        month = month + 1 
            
    
    stop_timestamp = "" + str(year) + "-" + str(month) + "-01 00:00:00"

    return start_timestamp, stop_timestamp

def get_dates(month, year):
    """ Get the start and stop dates for an entire month in the format of
    YYYY-MM-DD.

    The month and year attributes are expected to be populated as integers.

    Args: 
        month: The month to generate two dates for. The timestamps being
        the beginning of the month and the beginning of the next month.
        year: The year of the month.

    Returns: 
        Two strings that represent start and stop timestamps in the format of YYYY-MM-DD.
    """
    start_date = "" + str(year) + "-" + str(month) + "-01"

    if(month == 12):
        month = 1
        year = year + 1
    else:
        month = month + 1 
            
    
    stop_date = "" + str(year) + "-" + str(month) + "-01"

    return start_date, stop_date

def get_dates_from_year(year):
    """ Get the start and stop dates for an entire year in the format of
    YYYY-MM-DD.

    The year attribute is expected to be populated as an integer.

    Args: 
        year: The year to cover with timestamps.

    Returns: 
        Two strings that represent start and stop timestamps in the format of YYYY-MM-DD.
        The first timestamp is the first day of the given year. The second timestamp is the
        first day of the next year.
    """

    start_date = "" + str(year) + "-01-01"

    year = year + 1
               
    stop_date = "" + str(year) + "-01-01"

    return start_date, stop_date

def get_month():
    """ Retrieve the month from the user.
        
    Returns: 
        The month as an int 1-12.
    """
    return int(input("What month? (1-12) "))
    
def get_year():
    """ Retrieve the year from the user.
    
    Returns:
        The year as an int.
    """
    return int(input("What year? "))

def get_creator_id():
    """ Retrieve the creator ID from the user.
    
    Returns:
        The creator ID as an int.
    """
    return int(input("What is the creator ID? "))

def get_album_name():
    """ Retrieve the album name from the user.
    
    Returns:
        The album name as a string.
    """
    return input("What is the album name? ")

def get_album_edition():
    """ Retrieve the album edition from the user.
    
    Returns:
        The album edition as a string.
    """
    return input("What is the edition? ")

def get_song_title():
    """ Retrieve the song title from the user.
    
    Returns:
        The song title as a string.
    """
    return input("What is the song title? ")

def get_start_date():
    """ Retrieve the start date from the user.
    
    Returns:
        The start date in the format YYYY-MM-DD.
    """
    return input("What is the start date? As YYYY-MM-DD ")

def get_stop_date():
    """ Retrieve the stop date from the user.
    
    Returns:
        The stop date in the format YYYY-MM-DD.
    """
    return input("What is the stop date? As YYYY-MM-DD. This date will not be included in the calculation. ")

def get_record_label():
    """ Retrieve the record label from the user.
    
    Returns:
        The record label as a string.
    """
    return input("What is the record label? ")

def get_podcast_name():
    """ Retrieve the podcast name from the user.
    
    Returns:
        The podcast name as a string.
    """
    return input("What is the podcast name? ")

def calculate_monthly_play_count_song():
    """ Request information from the user and complete the calculation for the monthly play count.
    """
    try:
        song_title = get_song_title()
        creator_id = get_creator_id()
        album_name = get_album_name()
        edition = get_album_edition()
        month = get_month()
        year = get_year()
        sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year, print_table=True):
    """ Execute a SQL query to get the monthly play count for the song provided in the arguments.
    
    Args:
        song_title: The song title to query.
        creator_id: The creator of the song.
        album_name: The album that the song is in.
        edition   : The edition of the album.
        month     : The month to get the count for
        year      : The year that the month is in.

    """
    conn, cur = db.Database().connect_to_MariaDB()

    try:

        start_timestamp, stop_timestamp = get_timestamps(month, year)

        sql = "" \
        "SELECT COUNT(*) " \
        "FROM ListensToSong " \
        "WHERE songTitle = %s AND creatorId = %s AND albumName = %s AND edition = %s AND timestamp >= %s AND timestamp < %s;"

        tuple = (song_title, creator_id, album_name, edition, start_timestamp, stop_timestamp)
       
        cur.execute(sql, tuple)
        conn.commit()
        result = cur.fetchall()

        if print_table:
            print()
            print(tabulate([[str(month) + "-" + str(year), song_title, result[0][0]]], headers=["Month", "Song Title", "Play Count"], tablefmt='psql'))

        cur.close()
        conn.close()

        return True, result

    except mariadb.Error as e:
        print(f"Error calculating monthly play count for song.: {e}")
        cur.close()
        conn.close()
        return False, None
    
def calculate_monthly_play_count_album():
    """ Request information from the user and complete the calculation for the monthly play count for an album.
    """
    try:
        creator_id = get_creator_id()
        album_name = get_album_name() 
        edition = get_album_edition()
        month = get_month()
        year = get_year()
        sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year)
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year):
    """ Execute a SQL query to get the monthly play count for the album provided in the arguments.
    
    Args:
        album_name: The album name.
        edition   : The edition of the album.
        creator_id: The creator of the album.
        month     : The month to get the count for
        year      : The year that the month is in.

    """
    conn, cur = db.Database().connect_to_MariaDB()

    try:

        start_timestamp, stop_timestamp = get_timestamps(month, year)

        sql = "" \
        "SELECT COUNT(*) " \
        "FROM ListensToSong " \
        "WHERE albumName = %s AND edition = %s AND creatorId = %s AND timestamp >= %s AND timestamp < %s;"

        cur.execute(sql, (album_name, edition, creator_id, start_timestamp, stop_timestamp))
        conn.commit()

        result = cur.fetchall()

        print()
        print(tabulate([[str(month) + "-" + str(year), album_name, result[0][0]]], headers=["Month", "Album Name", "Play Count"], tablefmt='psql'))

        cur.close()
        conn.close()

        return True, result

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None

    
def calculate_monthly_play_count_artist(): 
    """ Request information from the user and complete the calculation for the monthly play count for an artist.
    """
    try:
        creator_id = get_creator_id()
        month = get_month()
        year = get_year()
        sql_calculate_monthly_play_count_artist(creator_id, month, year)
    except Exception as e:
        print("There was an error with the input provided. Try again.")


def sql_calculate_monthly_play_count_artist(creator_id, month, year):
    """ Execute a SQL query to get the monthly play count for the artist provided in the arguments.
    
    Args:
        creator_id: The artist's creator ID.
        month     : The month to get the count for
        year      : The year that the month is in.

    """
    conn, cur = db.Database().connect_to_MariaDB()
    try:

        start_timestamp, stop_timestamp = get_timestamps(month, year)

        sql = "" \
        "SELECT COUNT(*) " \
        "FROM ListensToSong " \
        "WHERE creatorId = %s AND timestamp >= %s AND timestamp < %s;"

        cur.execute(sql, (creator_id, start_timestamp, stop_timestamp))
        conn.commit()

        result = cur.fetchall()

        print()
        print(tabulate([[str(month) + "-" + str(year), creator_id, result[0][0]]], headers=["Month", "Artist", "Play Count"], tablefmt='psql'))

        cur.close()
        conn.close()

        return True, result

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None

def calculate_total_payment_to_host_per_time_period():
    """ Request information from the user and complete the calculation for the total payments to the host for the given time period.
    """
    try:
        creator_id = get_creator_id()
        start_date = get_start_date()
        stop_date = get_stop_date()
        sql_calculate_total_payment_to_host_per_time_period(creator_id, start_date, stop_date)
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_calculate_total_payment_to_host_per_time_period(creator_id, start_date, stop_date):
    """ Execute a SQL query to get the total value of the payments made to the host in the given time period.
    
    Args:
        creator_id: The artist's creator ID.
        start_date: The start of the time period to calculate the payments for.
        stop_date : The end of the time period to calculate the payments for.

    """
    conn, cur = db.Database().connect_to_MariaDB()
    try:
        sql = "" \
        "SELECT SUM(value) " \
        "FROM Payment NATURAL JOIN PayToContentCreator NATURAL JOIN PodcastHost " \
        "WHERE creatorId = %s AND date >= %s AND date < %s;"

        cur.execute(sql, (creator_id, start_date, stop_date))
        conn.commit()

        result = cur.fetchall()

        if(result[0][0] == None):
            result[0] = (0.0, )

        print()
        print(tabulate([[start_date, stop_date, creator_id, result[0][0]]], headers=["Start Date", "Stop Date", "Host", "Total Payment"], tablefmt='psql'))

        cur.close()
        conn.close()

        return True, result

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None
    
def calculate_total_payment_to_artist_per_time_period():
    """ Request information from the user and complete the calculation for the total payments to the artist for the given time period.
    """
    try:
        creator_id = get_creator_id()
        start_date = get_start_date()
        stop_date = get_stop_date()
        sql_calculate_total_payment_to_artist_per_time_period(creator_id, start_date, stop_date)
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_calculate_total_payment_to_artist_per_time_period(creator_id, start_date, stop_date):
    """ Execute a SQL query to get the total value of the payments made to the host in the given time period.
    
    Args:
        creator_id: The artist's creator ID.
        start_date: The start of the time period to calculate the payments for.
        stop_date : The end of the time period to calculate the payments for.

    """
    conn, cur = db.Database().connect_to_MariaDB()
    try:
        sql = "" \
        "SELECT SUM(value) " \
        "FROM Payment NATURAL JOIN PayToContentCreator NATURAL JOIN Artist " \
        "WHERE creatorId = %s AND date >= %s AND date < %s;"

        cur.execute(sql, (creator_id, start_date, stop_date))
        conn.commit()

        result = cur.fetchall()

        if(result[0][0] == None):
            result[0] = (0.0, )

        print()
        print(tabulate([[start_date, stop_date, creator_id, result[0][0]]], headers=["Start Date", "Stop Date", "Artist", "Total Payment"], tablefmt='psql'))

        cur.close()
        conn.close()

        return True, result

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None
    
def calculate_total_payment_to_record_label_per_time_period():
    """ Request information from the user and complete the calculation for the total payments to the record for the given time period.
    """
    try:
        record_label_name = get_record_label()
        start_date = get_start_date()
        stop_date = get_stop_date()
        sql_calculate_total_payment_to_record_label_per_time_period(record_label_name, start_date, stop_date)
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_calculate_total_payment_to_record_label_per_time_period(record_label_name, start_date, stop_date):
    """ Execute a SQL query to get the total value of the payments made to the record label in the given time period.
    
    Args:
        record_label_name: The record label's name.
        start_date       : The start of the time period to calculate the payments for.
        stop_date        : The end of the time period to calculate the payments for.

    """
    conn, cur = db.Database().connect_to_MariaDB()
    try:
        sql = "" \
        "SELECT SUM(value) " \
        "FROM Payment NATURAL JOIN PayToRecordLabel, RecordLabel " \
        "WHERE RecordLabel.labelName = PayToRecordLabel.recordLabelName AND recordLabelName = %s AND date >= %s AND date < %s;"

        cur.execute(sql, (record_label_name, start_date, stop_date))
        conn.commit()

        result = cur.fetchall()

        if(result[0][0] == None):
            result[0] = (0.0, )

        print()
        print(tabulate([[start_date, stop_date, record_label_name, result[0][0]]], headers=["Start Date", "Stop Date", "Record Label", "Total Payment"], tablefmt='psql'))

        cur.close()
        conn.close()

        return True, result

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None
    
def calculate_total_revenue_per_month():
    """ Request information from the user and complete the calculation for the total revenue for the month provided.
    """
    try:
        month = get_month()
        year = get_year()
        sql_calculate_total_revenue_per_month(month, year)
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_calculate_total_revenue_per_month(month, year):
    """ Execute a SQL query to get the total revenue for the given month.
    
    Args:
        month : The month to calculate the total revenue for (as an int 1-12).
        year  : The year of the month as an int.

    """
    conn, cur = db.Database().connect_to_MariaDB()
    try:
        start_date, stop_date = get_dates(month, year)

        sql = "" \
        "SELECT SUM(value) " \
        "FROM PayFromUser NATURAL JOIN Payment " \
        "WHERE date >= %s AND date < %s;"

        cur.execute(sql, (start_date, stop_date))
        conn.commit()
        result = cur.fetchall()

        if(result[0][0] == None):
            result[0] = (0.0, )

        print()
        print(tabulate([[str(month) + "-" + str(year), result[0][0]]], headers=["Month", "Revenue"], tablefmt='psql'))

        cur.close()
        conn.close()
        return True, result

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None
    
def calculate_total_revenue_per_year():
    """ Request information from the user and complete the calculation for the total revenue for the year provided.
    """
    try:
        year = get_year()
        sql_calculate_total_revenue_per_year(year)
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_calculate_total_revenue_per_year(year):
    """ Execute a SQL query to get the total revenue for the given year.
    
    Args:
        year : The year to calculate the revenue for as an int.

    """
    conn, cur = db.Database().connect_to_MariaDB()
    try:

        start_date, endDate = get_dates_from_year(year)

        sql = "" \
        "SELECT SUM(value) as annualRevenue " \
        "FROM PayFromUser NATURAL JOIN Payment " \
        "WHERE date >= %s AND date < %s;"

        cur.execute(sql, (start_date, endDate))
        conn.commit()

        result = cur.fetchall()
        
        if(result[0][0] == None):
            result[0] = (0.0, )
                    
        print()
        print(tabulate([[year, result[0][0]]], headers=["Year", "Revenue"], tablefmt='psql'))

        cur.close()
        conn.close()
        return True, result
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None
    
def report_songs_artist():
    """ Request information from the user and report the songs for the given artist.
    """
    try:
        creator_id = get_creator_id()
        sql_report_songs_artist(creator_id);
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_report_songs_artist(creator_id):
    """ Execute a SQL query to get the list of songs created by an artist.
    
    Args:
        creator_id : The artist to retrieve songs for.

    """
    conn, cur = db.Database().connect_to_MariaDB()
    try:
        output_result = []
        sql = "" \
        "SELECT Song.SID, Song.songTitle, Song.creatorId, Song.albumName, Song.edition, Song.playCount, Song.royaltyRate, CollaboratesOn.guestArtistId, Song.royaltyPaidStatus " \
        "FROM Song LEFT JOIN CollaboratesOn " \
        "ON Song.creatorId = CollaboratesOn.creatorId AND Song.songTitle = CollaboratesOn.songTitle AND Song.albumName = CollaboratesOn.albumName AND Song.edition = CollaboratesOn.edition " \
        "WHERE Song.creatorId = %s;"

        cur.execute(sql, (creator_id,))
        conn.commit()
        result = cur.fetchall()

        i = 0
        for value in result:
            creator_id = value[2]
            album_name = value[3]
            edition = value[4]
            song_title = value[1]
            status = value[8]
            play_count = sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, 4, 2023, False)
            list_result = list(result[i])
            list_result[5] = play_count[1][0][0]
            if status == 0:
                list_result[8] = False
            else: 
                list_result[8] = True
            output_result.append(list_result)
            i = i+1


        print()
        print(tabulate(output_result, headers=["Song ID", "Song Title", "Artist", "Album Name", "Album Edition", "Play Count", "Royalty Rate (usd)", "Collaborators", "Royalty Paid Status"], tablefmt='psql'))

        cur.close()
        conn.close()
        return True, output_result
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None
    
def report_songs_album():
    """ Request information from the user and report the songs for the given album.
    """
    try:
        album_name = get_album_name()
        edition = get_album_edition()
        sql_report_songs_album(album_name, edition)
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_report_songs_album(album_name, edition):
    """ Execute a SQL query to get the list of songs created by an artist on a certain album.
    
    Args:
        album_name : The name of the album.
        edition    : The edition of the album. 

    """
    conn, cur = db.Database().connect_to_MariaDB()
    try:
        output_result = []
        sql = "" \
        "SELECT Song.SID, Song.songTitle, Song.creatorId, Song.albumName, Song.edition, Song.playCount, Song.royaltyRate, CollaboratesOn.guestArtistId, Song.royaltyPaidStatus " \
        "FROM Song LEFT JOIN CollaboratesOn " \
        "ON Song.creatorId = CollaboratesOn.creatorId AND Song.songTitle = CollaboratesOn.songTitle AND Song.albumName = CollaboratesOn.albumName AND Song.edition = CollaboratesOn.edition " \
        "WHERE Song.albumName = %s AND Song.edition = %s;"

        cur.execute(sql, (album_name, edition))
        conn.commit()
        result = cur.fetchall()

        i = 0
        for value in result:
            creator_id = value[2]
            album_name = value[3]
            edition = value[4]
            song_title = value[1]
            status = value[8]
            play_count = sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, 4, 2023, False)
            list_result = list(result[i])
            list_result[5] = play_count[1][0][0]
            if status == 0:
                list_result[8] = False
            else: 
                list_result[8] = True

            output_result.append(list_result)
            i = i+1

        print()
        print(tabulate(output_result, headers=["Song ID", "Song Title", "Artist", "Album Name", "Album Edition", "Play Count", "Royalty Rate (usd)", "Collaborators", "Royalty Paid Status"], tablefmt='psql'))

        cur.close()
        conn.close()
        return True, output_result
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None
    
def report_songs_album_and_artist():
    """ Request information from the user and report the songs for the given album and artist.
    """
    try:
        album_name = get_album_name()
        edition = get_album_edition()
        creator_id = get_creator_id()
        sql_report_songs_album_and_artist(album_name, edition, creator_id)
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_report_songs_album_and_artist(album_name, edition, creator_id):
    """ Execute a SQL query to get the list of songs created by an artist on a certain album.
    
    Args:
        album_name : The name of the album.
        edition    : The edition of the album. 
        creator_id : The artist of the album.

    """
    conn, cur = db.Database().connect_to_MariaDB()
    try:
        output_result = []
        sql = "" \
        "SELECT Song.SID, Song.songTitle, Song.creatorId, Song.albumName, Song.edition, Song.playCount, Song.royaltyRate, CollaboratesOn.guestArtistId, Song.royaltyPaidStatus " \
        "FROM Song LEFT JOIN CollaboratesOn " \
        "ON Song.creatorId = CollaboratesOn.creatorId AND Song.songTitle = CollaboratesOn.songTitle AND Song.albumName = CollaboratesOn.albumName AND Song.edition = CollaboratesOn.edition " \
        "WHERE Song.albumName = %s AND Song.edition = %s AND Song.creatorId = %s;"

        cur.execute(sql, (album_name, edition, creator_id))
        conn.commit()

        result = cur.fetchall()

        i = 0
        for value in result:
            creator_id = value[2]
            album_name = value[3]
            edition = value[4]
            song_title = value[1]
            status = value[8]
            play_count = sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, 4, 2023, False)
            list_result = list(result[i])
            list_result[5] = play_count[1][0][0]
            if status == 0:
                list_result[8] = False
            else: 
                list_result[8] = True

            output_result.append(list_result)
            i = i+1

        print()
        print(tabulate(output_result, headers=["Song ID", "Song Title", "Artist", "Album Name", "Album Edition", "Play Count", "Royalty Rate (usd)", "Collaborators", "Royalty Paid Status"], tablefmt='psql'))

        cur.close()
        conn.close()
        return True, output_result
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None
    
def report_podcasts_epsiodes():
    """ Request information from the user and report the episodes for the given podcast.
    """
    try:
        podcast_name = get_podcast_name()
        sql_report_podcasts_epsiodes(podcast_name)
    except Exception as e:
        print("There was an error with the input provided. Try again.")

def sql_calculate_listening_count_podcast_episode(podcast_name, episode_name):
    """ Execute a SQL query to get the monthly play count for the podcast provided in the arguments.
    
    Args:
        podcast_name: The podcast to query.
        episode_name: The episode to query.

    """
    conn, cur = db.Database().connect_to_MariaDB()

    try:

        sql = "" \
        "SELECT COUNT(*) " \
        "FROM ListensToPodcastEpisode " \
        "WHERE podcastEpisodeTitle = %s AND podcastName = %s;"

        tuple = (episode_name, podcast_name)
       
        cur.execute(sql, tuple)
        conn.commit()
        result = cur.fetchall()

        cur.close()
        conn.close()

        return True, result

    except mariadb.Error as e:
        print(f"Error calculating monthly play count for song.: {e}")
        cur.close()
        conn.close()
        return False, None


def sql_report_podcasts_epsiodes(podcast_name):
    """ Execute a SQL query to get the list of episodes for a chosen podcast.
    
    Args:
        podcast_name : The name of the podcast.

    """
    conn, cur = db.Database().connect_to_MariaDB()
    try:
        output_result = []
        sql = "" \
        "SELECT PodcastEpisode.PEID, PodcastEpisode.title, PodcastEpisode.podcastName, GuestStars.creatorId, PodcastEpisode.advertisementCount " \
        "FROM PodcastEpisode LEFT JOIN GuestStars " \
        "ON PodcastEpisode.title = GuestStars.title AND PodcastEpisode.podcastName = GuestStars.podcastName " \
        "WHERE PodcastEpisode.podcastName = %s;"

        cur.execute(sql, (podcast_name,))
        conn.commit()

        result = cur.fetchall()

        i = 0
        for value in result:
            episode_name = value[1]
            podcast_name = value[2]
            play_count = sql_calculate_listening_count_podcast_episode(podcast_name, episode_name)
            list_result = list(result[i])
            list_result.append(play_count[1][0][0])
            output_result.append(list_result)
            i = i+1

        print()
        print(tabulate(output_result, headers=["Podcast Episode ID", "Episode Name", "Podcast Name", "Guest Star", "Ad Count", "Listen Count"], tablefmt='psql'))

        cur.close()
        conn.close()
        return True, output_result
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        cur.close()
        conn.close()
        return False, None