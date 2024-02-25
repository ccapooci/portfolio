"""Module for payment operations and associated API functions.

Payment operations include royalty payments for songs, payments from
subscribers, and payments for podcasts.
"""
from datetime import date, datetime
from decimal import Decimal
from re import match

import main
from operations import db

_PODCAST_BASE_AMOUNT = Decimal(20.00)
_PODCAST_BONUS = Decimal(5.00)

_SONG_ARTISTS_SHARE = Decimal(0.7)
_SONG_RECORD_LABEL_SHARE = Decimal(0.3)

def _get_new_payment_id(cur):
    """Get a new payment ID

    Args:
        cur: cursor to use for the query.

    Returns:
        New payment ID.
    """
    cur.execute("SELECT MAX(paymentId) FROM Payment;")
    val = cur.fetchall()[0][0]

    if val is None:
        val = 0
    else:
        val = val + 1

    return val

def _input_special(prompt):
    """Input but with empty or whitespace strings replaced by None.

    Args:
        prompt: prompt to present to user

    Returns:
        None if a whitespace or empty string else the string provided.
    """
    response = input(prompt)
    if match("^\W*$", response):
        return None

    return response

def _pay_for_song(songTitle, albumName, edition, creatorId, month, year, cur):
    """Helper method that pays for single song.

    Args:
        songTitle: name of the song
        albumName: name of the album
        edition: edition of the album
        creatorId: ID of the creator of the song
        month: month for the payment
        year: for the payment

    Returns:
      Amount paid to each party in a list.
    """
    payment_date = date(year, month, day=1)

    # get play count, royalty rate, and record label for song
    cur.execute(f"SELECT playCount, royaltyRate, recordLabelName  FROM Song natural join Owns WHERE creatorId = '{creatorId}' AND albumName = '{albumName}' AND edition = '{edition}' AND songTitle = '{songTitle}';")

    results = cur.fetchall()[0]

    play_count = results[0]
    royalty_rate = results[1]
    record_label = results[2]

    # get just the ids of the artists that will be paid
    cur.execute(f"SELECT guestArtistId FROM CollaboratesOn WHERE creatorId = '{creatorId}' AND albumName = '{albumName}' AND edition = '{edition}' AND songTitle = '{songTitle}';")

    # create a list of guest artist ids
    guest_artist_results = [id_[0] for id_ in cur.fetchall()]

    total_artists = len(guest_artist_results) + 1
    artists_value = round(royalty_rate * play_count * _SONG_ARTISTS_SHARE / (total_artists), 2)
    record_label_value = round(royalty_rate * play_count * _SONG_RECORD_LABEL_SHARE, 2)

    # pay record label
    payment_id_record_label = _get_new_payment_id(cur)

    cur.execute(f"INSERT INTO Payment(paymentId, date, value) values({payment_id_record_label}, '{payment_date}', {record_label_value});")
    cur.execute(f"INSERT INTO PayToRecordLabel(recordLabelName, paymentId) values('{record_label}', {payment_id_record_label});")

    # pay primary artist
    payment_id_artist = _get_new_payment_id(cur)

    cur.execute(f"INSERT Payment(paymentId, date, value) values({payment_id_artist}, '{payment_date}', {artists_value});")
    cur.execute(f"INSERT into PayToContentCreator(creatorId, paymentId) values({creatorId}, {payment_id_artist});")

    # pay guest artists
    for guest_artist in guest_artist_results:
        payment_id = _get_new_payment_id(cur)

        cur.execute(f"INSERT Payment(paymentId, date, value) values({payment_id}, '2023-04-02', {artists_value});")
        cur.execute(f"INSERT into PayToContentCreator(creatorId, paymentId) values({guest_artist}, {payment_id});")

    cur.execute(f"UPDATE Song set royaltyPaidStatus = 1 WHERE creatorId = '{creatorId}' AND albumName = '{albumName}' AND edition = '{edition}' AND songTitle = '{songTitle}';")

    main.print_debug(f"Payment processed {songTitle}, {albumName}, {edition}, {creatorId}...")

    payee_information = {key: artists_value for key in guest_artist_results}
    payee_information[record_label] = record_label_value
    payee_information[creatorId] = artists_value

    return payee_information

def make_song_payment_interactive():
    """Prompt user for song payment details.

    Returns:
        Status indicating if the operation was successful and list of
        payment information.
    """
    song_title = _input_special("Name of the song: ")
    album_name = _input_special("Name of the album: ")
    edition = _input_special("Edition of the album: ")
    creator_id = _input_special("Id of the creator of the song: ")
    month = _input_special("Month for the payment: ")
    year = _input_special("Year for the payment: ")

    if not month:
        month = datetime.now().month

    if not year:
        year = datetime.now().year

    month = int(month)
    year = int(year)

    status, results = makeSongPayment(song_title,
                                      album_name,
                                      edition,
                                      creator_id,
                                      month,
                                      year)

    return status, results

def makeSongPayment(songTitle, albumName, edition, creatorId, month, year):
    """Make payment for one song or all songs.

    Return confirmation and amount paid to each party.  If None passed
    for attributes other than month and year, payment is generated for
    all songs.

    Args:
        songTitle: name of the song
        albumName: name of the album
        edition: edition of the album
        creatorId: ID of the creator of the song
        month: month for the payment
        year: for the payment

    Returns:
        True if operation was successful and amount paid to each party
        in a list.
        False if the operation fails and an empty list.
    """
    conn, cur = db.Database().connect_to_MariaDB()

    try:
        if not all([songTitle, albumName, edition, creatorId]):
            payee_information = []

            # get play count, royalty rate, and record label for songs
            cur.execute(f"SELECT songTitle, albumName, edition, creatorId, playCount, royaltyRate, recordLabelName  FROM Song natural join Owns;")

            results = cur.fetchall()

            for song_data in results:
                payee_information.append(_pay_for_song(songTitle=song_data[0],
                                                       albumName=song_data[1],
                                                       edition=song_data[2],
                                                       creatorId=song_data[3],
                                                       month=month,
                                                       year=year,
                                                       cur=cur))

        else:
            payee_information = [_pay_for_song(songTitle=songTitle,
                                               albumName=albumName,
                                               edition=edition,
                                               creatorId=creatorId,
                                               month=month,
                                               year=year,
                                               cur=cur)]

    except IndexError:
        main.print_debug(f"No song found...")
        return False, []

    else:
        conn.commit()
        return True, payee_information

    finally:
        cur.close()
        conn.close()

def receive_payment_interactive():
    """Prompt user for subscriber payment.

    Returns:
        Status indicating if the operation was successful and list of
        payment information.
    """
    user_email = _input_special("User email: ")
    month = _input_special("Month for the payment: ")
    year = _input_special("Year for the payment: ")

    if not month:
        month = datetime.now().month

    if not year:
        year = datetime.now().year

    month = int(month)
    year = int(year)

    status, results = receivePayment(userEmail=user_email,
                                     year=year,
                                     month=month)
    return status, results

def receivePayment(userEmail=None, month=None, year=None):
    """Take payment from subscriber or all subscribers.

    If None passed for userEmail, payment received from all users.

    Args:
        userEmail: describes email to receive payment for
        month: describes month for which to receive payment
        year: describes year for which to recieve payment

    Returns:
        True if successfully processed and amount paid by subscribers
        in a list.
        False if the operation fails and an empty list.
    """
    conn, cur = db.Database().connect_to_MariaDB()

    payment_date = date(year, month, day=1)

    try:
        if not userEmail:

            cur.execute(f"SELECT email, subscriptionFee FROM User WHERE statusOfSubscription = 'A';")
            payor_information = cur.fetchall()

            for payorInfo in payor_information:
                email, value = payorInfo[0], round(payorInfo[1], 2)

                payment_id = _get_new_payment_id(cur)

                cur.execute(f"INSERT into Payment(paymentId, date, value) values({payment_id}, '{payment_date}', {value});")

                cur.execute(f"INSERT into PayFromUser (paymentId, userEmail) values({payment_id}, '{email}');")

            main.print_debug(f"Payment processed for all users...")

        else:
            payment_id = _get_new_payment_id(cur)

            cur.execute(f"SELECT subscriptionFee FROM User WHERE email = '{userEmail}' AND statusOfSubscription = 'A';")
            value = cur.fetchall()[0][0]
            values = [value]

            cur.execute(f"INSERT into Payment(paymentId, date, value) values({payment_id}, '{payment_date}', {value});")

            cur.execute(f"INSERT into PayFromUser (paymentId, userEmail) values({payment_id}, '{userEmail}');")

            payor_information = [(userEmail, value)]

            main.print_debug(f"Payment processed for {userEmail}...")

    except IndexError:
        main.print_debug(f"No subscriber found...")
        return False, []

    else:
        conn.commit()
        return True, payor_information

    finally:
        cur.close()
        conn.close()

def pay_podcast_hosts_interactive():
    """Prompt user for paying podcast hosts.

    Returns:
        Status indicating if the operation was successful and list of
        payment information.
    """
    podcast_name = _input_special("Name of podcast show: ")
    podcast_episode = _input_special("Name of podcast episode: ")
    month = _input_special("Month for the payment: ")
    year = _input_special("Year for the payment: ")

    if not month:
        month = datetime.now().month

    if not year:
        year = datetime.now().year

    month = int(month)
    year = int(year)

    status, results = payPodcastHosts(podcastEpisode=podcast_episode,
                                      podcastName=podcast_name,
                                      month=month,
                                      year=year)

    return status, results

def payPodcastHosts(podcastEpisode=None, podcastName=None, month=None, year=None):
    """Pay podcast host for an episode or process all payments.

    If None is passed for podcastEpisode and podcastName, payment
    generated for all podcastEpisodes.

    If the podcast data query fails the transaction is rolled back.

    Args:
        podcastEpisode: name of the podcast episode
        podcastName: name of the podcast show under which episodes are
            recorded
        month: month to register the payment under
        year: year to register the payment under

    Returns:
        True if operation was successful and amount paid to each party
        in a list.
        False if the operation fails and an empty list.
    """
    conn, cur = db.Database().connect_to_MariaDB()

    payment_date = date(year=year, month=month, day=1)

    try:
        if not all([podcastEpisode, podcastName]):
            cur.execute('START TRANSACTION;')

            cur.execute(f"SELECT creatorId, {_PODCAST_BASE_AMOUNT} + {_PODCAST_BONUS} * advertisementCount FROM Hosts NATURAL JOIN Podcast NATURAL JOIN PodcastEpisode;")
            result = cur.fetchall()

            for result_ in result:
                creator_id = result_[0]
                value = result_[1]

                payment_id = _get_new_payment_id(cur)

                cur.execute(f"INSERT Payment(paymentId, date, value) values({payment_id}, '{payment_date}', {value});")
                cur.execute(f"INSERT into PayToContentCreator(paymentId, creatorId) values({payment_id}, {creator_id});")

            main.print_debug(f"Payment processed for all creator IDs...")

        else:

            cur.execute('START TRANSACTION;')
            cur.execute(f"SELECT creatorId, {_PODCAST_BASE_AMOUNT} + {_PODCAST_BONUS} * advertisementCount FROM Hosts NATURAL JOIN Podcast NATURAL JOIN PodcastEpisode WHERE podcastName = '{podcastName}' AND title = '{podcastEpisode}';")

            result_ = cur.fetchall()[0]
            result = [result_]
            creator_id = result_[0]
            value = result_[1]

            payment_id = _get_new_payment_id(cur)

            cur.execute(f"INSERT Payment(paymentId, date, value) values({payment_id}, '{payment_date}', {value});")
            cur.execute(f"INSERT into PayToContentCreator(paymentId, creatorId) values({payment_id}, {creator_id});")

            main.print_debug(f"Payment processed for creator ID: {creator_id}...")

    except IndexError:
        main.print_debug(f"No podcast data found...")
        cur.execute('ROLLBACK;')
        return False, []

    else:
        cur.execute('COMMIT;')
        return True, result

    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    pass
