"""
Module for metadata maintenance.
"""
import warnings
import pandas as pd
import mariadb
import sys
from tabulate import tabulate
import datetime
from operations import db
import random
from time import time

if not sys.warnoptions:
    warnings.simplefilter('ignore')


def update_all_play_counts():
    """
    Helper function to manage update of all song play counts in the db. Calculates the total play counts for a specified
    time period and updates the values in the Songs SQL table to reflect the proper values.

    :return: No data object returned, updates database and prints confirmation. Returns none to escape the function if
    one of the updates fails.
    """

    when = input('Please enter the month (Format: YYYY-MM) the play count should be updated for: ')
    start = f'{when}-01'
    month = int(when[5:])
    year = when[:4]
    end = f'{year}-{month+1}-01'

    # Get list of songs
    song_sql = (f'SELECT songTitle, creatorId, albumName, edition FROM Song;')

    # Get connection
    conn, cur = db.Database().connect_to_MariaDB()

    # Execute query
    songs = pd.read_sql(song_sql, conn)

    n_songs = len(songs)

    # Get play count for each song in database
    for i in range(0, len(songs)):
        # Grab keys
        song = songs.iloc[i, 0]
        creatorId = songs.iloc[i, 1]
        album = songs.iloc[i, 2]
        edition = songs.iloc[i, 3]

        # Get play count for specified song
        count_sql = (f'SELECT COUNT(*) AS playCount FROM ListensToSong WHERE songTitle="{song}" AND creatorId="{creatorId}" '
                     f'AND albumName="{album}" AND edition="{edition}" AND timestamp>="{start}" '
                     f'AND timestamp<"{end}";')

        count_result = pd.read_sql(count_sql, conn)
        play_count = count_result.loc[0, "playCount"]

        # Update the play count for that song in the Song relation
        sql = (f'UPDATE Song SET playCount = {play_count} WHERE songTitle = "{song}" '
               f'AND albumName = "{album}" AND edition = "{edition}" AND creatorId = {creatorId};')

        # Try to execute update
        try:
            cur.execute('START TRANSACTION;')
            cur.execute(sql)
            cur.execute('COMMIT;')

        except mariadb.Error as e:
            print(f'Error updating play count for {song}: {e}')
            cur.execute('ROLLBACK;')

            conn.close()
            return None

    # Print confirmation if all successful
    print(f'Play count successfully updated for {n_songs} songs!')
    conn.close()


def update_song_play_count():
    """
    This function gathers interactive inputs that allow the database to specify a specific song, then updates its
    play count to a specified number. The function itself takes no arguments, as the inputs are gathered dynamically
    from the user through the terminal interface.

    For this particular function, we have elected to use the creatorId directly, as updating a play count is not likely
    to be a user-facing operation, and we assume that the admin staff making the update would know the artist creatorId.

    :return: The function does not "return" any data objects in the standard sense. However, the function does print a
    confirmation that the update was successful or unsuccessful. In the successful case, the function also outputs a
    view from the db with the new play count.
    """

    # Get key info
    song = input('What song would you like to update the play count for? If you would like to update the play count for '
                 'all songs, please enter "all": ')

    # Handle the all case
    if song == 'all':
        update_all_play_counts()

    # Otherwise continue with information gathering.
    else:
        album = input('What album is the song on? ')
        edition = input('Please tell us which edition of the album you are referring to: ')
        creatorId = input('Please provide the creatorId of the artist who wrote the song: ')
        when = input('Please enter the month (Format: YYYY-MM) the play count should be updated for: ')
        start = f'{when}-01'
        month = int(when[5:])
        year = when[:4]
        end = f'{year}-{month + 1}-01'

        # Connect to db
        conn, cur = db.Database().connect_to_MariaDB()

        # Get play count for specified song
        count_sql = (
            f'SELECT COUNT(*) AS playCount FROM ListensToSong WHERE songTitle="{song}" AND creatorId="{creatorId}" '
            f'AND albumName="{album}" AND edition="{edition}" AND timestamp>="{start}" '
            f'AND timestamp<"{end}";')

        count_result = pd.read_sql(count_sql, conn)
        play_count = count_result.loc[0, "playCount"]

        # Build SQL statements for execution and confirmation
        sql = (f'UPDATE Song SET playCount = {play_count} WHERE songTitle = "{song}" '
               f'AND albumName = "{album}" AND edition = "{edition}" AND creatorId = {creatorId};')


        view = (f'SELECT * FROM Song WHERE songTitle = "{song}" '
               f'AND albumName = "{album}" AND edition = "{edition}" AND creatorId = {creatorId};')

        try:
            # Execute update transaction
            cur.execute('START TRANSACTION;')
            cur.execute(sql)
            cur.execute('COMMIT;')

            # Confirmation
            print(f'{song} play count updated.')
            print(tabulate(pd.read_sql(view, conn), headers='keys', tablefmt='psql'))

            # Close connection
            conn.close()

        except mariadb.Error as e:
            # Catch error, display, rollback attempted transaction, and close connection
            # It is assumed that if the song doesn't exist that error will be reflected here as well
            print(f'Error with update: {e}')
            cur.execute('ROLLBACK;')
            conn.close()


def update_podcast_ratings():
    """
    This function is very similar to the update_song_play_count() function. Again, inputs are gathered dynamically
    from the user rather than passed to the function itself. Gets the inputs needed to form a key, value for the rating
    update, then attempts to execute the update.

    :return: Again, there is no object returned by the function, but it does provide a notification of whether the
    update was successful or not. If successful, a view of the db with the new value is displayed as well.
    """

    # Gather user inputs
    podcast = input('Which podcast would you like to update the ratings for? ')
    rating = input(f'Please enter the latest rating for {podcast}: ')

    # Build queries
    sql = (f'UPDATE Podcast SET rating = {rating} WHERE podcastName = "{podcast}";')

    view = (f'SELECT * FROM Podcast WHERE podcastName = "{podcast}";')

    # conn, cur = dbconnect.connect_to_MariaDB()
    conn, cur = db.Database().connect_to_MariaDB()

    # Attempt update
    try:
        # Execute update transaction
        cur.execute('START TRANSACTION;')
        cur.execute(sql)
        cur.execute('COMMIT;')

        # Confirmation
        print(f'{podcast} rating updated.')
        print(tabulate(pd.read_sql(view, conn), headers='keys', tablefmt='psql'))

        # Close connection
        conn.close()

    except mariadb.Error as e:
        # Catch error, display, rollback attempted transaction, and close connection
        print(f'Error with update: {e}')
        cur.execute('ROLLBACK;')
        conn.close()


def find_songs_given_artist():
    """
    This function is designed as if it were user-facing (i.e., the user has searched for an artist, and would like to
    see their songs). The difference from the previous two functions is that it does not assume knowledge of a creatorId
    by the person searching. As such, it takes the artist name, searches the db to find the creatorId for key formation,
    and then proceeds with displaying all songs associated with that artist.

    There is some functionality to handle different results from the creatorId search. In the unlikely event that there
    are two artists or content creators in the system with the same name in the firstName column, then the program will
    provide that list to the user and have them choose the correct creatorId to search. It then builds and executes
    the SELECT query.

    :return: There is no data object returned. The function instead prints an output of the songs associated with the
    given artist in the database.
    """
    # Get artist from user input
    artist = input('Which artist would you like to see songs for? ')

    # Get connection
    conn, cur = db.Database().connect_to_MariaDB()

    # Find creatorId for that artist, if multiple artists have the same name, make user choose the correct creatorId
    id_sql = (f'SELECT * FROM ContentCreator WHERE firstName = "{artist}";')

    # Make sure we find a result
    valid_result = True
    try:
        # Get entries associated with artist name
        result = pd.read_sql(id_sql, conn)

        # Extract creatorId from result
        if len(result.index) == 1:
            creatorId = result.loc[0, 'creatorId']

        # If more than one artist with same name, make user choose (and enter the correct creatorId)
        elif len(result.index) > 1:
            print('We found more than one artist matching your input, shown in the table below: ')
            print(tabulate(result, headers='keys', tablefmt='psql'))
            creatorId = input('Please enter the creatorId associated with the artist you were looking for: ')

        # If no artists found, say no valid result, let the user know, and close the connection
        else:
            print('We could not find the artist you were looking for :(')
            valid_result = False
            conn.close()

    # Catch error if the artist name isn't found, stop progression, and close connection
    except mariadb.Error as e:
        print(f'Error fetching artist creatorId: {e}')
        valid_result = False
        conn.close()

    # If no errors getting creatorId
    if valid_result:

        # Build query
        sql = (f'SELECT songTitle, albumName, duration FROM Song NATURAL JOIN Artist '
               f'WHERE creatorId = {creatorId}')

        # Execute search and display results
        try:
            print(f'Here are all the songs we have for {artist}: ')
            print(tabulate(pd.read_sql(sql, conn), headers='keys', tablefmt='psql'))

            conn.close()

        # Catch any errors, report them, ensure connection closed
        except mariadb.Error as e:
            print(f'Error retrieving songs: {e}')

            conn.close()


def find_songs_given_album():
    """
    Similar to find_songs_given_artist(). However, in this case, ensuring the correct album with minimal input from the
    user is a bit more challenging. In this case, we must check for multiple albums with the same name, then resolve
    any conflicts between multiple artists with the same album name or an album with multiple editions by one artist.

    There are some helper functions included within to help with that objective. They have some documentation as well.

    :return: No data object return, but prints a list of songs on the selected album or prints an error message
    depending on whether the user's input is valid.
    """
    # Get album from user input
    album = input('Which album would you like to see the songs for? ')

    # Create connection objects
    conn, cur = db.Database().connect_to_MariaDB()

    # Search for given album, see if is unique
    album_sql = (f'SELECT * FROM Album NATURAL JOIN ContentCreator WHERE albumName = "{album}";')

    # Make sure we find a result
    valid_result = True
    try:
        # Get entries associated with artist name
        result = pd.read_sql(album_sql, conn)

        # Extract creatorId from result
        if len(result.index) == 1:
            creatorId = result.loc[0, 'creatorId']
            edition = result.loc[0, 'edition']
            artist = result.loc[0, 'firstName']

        # If there is no result, print an error message and break the control flow by switching valid_result
        elif len(result.index) == 0:
                print('We could not find the album you were looking for :(')
                valid_result = False
                conn.close()

        # If more than one artist with same name, or multiple artists with same album name
        # make user choose (and enter the correct creatorId)
        else:
            def check_artists(result):
                """
                This function helps check for and resolve the situation where there are multiple artists with the same
                album name. A function was used for check_artist and check_edition to avoid heavily nested conditional
                statements.

                :param result: this is the table returned from the album search above.
                :return: Returns the result, filtered by a selected creatorId if there are multiple artists, and
                returns the creatorId either selected or found
                """
                # Get the creatorId and artist name from result
                check_artists = result.get(['creatorId', 'firstName'])

                # Drop duplicate artist names
                check_artists.drop_duplicates('firstName', inplace=True)

                # See how many are left. If more than one, have the user select the correct creatorId
                if len(check_artists.index) > 1:
                    print('We found more than one artist matching your input, shown in the table below: ')
                    print(tabulate(check_artists, headers='keys', tablefmt='psql'))
                    creatorId = input('Please enter the creatorId associated with the artist you were looking for: ')

                    # Filter the original result by creatorId to ensure there is only the one artist
                    result = result[result['creatorId'] == int(creatorId)]

                # If there is only one artist left after dropping duplicates, grab the creatorId and keep moving
                else:
                    result.reset_index(inplace=True)
                    creatorId = result.loc[0, 'creatorId']

                return result, creatorId

            # Function call
            result, creatorId = check_artists(result)

            # Reset the index to avoid numbering issues with the .loc call, assign artist name
            result.reset_index(inplace=True)
            artist = result.loc[0, 'firstName']

            def check_editions(result):
                """
                This function is similar to check_artists() but it resolves any conflicts with multiple editions.

                :param result: This is the filtered result after running through the artist check
                :return: This one returns a result with only the correct edition selected and returns that edition
                """
                # Get relevant columns from the result
                check_edition = result.get(['firstName', 'albumName', 'edition'])

                # If there are multiple rows left with only the one artist, make user specify the correct edition
                if len(check_edition.index) > 1:
                    print('We found more than one edition of the album matching your input, shown in the table below: ')
                    print(tabulate(check_edition, headers='keys', tablefmt='psql'))
                    edition = input('Please enter the edition of the album you are searching for from the table: ').title()

                    # Filter result by selected edition. Should have only one row left
                    result = result[result['edition'] == edition]

                else:
                    # If there is only one, reset index to make sure the numbering is right, get the edition value
                    result.reset_index(inplace=True)
                    edition = result.loc[0, 'edition']

                return result, edition

            # Function call
            result, edition = check_editions(result)

    # Catch error if the album name isn't found, stop progression, and close connection
    except mariadb.Error as e:
        print(f'Error fetching album info: {e}')
        valid_result = False
        conn.close()

    # If no errors getting creatorId
    if valid_result:

        # Build query
        sql = (f'SELECT songTitle, duration FROM Song '
               f'WHERE albumName = "{album}" AND edition = "{edition}" AND creatorId = {creatorId}')

        # Execute search and display results
        try:
            print(f'Here are all the songs we have for {album}, {edition} Edition, by {artist}: ')
            print(tabulate(pd.read_sql(sql, conn), headers='keys', tablefmt='psql'))

            conn.close()

        # Catch any errors, report them, ensure connection closed
        except mariadb.Error as e:
            print(f'Error retrieving songs: {e}')

            conn.close()


def find_podcast_episodes_given_podcast():
    """
    This function takes a dynamic user input of podcast name and prints the list of episodes available for that podcast.
    Similar to the find songs given X functions.

    :return: No data object returned, but does print out a list of episodes for the user to view.
    """
    # Get podcast
    podcast = input('Please enter the podcast you would like to see episodes for: ')

    # Get connection
    conn, cur = db.Database().connect_to_MariaDB()

    # Build query
    sql = (f'SELECT title, duration FROM PodcastEpisode '
           f'WHERE podcastName = "{podcast}";')

    # Try to get result
    try:
        print(f'Here are all the episodes we found for {podcast}:')
        print(tabulate(pd.read_sql(sql, conn), headers='keys', tablefmt='psql'))

        conn.close()

    # Catch possible errors and ensure that connection closes
    except mariadb.Error as e:
        print(f'Error reading the table: {e}')
        conn.close()


def generate_random_timestamp(month_str):
    """
    Helper function to generate a random timestamp given a month.
    :param month_str: desired month formatted as YYYY-MM
    :return: string formatted as a timestamp that is SQL friendly.
    """
    # Get possible days from month
    if month_str[5:] in ['01', '03', '05', '07', '08', '10', '12']:
        n_days = 31

    elif month_str[5:] == '02':
        n_days = 28

    else:
        n_days = 30

    # Build timestamp
    day = str(random.randint(1, n_days))
    hour = str(random.randint(0, 23))
    minute = str(random.randint(0, 59))
    second = str(random.randint(0, 59))

    if len(day) < 2:
        day = '0' + day

    if len(hour) < 2:
        hour = '0' + hour

    if len(minute) < 2:
        minute = '0' + minute

    if len(second) < 2:
        second = '0' + second

    return f'{month_str}-{day} {hour}:{minute}:{second}'


def get_bulk_song_inputs():
    """
    Helper function to gather inputs for bulk adding song listens.
    :return: all inputs needed for bulk_add_song_listens() function
    """
    # Get data to make inputs
    song = input('Please enter the name of the song you would like to add bulk listens to: ')
    album = input('Please enter the name of the album the song is on: ')
    edition = input('Please enter the album edition: ')
    artist = input('Please enter the name of the artist who wrote the song: ')
    month = input('Please enter the month you would like to add the listens to (Format: YYYY-MM): ')
    n_records = input('How many "listen to" records should be generated? ')

    return song, album, edition, artist, month, n_records


def bulk_add_song_listens(song, album, edition, artist, month, n_records):
    """
    This function is used to prove database functionality and bulk add users to the ListensToSong relation.

    :param: song -- name of the song to be listened to
    :param: album -- album containing the song
    :param: edition -- album edition
    :param: artist -- artist who wrote the song
    :param: month -- the month the listens take place in
    :param: n_records -- number of tuples to enter into the table

    :return: returns a confirmation that the additions were successful.
    """

    # Get connection
    conn, cur = db.Database().connect_to_MariaDB()

    # Find creatorId for that artist, if multiple artists have the same name, make user choose the correct creatorId
    id_sql = (f'SELECT * FROM ContentCreator WHERE firstName = "{artist}";')

    # Make sure we find a result
    valid_result = True
    try:
        # Get entries associated with artist name
        result = pd.read_sql(id_sql, conn)

        # Extract creatorId from result
        if len(result.index) == 1:
            creatorId = result.loc[0, 'creatorId']

        # If more than one artist with same name, make user choose (and enter the correct creatorId)
        elif len(result.index) > 1:
            print('We found more than one artist matching your input, shown in the table below: ')
            print(tabulate(result, headers='keys', tablefmt='psql'))
            creatorId = input('Please enter the creatorId associated with the artist you were looking for: ')

        # If no artists found, say no valid result, let the user know, and close the connection
        else:
            print('We could not find the artist you were looking for :(')
            valid_result = False
            conn.close()

    # Catch error if the artist name isn't found, stop progression, and close connection
    except mariadb.Error as e:
        print(f'Error fetching artist creatorId: {e}')
        valid_result = False
        conn.close()

    # If no errors getting creatorId
    if valid_result:
        # Pull table of users
        user_sql = ('SELECT * FROM User;')
        users = pd.read_sql(user_sql, conn)
        n_users = len(users.index)

        # Get existing ListensToSong records to avoid duplication
        song_listens = pd.read_sql(('SELECT * FROM ListensToSong;'), conn)
        song_listens = list(song_listens.itertuples(index=False, name=None))

        t1 = time()
        inserts = []
        while len(inserts) < int(n_records):
            # Build random timestamp
            timestamp = generate_random_timestamp(month)

            # Choose random user email
            user_ind = random.randint(0, n_users - 1)
            email = users.loc[user_ind, 'email']

            # Build insert tuple
            record = (email, song, int(creatorId), album, edition, timestamp)

            if record in inserts:
                pass

            if record in song_listens:
                pass

            else:
                inserts.append(record)

        t2 = time()

        print(f'It took {t2-t1} seconds to randomly generate {n_records} records.')

        # Insert records into table
        try:
            sql = ("INSERT INTO ListensToSong (email, songTitle, creatorId, albumName, edition, timestamp) VALUES (%s, %s, %s, %s, %s, %s)")
            t1 = time()

            if len(inserts) < 1000:
                cur.execute('START TRANSACTION;')
                cur.executemany(sql, inserts)
                cur.execute('COMMIT;')

            else:
                while len(inserts) > 1000:
                    chunk = inserts[:1000]
                    inserts = inserts[1000:]
                    cur.execute('START TRANSACTION;')
                    cur.executemany(sql, chunk)
                    cur.execute('COMMIT;')

                if len(inserts) > 0:
                    cur.execute('START TRANSACTION;')
                    cur.executemany(sql, inserts)
                    cur.execute('COMMIT;')

            t2 = time()
            print(f'{n_records} random records inserted into ListensToSong in {t2-t1} seconds.')

            conn.close()

        except mariadb.Error as e:
            print(f'Error inserting random records: {e}')
            cur.execute('ROLLBACK;')

            conn.close()


def update_artist_monthly_listeners():
    """
    This function has a control flow element based on a user choice for which action they would like to take. Allows
    the user to either view monthly listeners (as it is calculated implicitly rather than stored as an attribute) or to
    "update" monthly listeners for a given month by "listening to a song."

    I didn't quite realize how this would go until it was too far gone, but I should have written different functions
    for each of the choices. However, it appears to work as intended.

    :return: No data object is returned. Depending on the user choice, there is a different print output. If the user
    opts to view monthly listeners, a table with the artist and monthly listener count is returned. If the user listens
    to a song, the program outputs a confirmation message if the listen event is inserted correctly or an error message
    if not.
    """
    # Note about handling monthly listeners
    print('In trying to replicate the real world, we chose to calculate monthly listeners implicitly based on our '
          'ListensToSong relation. As such, the number cannot be updated directly. However, you can listen to a song '
          'to influence that number if you would like. \n')

    # Get user choice for desired action
    choice = int(input('Please enter the number corresponding to the option you prefer: '
                       '\n  1) See monthly listeners for an artist. '
                       '\n  2) Listen to a song.'
                       '\n  3) Bulk add listeners to a song. \n'))

    # View monthly listeners case
    if choice == 1:
        # User inputs an artist name and a desired month
        artist = input('Please enter the artist you would like to see the monthly listeners for: ')
        when = input('Please enter a month and year (format: YYYY-MM) you would like to see monthly listeners for: ')

        # Start and end points are appended to the month
        start = f'{when}-01'
        month = int(when[5:])
        year = when[:4]
        end = f'{year}-{month + 1}-01'

        # Connect to db
        conn, cur = db.Database().connect_to_MariaDB()

        # Try to gather creatorId from artist name
        creatorId_sql = (f'SELECT * FROM ContentCreator WHERE firstName = "{artist}";')

        # Start logic gate
        valid_result = True
        try:
            # Read results from search of ContentCreator relation
            creatorId_result = pd.read_sql(creatorId_sql, conn)

            # Extract creatorId if there is only one result
            if len(creatorId_result.index) == 1:
                creatorId = creatorId_result.loc[0, 'creatorId']

            # Error out, break control flow if there are no results for the artist
            elif len(creatorId_result.index) == 0:
                valid_result = False
                print('We couldn\'t find the artist you were looking for :(')
                conn.close()

            # Make user choose creatorId if there happens to be more than one artist with the same name
            else:
                print('We found more than one artist matching your input, shown in the table below: ')
                print(creatorId_result.to_string())
                creatorId = input('Please enter the creatorId associated with the artist you were looking for: ')

        # Handle errors
        except mariadb.Error as e:
            print(f'Error finding the artist: {e}')
            conn.close()

        # If the above result passes the logic check...
        if valid_result:
            # Build query
            sql = (f'SELECT creatorId, firstName AS artist, COUNT(*) AS monthlyListeners FROM '
                   f'(SELECT DISTINCT creatorId, email FROM ListensToSong '
                   f'WHERE creatorId = {creatorId} AND timestamp >= "{start}" '
                   f'AND timestamp < "{end}") AS MonthlyListeners NATURAL JOIN ContentCreator;')

            # Execute search and display results
            try:
                print(f'Here are the monthly listeners we have for {artist} in {year}-{month}: ')
                print(tabulate(pd.read_sql(sql, conn), headers='keys', tablefmt='psql'))

                conn.close()

            # Catch any errors, report them, ensure connection closed
            except mariadb.Error as e:
                print(f'Error retrieving songs: {e}')
                conn.close()

    # Listen to song case
    elif choice == 2:
        # Gather inputs
        user = input('Please enter the email address of the user listening to the song: ')
        song = input('Please enter the name of the song you would like to listen to: ')
        album = input('Please enter the name of the album the song is on: ')
        artist = input('Please enter the name of the artist: ')
        when = input('When was the song listened to? Please enter a timestamp (format: YYYY-MM-DD HH:MM:SS) if you would'
                     ' like to specify a time. Otherwise, please enter "now": ')

        # Create a timestamp for right now if the user chooses
        if when == 'now':
            when = datetime.datetime.now()
            when = when.strftime('%Y-%m-%d %H:%M:%S')

        # Find artist creatorId
        # Get connection
        conn, cur = db.Database().connect_to_MariaDB()

        # Find creatorId for that artist, if multiple artists have the same name, make user choose the correct creatorId
        id_sql = (f'SELECT * FROM ContentCreator WHERE firstName = "{artist}";')

        # Make sure we find a result
        valid_artist = True
        try:
            # Get entries associated with artist name
            result = pd.read_sql(id_sql, conn)

            # Extract creatorId from result
            if len(result.index) == 1:
                creatorId = result.loc[0, 'creatorId']

            # If more than one artist with same name, make user choose (and enter the correct creatorId)
            elif len(result.index) > 1:
                print('We found more than one artist matching your input, shown in the table below: ')
                print(result.to_string())
                creatorId = input('Please enter the creatorId associated with the artist you were looking for: ')

            # If there is no artist found, print error message, break control flow, close connection
            else:
                print('We could not find the artist you were looking for :(')
                valid_artist = False
                conn.close()

        # Catch error if the artist name isn't found, stop progression, and close connection
        except mariadb.Error as e:
            print(f'Error fetching artist creatorId: {e}')
            valid_artist = False
            conn.close()

        # If no errors getting creatorId, try to find the album, make user select edition if multiple
        if valid_artist:
            album_sql = (f'SELECT albumName, edition FROM Album '
                         f'WHERE creatorId = {creatorId} AND albumName = "{album}";')

            # Assume we found nothing, set logic pass if we get a good result
            valid_album = False
            result = pd.read_sql(album_sql, conn)

            # Check to see if there are multiple editions or not
            # If one, grab edition, keep moving
            if len(result.index) == 1:
                edition = result.loc[0, 'edition']
                valid_album = True

            # If no results, print an error message, close connection, and end
            elif len(result.index) == 0:
                print('We could not find the album you were looking for :(')
                conn.close()

            # If more than one result, make user select the edition, keep moving
            elif len(result.index) > 1:
                print('We found multiple editions of the album you were searching for.\n ')
                print(tabulate(result, headers='keys', tablefmt='psql'))
                edition = input('Please enter the correct edition from the table above: ')
                valid_album = True

            # If we have the album, build and execute sql query
            if valid_album:
                try:
                    sql = (f'INSERT INTO ListensToSong (email, songTitle, creatorId, albumName, edition, timestamp) '
                           f'VALUES ("{user}", "{song}", {creatorId}, "{album}", "{edition}", "{when}");')

                    # Run transaction
                    cur.execute('START TRANSACTION;')
                    cur.execute(sql)
                    cur.execute('COMMIT;')

                    # Print confirmation, close connection
                    print(f'{user} listened to {song} on {album}, {edition} edition at {when}.')
                    conn.close()

                # Catch error if they occur, rollback transaction, close connection
                except mariadb.Error as e:
                    print(f'Error listening to song: {e}')
                    cur.execute('ROLLBACK;')
                    conn.close()

            # Close if statement
            else:
                print('There was an issue getting the correct album.')
                conn.close()

        # Close if statement
        else:
            print('There was an issue getting the correct artist.')
            conn.close()

    # Case for bulk adding listen events
    elif choice == 3:
        song, album, edition, artist, month, n_records = get_bulk_song_inputs()
        bulk_add_song_listens(song, album, edition, artist, month, n_records)

    # Error message if user does not select 1, 2, or 3
    else:
        print('You did not provide a valid input, please try again.')


def show_podcast_subscribers():
    """
    Function to calculate and display the number of subscribers for a given podcast. Part of the
    update_podcast_subscribers operation set. Gathers input dynamically from user, builds the query, and executes.

    :return: No data object returned. Instead, prints out a table with the name of the podcast and the number of
    subscribers.
    """

    # Get name of podcast
    podcast = input('Please enter the name of the podcast you would like to see subscribers for: ')

    # Build query
    sql = (f'SELECT podcastName, COUNT(*) AS subscribers FROM SubscribesToPodcast '
           f'WHERE podcastName = "{podcast}";')

    # Get connection
    conn, cur = db.Database().connect_to_MariaDB()

    # Try to execute query
    try:
        print(tabulate(pd.read_sql(sql, conn), headers='keys', tablefmt='psql'))
        conn.close()

    # Error out and close connection if query doesn't work
    except mariadb.Error as e:
        print(f'Error viewing subscribers: {e}')
        conn.close()


def subscribe_to_podcast():
    """
    Part of the update_podcast_subscribers flow. If the user wishes to subscribe to a podcast, they can specify the
    user email, the podcast to subscribe to, and the timestamp for that action to occur.

    :return: Does not return a data object. Prints a confirmation that the subscription was successful if it works,
    or provides an error message otherwise.
    """
    # Get podcast name and user who is subscribing
    user = input('Please enter the email address of the user who is subscribing: ')
    podcast = input(f'Please enter the podcast that {user} is subscribing to: ')
    when = input('When did the user subscribe? Please enter a timestamp (format: YYYY-MM-DD HH:MM:SS) if you would'
                 ' like to specify a time. Otherwise, please enter "now": ')

    # Create timestamp if the user is subscribing 'now'
    if when == 'now':
        when = datetime.datetime.now()
        when = when.strftime('%Y-%m-%d %H:%M:%S')

    # Build query
    sql = (f'INSERT INTO SubscribesToPodcast (email, podcastName, timestamp) VALUES '
           f'("{user}", "{podcast}", "{when}");')

    # Get connection
    conn, cur = db.Database().connect_to_MariaDB()

    # Try to add subscriber
    try:

        # Transaction for insert
        cur.execute('START TRANSACTION;')
        cur.execute(sql)
        cur.execute('COMMIT;')

        # Confirmation
        print(f'{user} has successfully subscribed to {podcast} at {when}!')

        # Close connection
        conn.close()

    # Error handling, rollback transaction, close connection
    except mariadb.Error as e:
        print(f'There was an error adding subscriber: {e}')
        cur.execute('ROLLBACK;')
        conn.close()


def unsubscribe_from_podcast():
    """
    Part of the update_podcast_subscribers flow. This function builds and executes a delete statement if a user chooses
    to unsubscribe from a podcast.

    :return: No data objects returned. Prints a confirmation if unsubscribe is successful or an error message otherwise.
    """

    # Get input info
    user = input('Please enter the email of the user unsubscribing: ')
    podcast = input(f'Please enter the name of the podcast that {user} is unsubscribing from: ')

    # Find the timestamp for the subscription to complete the key
    timestamp_sql = (f'SELECT * FROM SubscribesToPodcast WHERE email="{user}" AND podcastName="{podcast}";')

    # Connect to db
    conn, cur = db.Database().connect_to_MariaDB()

    # Get subscriber result
    result = pd.read_sql(timestamp_sql, conn)

    # Check length of result, get timestamp if there is a subscriber record
    if len(result.index) == 0:
        print(f'It does not appear that {user} was subscribed to {podcast}...\n')
        conn.close()
        valid_result = False

    # Grab the final key element if the given user is subscribed to the given podcast
    else:
        when = result.loc[0, 'timestamp']
        valid_result = True

    # If there is a subscriber...
    if valid_result:
        # Build query
        sql = (f'DELETE FROM SubscribesToPodcast WHERE email="{user}" AND podcastName="{podcast}" '
               f'AND timestamp="{when}";')

        # Try to execute query
        try:
            # Delete transaction
            cur.execute('START TRANSACTION;')
            cur.execute(sql)
            cur.execute('COMMIT;')

            # Confirm and close connection
            print(f'{user} successfully unsubscribed from {podcast}! \n')
            conn.close()

        # Catch and print errors, close connection
        except mariadb.Error as e:
            print(f'There was an error unsubscribing: {e}')
            conn.close()


def get_bulk_subscriber_inputs():
    """
    Input handler for bulk addition of podcast subscribers.
    :return: input data for bulk_add_podcast_subscribers() function
    """

    podcast = input('Please enter the podcast you would like to bulk add subscribers to: ')
    n = input(f'Please enter the number of subscribers you would like to add to {podcast}: ')
    month = input('Please enter the month (Format: YYYY-MM) you would like to add the subscribers in: ')

    return podcast, month, n


def bulk_add_podcast_subscribers(podcast, month, n_records):
    """
    Function to conduct random bulk addition of podcast subscribers to SubscribesToPodcast relation.

    :param: podcast -- specified podcast for adding subscribers to
    :param: month -- month for the inserts
    :param: n -- number of inserts

    :return: nothing returned, adds specified number of records to podcast and prints confirmation.
    """

    # Get connection
    conn, cur = db.Database().connect_to_MariaDB()

    # Pull table of users
    user_sql = ('SELECT * FROM User;')
    users = pd.read_sql(user_sql, conn)
    n_users = len(users.index)

    # Get existing subscribers to avoid duplication
    sub_sql = (f'SELECT email, podcastName FROM SubscribesToPodcast WHERE podcastName="{podcast}";')
    subs = pd.read_sql(sub_sql, conn)
    subs = list(subs.itertuples(index=False, name=None))
    print(subs)

    # Check if there are enough users not subscribed to complete the operation
    n_subs = len(subs)
    n_free = n_users - n_subs
    if n_free < int(n_records):
        print('There are not enough users in the database to carry out this operation. Please reduce the number of '
              'subscribers you are adding, or create more users with generateUsers.')
        conn.close()
        return None

    # Generate entries
    t1 = time()
    inserts = []
    check_inserts = []
    while len(inserts) < int(n_records):
        # Build random timestamp
        timestamp = generate_random_timestamp(month)

        # Choose random user email
        user_ind = random.randint(0, n_users - 1)
        email = users.loc[user_ind, 'email']

        # Build check tuple
        check = (email, podcast)

        if check in check_inserts:
            pass

        if check in subs:
            pass

        # Build final tuple if the keys aren't already present in the db
        else:
            record = (email, podcast, timestamp)
            check_inserts.append(check)
            inserts.append(record)

    t2 = time()

    print(f'It took {t2 - t1} seconds to randomly generate {n_records} records.')

    # Insert records into table
    try:
        sql = ("INSERT INTO SubscribesToPodcast (email, podcastName, timestamp) "
               "VALUES (%s, %s, %s)")
        t1 = time()

        if len(inserts) < 1000:
            cur.execute('START TRANSACTION;')
            cur.executemany(sql, inserts)
            cur.execute('COMMIT;')

        else:
            while len(inserts) > 1000:
                chunk = inserts[:1000]
                inserts = inserts[1000:]
                cur.execute('START TRANSACTION;')
                cur.executemany(sql, chunk)
                cur.execute('COMMIT;')

            if len(inserts) > 0:
                cur.execute('START TRANSACTION;')
                cur.executemany(sql, inserts)
                cur.execute('COMMIT;')

        t2 = time()
        print(f'{n_records} random records inserted into ListensToPodcastEpisode in {t2 - t1} seconds.')

        conn.close()

    except mariadb.Error as e:
        print(f'Error inserting random records: {e}')
        cur.execute('ROLLBACK;')

        conn.close()


def get_bulk_unsubscribe_inputs():
    """
    Gathers data to bulk unsubscribe from a podcast.
    :return: data to feed to bulk_unsubscribe_from_podcast()
    """

    podcast = input('Please enter the name of the podcast you would like to remove subscribers from: ')
    n = input(f'Please enter the number of subscribers you would like to remove from {podcast}: ')

    return podcast, n


def bulk_unsubscribe_from_podcast(podcast, n_records):
    """
    Manages bulk deletes from the SubscribesToPodcast relation for a given podcast.

    :param podcast: podcast to remove subscribers from
    :param n_records: number of subscribers to remove.
    :return: no data object returned, but modifies database and prints a confirmation.
    """

    # Get db connection
    conn, cur = db.Database().connect_to_MariaDB()

    # Get current podcast subscribers
    sub_sql = (f'SELECT email, podcastName FROM SubscribesToPodcast WHERE podcastName="{podcast}"')
    subs_result = pd.read_sql(sub_sql, conn)

    # Check number of subscribers against number of records to be deleted. Special logic if more records to be deleted
    # than exist
    n_subs = len(subs_result.index)
    if int(n_records) > n_subs:
        choice = input(f'The number of records to be deleted ({n_records}) is greater than the current number of '
                       f'subscribers ({n_subs}). Would you like to delete all subscribers? (Y/N) ').upper()

        # If delete all, then execute deletion and break from function
        if choice == 'Y':
            sql = (f'DELETE FROM SubscribesToPodcast WHERE podcastName="{podcast}";')

            # Attempt transaction
            try:
                cur.execute('START TRANSACTION;')
                cur.execute(sql)
                cur.execute('COMMIT;')

                conn.close()
                return None

            # Break if it fails
            except mariadb.Error as e:
                print(f'There was an error carrying out the deletions: {e}')

                conn.close()
                return None

        # Reassign the number of deletions if user does not want to delete them all
        else:
            n_records = input(f'Please enter a number of records you would like to delete that is less than {n_subs}: ')

    # Randomly select entries to delete based on subscriber dataframe index
    deletion_inds = []

    while len(deletion_inds) < int(n_records):
        ind = random.randint(0, n_subs - 1)
        if ind in deletion_inds:
            pass
        else:
            deletion_inds.append(ind)

    # Build deletion tuples
    deletions = []

    for item in deletion_inds:
        record = (subs_result.loc[item, 'email'], subs_result.loc[item, 'podcastName'])
        deletions.append(record)

    # Build sql query
    sql = (f'DELETE FROM SubscribesToPodcast WHERE email=%s and podcastName=%s;')

    # Attempt deletions
    try:
        cur.execute('START TRANSACTION;')
        cur.executemany(sql, deletions)
        cur.execute('COMMIT;')

        print(f'{n_records} users successfully unsubscribed from {podcast}!')
        conn.close()

    # Handle error
    except mariadb.Error as e:
        print(f'Error with bulk unsubscribe: {e}')
        conn.close()


def update_podcast_subscribers():
    """
    This is a wrapper function for the three previous functions (show_podcast_subscribers(), subscribe_to_podcast(),
    and unsubscribe_from_podcast()). This basically allows the user to choose an option related to updating the podcast
    subscribers, and then calls the appropriate function based on the user input.

    :return: There is no data object returned by this function. The output is dependent on which of the three functions
    is called. Details for each can be found in their respective documentation.
    """
    # Display message about choosing to handle subscribers implicitly
    print('In trying to replicate the real world, we chose to calculate subscribers implicitly based on our '
          'SubscribesToPodcast relation. As such, the number cannot be updated directly. However, you can subscribe to'
          ' or unsubscribe from a podcast if you would like. \n')

    # Have the user select an option that they would like to do
    choice = int(input('Please enter the number corresponding to the option you prefer: '
                       '\n  1) See number of subscribers for a podcast. '
                       '\n  2) Subscribe to a podcast. '
                       '\n  3) Unsubscribe from a podcast. '
                       '\n  4) Bulk add subscribers to a podcast. '
                       '\n  5) Bulk remove subscribers from a podcast. \n'))

    # Make appropriate function call based on user choice.
    if choice == 1:
        show_podcast_subscribers()

    elif choice == 2:
        subscribe_to_podcast()

    elif choice == 3:
        unsubscribe_from_podcast()

    elif choice == 4:
        podcast, month, n = get_bulk_subscriber_inputs()
        bulk_add_podcast_subscribers(podcast, month, n)

    elif choice == 5:
        podcast, n = get_bulk_unsubscribe_inputs()
        bulk_unsubscribe_from_podcast(podcast, n)

    else:
        print('Invalid input provided. Please try again...\n')


def show_podcast_episode_listening_count():
    """
    Gets the listening count of a podcast episode from the ListensToPodcastEpisode relation.
    :return: Does not return a data object, simply prints the output.
    """

    # Get inputs
    episode = input('Please enter the name of the podcast episode you would like to see the listening count for: ')
    podcast = input('Please enter the name of the podcast the episode is on: ')
    when = input('Please enter a month (Format: YYYY-MM) you would like to see listeners for. If you would like to '
                  'see results since inception, please enter "all": ').upper()

    # Build query based on desired time
    if when == 'ALL':
        sql = (f'SELECT podcastEpisodeTitle, COUNT(*) AS listeningCount FROM ListensToPodcastEpisode '
               f'WHERE podcastEpisodeTitle="{episode}" AND podcastName="{podcast}";')

    else:
        start = f'{when}-01'
        month = int(when[5:])
        year = when[:4]
        end = f'{year}-{month + 1}-01'

        sql = (f'SELECT podcastEpisodeTitle, COUNT(*) AS listeningCount FROM ListensToPodcastEpisode '
               f'WHERE podcastEpisodeTitle="{episode}" AND podcastName="{podcast}" AND timestamp >= "{start}" '
               f'AND timestamp < "{end}";')

    # Connect to db
    conn, cur = db.Database().connect_to_MariaDB()

    # Try to execute query
    try:
        result = pd.read_sql(sql, conn)

        print(tabulate(result, headers='keys', tablefmt='psql'))

        conn.close()

    except mariadb.Error as e:
        print(f'Error finding podcast episode listening count: {e}')
        conn.close()


def listen_to_podcast_episode():
    """
    Function to simulate listening to a podcast episode. Part of the update_podcast_episode_listener_count bundle.
    :return: No data object returned, prints output only.
    """

    # Gather inputs
    user = input('Please enter the email address of the user listening to a podcast episode: ')
    episode = input('Please enter the name of the podcast episode being listened to: ')
    podcast = input('Please enter the podcast containing the provided episode: ')
    when = input('When did the user listen? Please enter a timestamp (format: YYYY-MM-DD HH:MM:SS) if you would'
                 ' like to specify a time. Otherwise, please enter "now": ')

    # Create timestamp if the user is subscribing 'now'
    if when == 'now':
        when = datetime.datetime.now()
        when = when.strftime('%Y-%m-%d %H:%M:%S')

    # Build query
    sql = (f'INSERT INTO ListensToPodcastEpisode (userEmail, podcastEpisodeTitle, podcastName, '
           f'timestamp) VALUES ("{user}", "{episode}", "{podcast}", "{when}")')

    # Connect to DB
    conn, cur = db.Database().connect_to_MariaDB()

    # Execute
    try:
        cur.execute('START TRANSACTION;')
        cur.execute(sql)
        cur.execute('COMMIT;')

        print(f'{user} listened to {episode} from {podcast} at {when}.')
        conn.close()

    except mariadb.Error as e:
        print(f'Error listening to podcast episode: {e}')
        conn.close()


def get_bulk_podcast_listener_inputs():
    """
    Helper function to get inputs for bulk_add_podcast_episode_listeners() function
    :return: all inputs for function
    """
    # Get inputs
    episode = input('Please enter the name of the podcast episode you would like to bulk add inputs for: ')
    podcast = input('Please enter the name of the podcast containing the episode: ')
    month = input('Please enter the month you would like to add the listens to (Format: YYYY-MM): ')
    n_records = input('How many "listen to" records should be generated? ')

    return episode, podcast, month, n_records


def bulk_add_podcast_episode_listeners(episode, podcast, month, n_records):
    """
    Function to bulk fill the ListensToPodcastEpisode relation to prove database functionality.
    :return: Does not return a data object, only prints an output.
    """
    # Get connection
    conn, cur = db.Database().connect_to_MariaDB()

    # Pull table of users
    user_sql = ('SELECT * FROM User;')
    users = pd.read_sql(user_sql, conn)
    n_users = len(users.index)

    # Get existing ListensToPodcastEpisode records to avoid duplication
    episode_listens = pd.read_sql(('SELECT * FROM ListensToPodcastEpisode;'), conn)
    episode_listens = list(episode_listens.itertuples(index=False, name=None))

    t1 = time()
    inserts = []
    while len(inserts) < int(n_records):
        # Build random timestamp
        timestamp = generate_random_timestamp(month)

        # Choose random user email
        user_ind = random.randint(0, n_users - 1)
        email = users.loc[user_ind, 'email']

        # Build insert tuple
        record = (email, episode, podcast, timestamp)

        if record in inserts:
            pass

        if record in episode_listens:
            pass

        else:
            inserts.append(record)

    t2 = time()

    print(f'It took {t2 - t1} seconds to randomly generate {n_records} records.')

    # Insert records into table
    try:
        sql = ("INSERT INTO ListensToPodcastEpisode (userEmail, podcastEpisodeTitle, podcastName, timestamp) "
               "VALUES (%s, %s, %s, %s)")
        t1 = time()

        if len(inserts) < 1000:
            cur.execute('START TRANSACTION;')
            cur.executemany(sql, inserts)
            cur.execute('COMMIT;')

        else:
            while len(inserts) > 1000:
                chunk = inserts[:1000]
                inserts = inserts[1000:]
                cur.execute('START TRANSACTION;')
                cur.executemany(sql, chunk)
                cur.execute('COMMIT;')

            if len(inserts) > 0:
                cur.execute('START TRANSACTION;')
                cur.executemany(sql, inserts)
                cur.execute('COMMIT;')

        t2 = time()
        print(f'{n_records} random records inserted into ListensToPodcastEpisode in {t2 - t1} seconds.')

        conn.close()

    except mariadb.Error as e:
        print(f'Error inserting random records: {e}')
        cur.execute('ROLLBACK;')

        conn.close()


def update_podcast_episode_listener_count():
    """
        This is a wrapper function for the three previous functions (show_podcast_subscribers(), subscribe_to_podcast(),
        and unsubscribe_from_podcast()). This basically allows the user to choose an option related to updating the podcast
        episode listening count, and then calls the appropriate function based on the user input.

        :return: There is no data object returned by this function. The output is dependent on which of the three functions
        is called. Details for each can be found in their respective documentation.
        """
    # Display message about choosing to handle subscribers implicitly
    print('In trying to replicate the real world, we chose to calculate podcast episode listeners implicitly based on our '
          'ListensToPodcastEpisode relation. As such, the number cannot be updated directly. However, you can listen'
          'to a podcast if you would like. \n')

    # Have the user select an option that they would like to do
    choice = int(input('Please enter the number corresponding to the option you prefer: '
                       '\n  1) See listening count for a podcast episode. '
                       '\n  2) Listen to a podcast episode. '
                       '\n  3) Bulk add podcast episode listeners. \n'))

    # Make appropriate function call based on user choice.
    if choice == 1:
        show_podcast_episode_listening_count()

    elif choice == 2:
        listen_to_podcast_episode()

    elif choice == 3:
        episode, podcast, month, n_records = get_bulk_podcast_listener_inputs()
        bulk_add_podcast_episode_listeners(episode, podcast, month, n_records)

    else:
        print('Invalid input provided. Please try again...\n')


def main():
    # WORKING
    # update_song_play_count()
    # update_podcast_ratings()
    # find_songs_given_artist()
    # find_songs_given_album()

    # Written with the tabulate package -- looks nice
    # find_podcast_episodes_given_podcast()
    # update_artist_monthly_listeners()
    # update_podcast_subscribers()
    # bulk_add_song_listens()
    # update_podcast_episode_listener_count()
    # podcast, month, n = get_bulk_subscriber_inputs()
    # bulk_add_podcast_subscribers(podcast, month, n)
    podcast, n = get_bulk_unsubscribe_inputs()
    bulk_unsubscribe_from_podcast(podcast, n)

if __name__ == '__main__':
    main()
