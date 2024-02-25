from operations import db
import mariadb
import datetime as dt
import time

start = time.time()

creator_sql = ("INSERT INTO ContentCreator (creatorId, firstName, lastName) VALUES (%s, %s, %s);")

creator_vals = [
    (2001, "Forest", None),
    (2002, "Rain", None),
    (6001, "Matthew", "Wilson")
]

user_sql = ("INSERT INTO User (UID, email, firstName, lastName, subscriptionFee, statusOfSubscription, phone, registrationDate)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")
user_vals = [
    (8001, 'alexa@alexa.dev', 'Alex', 'A', 10.0, 'A', '(259) 444-8294', dt.date(3001, 12, 2)),
    (8002, 'johnj@johnj.dev', 'John', 'J', 10.0, 'A', '(259) 444-8294', dt.date(3001, 12, 2))
]

payment_sql = ("INSERT INTO Payment (paymentId, date, value) VALUES (%s, %s, %s)")

payment_vals = [
    (6, dt.date(2023, 1, 2), 4.2),
    (7, dt.date(2023, 2, 2), 8.4),
    (8, dt.date(2023, 3, 2), 12.6),
    (9, dt.date(2023, 1, 2), 703.5),
    (10, dt.date(2023, 2, 2), 1547),
    (11, dt.date(2023, 3, 2), 2320.5),
    (12, dt.date(2023, 1, 2), 20.0),
    (13, dt.date(2023, 2, 2), 30.0),
    (14, dt.date(2023, 3, 2), 40.0),
    (15, dt.date(2023, 1, 2), 3.3),
    (16, dt.date(2023, 2, 2), 6.6),
    (17, dt.date(2023, 3, 2), 9.9),
    (18, dt.date(2023, 1, 2), 330),
    (19, dt.date(2023, 2, 2), 660),
    (20, dt.date(2023, 3, 2), 990),

    (21, dt.date(2023, 1, 2), 1111),
    (22, dt.date(2023, 2, 2), 2222),
    (23, dt.date(2023, 3, 2), 3333),
    (24, dt.date(2023, 4, 2), 123000)

]

payfromuser_sql = ("INSERT INTO PayFromUser (paymentId, userEmail) VALUES (%s, %s)")

payfromuser_vals = [
    (21, 'johnj@johnj.dev'),
    (22, 'alexa@alexa.dev'),
    (23, 'johnj@johnj.dev'),
    (24, 'alexa@alexa.dev')

]

album_sql = ("INSERT INTO Album (AID, creatorId, albumName, edition, releaseYear) VALUES (%s, %s, %s, %s, %s)")

album_vals = [
    (4001, 2001, 'Electric Oasis', 'Standard', 2000),
    (4002, 2002, 'Lost in the Echoes', 'Standard', 2000)
]

artist_sql = ("INSERT INTO Artist (creatorId, status, type, country, primaryGenre) VALUES (%s, %s, %s, %s, %s)")

artist_vals = [
    (2001, 'A', 'Band', 'United States', 'Rock' ),
    (2002, 'A', 'Band', 'United States', 'Rock' ),
]

contracts_sql = ("INSERT INTO Contracts (creatorId, recordLabelName) VALUES (%s, %s)")

contracts_vals = [
    (2001, 'Elevate Records'),
    (2002, 'Melodic Avenue Music')
]

recordlabel_sql = ("INSERT INTO RecordLabel (RID, labelName) VALUES (%s, %s)")

recordlabel_vals = [
    (3001, 'Elevate Records'),
    (3002, 'Melodic Avenue Music')
]

podcasthost_sql = ("INSERT INTO PodcastHost (creatorId, email, phone, city) VALUES (%s, %s, %s, %s)")

podcasthost_vals = [
    (6001, 'matt.wilson@mindovermatter.com', '(111) 111-1111', None)
]

hosts_sql = ("INSERT INTO Hosts (podcastName, creatorId) VALUES (%s, %s)")

hosts_vals = [
    ('Mind Over Matter: Exploring the Power of the Human Mind', 6001)
]

podcast_sql = ("INSERT INTO Podcast (PID, podcastName, language, country, rating) VALUES (%s, %s, %s, %s, %s)")

podcast_vals = [
    (5001, 'Mind Over Matter: Exploring the Power of the Human Mind', 'English', 'United States', 4.5)

]

podcastepisode_sql = ("INSERT INTO PodcastEpisode (PEID, title, podcastName, duration, releaseDate, advertisementCount) "
                      "VALUES (%s, %s, %s, %s, %s, %s)")

podcastepisode_vals = [
    (7001, 'The Science of Mindfulness', 'Mind Over Matter: Exploring the Power of the Human Mind', 1000, dt.date(2023, 3, 8), 0),
    (7002, 'Unlocking Your Potential', 'Mind Over Matter: Exploring the Power of the Human Mind', 1500, dt.date(2023, 3, 15), 0),
    (7003, 'Ep 3', 'Mind Over Matter: Exploring the Power of the Human Mind', 1600, dt.date(2023, 3, 18), 0),
    (7004, 'Ep 4', 'Mind Over Matter: Exploring the Power of the Human Mind', 1700, dt.date(2023, 3, 21), 0),
    (7005, 'Ep 5', 'Mind Over Matter: Exploring the Power of the Human Mind', 1800, dt.date(2023, 3, 24), 0)
]

listenstopodcastepisode_sql = ("INSERT INTO ListensToPodcastEpisode (userEmail, podcastEpisodeTitle, podcastName, "
                               "timestamp) VALUES (%s, %s, %s, %s)")

listenstopodcastepisode_vals = [
]

subscribestopodcast_sql = ("INSERT INTO SubscribesToPodcast (email, podcastName, timestamp) VALUES (%s, %s, %s)")

subscribestopodcast_vals = [
]

song_sql = ("INSERT INTO Song (SID, creatorId, albumName, edition, songTitle, trackNumber, duration, playCount, releaseDate, releaseCountry, language, royaltyPaidStatus, royaltyRate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

song_vals = [
    (1001, 2001, 'Electric Oasis', "Standard", "Electric Dreamscape", 1, 255, 500, '2023-05-07', "US", "English", False, 0.1),
    (1002, 2001, 'Electric Oasis', "Standard", "Midnight Mirage", 2, 255, 1000, '2023-05-07', "US", "English", False, 0.1),
    (1003, 2002, 'Lost in the Echoes', "Standard", "Echoes of You", 1, 255, 100, '2023-05-07', "US", "English", False, 0.1),
    (1004, 2002, 'Lost in the Echoes', "Standard", "Rainy Nights", 2, 255, 200, '2023-05-07', "US", "English", False, 0.1)
]

listentosong_sql = ("INSERT INTO ListensToSong (email, songTitle, creatorId, albumName, edition, timestamp) VALUES (%s, %s, %s, %s, %s, %s)")

listentosong_vals = [
]
paytocontentcreator_sql = ("INSERT INTO PayToContentCreator (creatorId, paymentId) VALUES (%s, %s)")

paytocontentcreator_vals = [
    (2001, 6),
    (2001, 7),
    (2001, 8),
    (2002, 9),
    (2002, 10),
    (2002, 11),
    (6001, 12),
    (6001, 13),
    (6001, 14)

]

paytorecordlabel_sql = ("INSERT INTO PayToRecordLabel (paymentId, recordLabelName) VALUES (%s, %s)")

paytorecordlabel_vals = [
    (15, "Elevate Records"),
    (16, "Elevate Records"),
    (17, "Elevate Records"),
    (18, "Melodic Avenue Music"),
    (19, "Melodic Avenue Music"),
    (20, "Melodic Avenue Music")
]

collaborateson_sql = ("INSERT INTO CollaboratesOn (creatorId, guestArtistId, songTitle, albumName, edition) VALUES (%s, %s, %s, %s, %s)")

collaborateson_vals = [
    (2001, 2002, "Midnight Mirage", "Electric Oasis", "Standard")
]

owns_sql = ("INSERT INTO Owns (creatorId, recordLabelName, songTitle, albumName, edition) VALUES (%s, %s, %s, %s, %s)")

owns_vals = [
    (2001, "Elevate Records", "Electric Dreamscape", "Electric Oasis", "Standard"),
    (2001, "Elevate Records", "Midnight Mirage", "Electric Oasis", "Standard"),
    (2002, "Melodic Avenue Music", "Echoes of You", "Lost in the Echoes", "Standard"),
    (2002, "Melodic Avenue Music", "Rainy Nights", "Lost in the Echoes", "Standard")
]

sponsor_sql = ("INSERT INTO Sponsor (sponsorName) VALUES (%s)")

sponsor_vals = [
    ["General Motors"],
    ["Ford"],
    ["Dewalt"],
    ["Nike"],
    ["Adidas"]
]

sponsors_sql = ("INSERT INTO Sponsors (podcastName, sponsorName) VALUES (%s, %s)")

sponsors_vals = [

]

podcast_genre_sql = ("INSERT INTO PodcastGenre (genreName) VALUES (%s)")

podcast_genre_vals = [
    ("Tech",),
    ("Comedy",),
    ("Business",),
    ("Self Improvement",),
    ("Sports",),
    ("Mystery",),
    ("News",)
]

describes_podcast_sql = ("INSERT INTO DescribesPodcast (podcastName, genreName) VALUES (%s, %s)")

describes_podcast_vals = [

]

special_guest_sql = ("INSERT INTO SpecialGuest (creatorId) VALUES (%s)")

special_guest_vals = [

]

guest_stars_sql = ("INSERT INTO GuestStars (creatorId, title, podcastName) VALUES (%s, %s, %s)")

guest_stars_vals = [
]

inserts = {
    'creator': [creator_sql, creator_vals],
    'user': [user_sql, user_vals],
    'artist': [artist_sql, artist_vals],
    'album': [album_sql, album_vals],
    'song': [song_sql, song_vals],
    'collaborates_on': [collaborateson_sql, collaborateson_vals],
    'record_label': [recordlabel_sql, recordlabel_vals],
    'contracts': [contracts_sql, contracts_vals],
    'owns': [owns_sql, owns_vals],
    'podcast_host': [podcasthost_sql, podcasthost_vals],
    'podcast': [podcast_sql, podcast_vals],
    'hosts': [hosts_sql, hosts_vals],
    'sponsor': [sponsor_sql, sponsor_vals],
    #'sponsors': [sponsors_sql, sponsors_vals],
    'podcast_episode': [podcastepisode_sql, podcastepisode_vals],
    'podcast_genre': [podcast_genre_sql, podcast_genre_vals],
    #'describes_podcast': [describes_podcast_sql, describes_podcast_vals],
    #'guest_stars': [guest_stars_sql, guest_stars_vals],
    #'special_guest': [special_guest_sql, special_guest_vals],
    #'subscribes_to_podcast': [subscribestopodcast_sql, subscribestopodcast_vals],
    #'listens_to_podcast_episode': [listenstopodcastepisode_sql, listenstopodcastepisode_vals],
    #listen_to_song': [listentosong_sql, listentosong_vals],
    'payment': [payment_sql, payment_vals],
    'pay_to_content_creator': [paytocontentcreator_sql, paytocontentcreator_vals],
    'pay_to_record_label': [paytorecordlabel_sql, paytorecordlabel_vals],
    'pay_from_user': [payfromuser_sql, payfromuser_vals],
 }

def main():
    conn, cur = db.Database().connect_to_MariaDB()

    try:
        conn.auto_reconnect = True
        # TODO: Test below queries
        # for item in podcast_genre_vals:
        #     cur.execute(podcast_genre_sql, item)
        #
        # for item in describes_podcast_vals:
        #     cur.execute(describes_podcast_sql, item)
        #
        # for item in special_guest_vals:
        #     cur.execute(special_guest_sql, item)
        #
        # for item in guest_stars_vals:
        #     cur.execute(guest_stars_sql, item)

        for key, value in inserts.items():
            #for item in value[1]:
            cur.executemany(value[0], value[1])


        # cur.execute(sponsors_sql, sponsors_vals[0])
        # cur.execute(sponsors_sql, sponsors_vals[1])
        # cur.execute(sponsors_sql, sponsors_vals[2])
        # cur.execute(sponsors_sql, sponsors_vals[3])
        # cur.execute(sponsors_sql, sponsors_vals[4])

        conn.commit()

        print('Tables populated with sample data.')

        # cur.execute("SELECT * FROM SubscribesToPodcast;")
        # result = cur.fetchall()
        # for x in result:
        #     print(x)

        #cur.execute("SELECT * FROM SubscribesToPodcast;")
        #result = cur.fetchall()
        #for x in result:
        #    print(x)

        end = time.time()

        print(end-start)

        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        conn.close()

if __name__ == '__main__':
    main()
