import mariadb
import datetime as dt

from operations import db

creator_sql = ("INSERT INTO ContentCreator (creatorId, firstName, lastName) VALUES (%s, %s, %s);")

creator_vals = [
    (1, 'The Mars Volta', None),
    (2, 'Lex', 'Fridman'),
    (3, 'Joe', 'Rogan'),
    (4, 'The Fall of Troy', None),
    (5, 'Mac Miller', None),
    (6, 'TTNG', None),
    (7, 'Tim', 'Ferriss'),
    (8, 'Leila', 'Fadel'), 
    (2001, "Forest", None),
    (2002, "Rain", None),
    (6001, "Matthew", "Wilson")
]

user_sql = ("INSERT INTO User (email, firstName, lastName, subscriptionFee, statusOfSubscription, phone, registrationDate)"
            " VALUES (%s, %s, %s, %s, %s, %s, %s);")
user_vals = [
    ('smallfry@aol.com', 'Philip', 'Fry', 9.99, 'A', '(555) 123-4567', dt.date(1999, 5, 22)),
    ('cyclopsRULEZ@futuremail.net', 'Turanga', 'Leela', 99.99, 'A', None, dt.date(3001, 12, 1)),
    ('girder_guy@planetexpress.com', 'Bender', 'Rodriguez', 0.99, 'A', '(999) 635-6889', dt.date(2994, 4, 21)),
    ('curseWERNSTROM@planetexpress.com', 'Hubert', 'Farnsworth', 1.00, 'A', None, dt.date(2902, 7, 18)),
    ('bigbadbureaucrat@planetexpress.com', 'Hermes', 'Conrad', 0, 'I', None, dt.date(3000, 1, 1)),
    ('lonely_lobster@futuremail.net', 'John', 'Zoidberg', 99.99, 'A', '(259) 444-8294', dt.date(3001, 12, 2)),
    ('alexa@alexa.dev', 'Alex', 'A', 10.0, 'A', '(259) 444-8294', dt.date(3001, 12, 2)),
    ('johnj@johnj.dev', 'John', 'J', 10.0, 'A', '(259) 444-8294', dt.date(3001, 12, 2))
]

payment_sql = ("INSERT INTO Payment (paymentId, date, value) VALUES (%s, %s, %s)")

payment_vals = [
    (1, dt.date(3001, 3, 1), 99.99),
    (2, dt.date(3001, 4, 1), 99.99),
    (3, dt.date(3001, 5, 1), 99.99),
    (4, dt.date(3001, 6, 1), 99.99),
    (5, dt.date(3001, 7, 1), 99.99),
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
    (20, dt.date(2023, 3, 2), 990)
]

payfromuser_sql = ("INSERT INTO PayFromUser (paymentId, userEmail) VALUES (%s, %s)")

payfromuser_vals = [
    (1, 'lonely_lobster@futuremail.net'),
    (2, 'lonely_lobster@futuremail.net'),
    (3, 'cyclopsRULEZ@futuremail.net'),
    (4, 'lonely_lobster@futuremail.net'),
    (5, 'cyclopsRULEZ@futuremail.net')
]

album_sql = ("INSERT INTO Album (creatorId, albumName, edition, releaseYear) VALUES (%s, %s, %s, %s)")

album_vals = [
    (1, 'De-Loused in the Comatorium', 'Standard', 2003),
    (1, 'Amputechture', 'Standard', 2006),
    (1, 'The Bedlam in Goliath', 'Standard', 2008),
    (4, 'Doppelganger', 'Standard', 2003),
    (4, 'Manipulator', 'Standard', 2007),
    (4, 'Phantom on the Horizon', 'Standard', 2008),
    (2001, 'Electric Oasis', 'Standard', 2000),
    (2002, 'Lost in the Echoes', 'Standard', 2000)
]

artist_sql = ("INSERT INTO Artist (creatorId, status, type, country, primaryGenre) VALUES (%s, %s, %s, %s, %s)")

artist_vals = [
    (1, 'A', 'Band', 'United States', 'Progressive Rock'),
    (4, 'A', 'Band', 'United States', 'Mathcore'),
    (5, 'I', 'Musician', 'United States', 'Hip Hop'),
    (6, 'A', 'Band', 'England', 'Math rock' ),
    (2001, 'A', 'Band', 'United States', 'Rock' ),
    (2002, 'A', 'Band', 'United States', 'Rock' ),   
]

contracts_sql = ("INSERT INTO Contracts (creatorId, recordLabelName) VALUES (%s, %s)")

contracts_vals = [
    (1, 'Clouds Hill'),
    (4, 'Equal Vision'),
    (5, 'Rostrum'),
    (6, 'Sargent House'),
    (2001, 'Elevate Records'),
    (2002, 'Melodic Avenue Music')
]

recordlabel_sql = ("INSERT INTO RecordLabel (labelName) VALUES (%s)")

recordlabel_vals = [
    ['Clouds Hill'],
    ['Equal Vision'],
    ['Rostrum'],
    ['Sargent House'],
    ['Elevate Records'],
    ['Melodic Avenue Music']
]

podcasthost_sql = ("INSERT INTO PodcastHost (creatorId, email, phone, city) VALUES (%s, %s, %s, %s)")

podcasthost_vals = [
    (2, None, '(123) 456-7890', 'Boston'),
    (3, None, None, None),
    (7, 'timmy_f@4hours.com', None, 'East Hampton'),
    (8, 'leila_fadel@npr.org', '(999) 999-9999', None),
    (6001, 'matt.wilson@mindovermatter.com', '(111) 111-1111', None)
]

hosts_sql = ("INSERT INTO Hosts (podcastName, creatorId) VALUES (%s, %s)")

hosts_vals = [
    ('Lex Fridman Podcast', 2),
    ('The Joe Rogan Experience', 3),
    ('The Tim Ferriss Show', 7),
    ('Up First', 8),
    ('Mind Over Matter: Exploring the Power of the Human Mind', 6001)
]

podcast_sql = ("INSERT INTO Podcast (podcastName, language, country, rating) VALUES (%s, %s, %s, %s)")

podcast_vals = [
    ('Lex Fridman Podcast', 'English', 'United States', 4.9),
    ('The Joe Rogan Experience', 'English', 'United States', 4.8),
    ('The Tim Ferriss Show', 'English', 'United States', 4.9),
    ('Up First', 'English', 'United States', 4.8),
    ('Mind Over Matter: Exploring the Power of the Human Mind', 'English', 'United States', 4.5)

]

podcastepisode_sql = ("INSERT INTO PodcastEpisode (title, podcastName, duration, releaseDate, advertisementCount) "
                      "VALUES (%s, %s, %s, %s, %s)")

podcastepisode_vals = [
    ('#1952 - Michael Malice', 'The Joe Rogan Experience', 12540, dt.date(2023, 3, 8), 3),
    ('#1951 - Coffeezilla', 'The Joe Rogan Experience', 11100, dt.date(2023, 3, 7), 3),
    ('#284 - Saifedean Ammous: Bitcoin, Anarchy, and Austrian Economics', 'Lex Fridman Podcast', 14280, dt.date(2022, 5, 11), 4),
    ('Florida Legislative Session, Powell Testimony, French Strikes', 'Up First', 840, dt.date(2023, 3, 7), 1), 
    ('The Science of Mindfulness', 'Mind Over Matter: Exploring the Power of the Human Mind', 1000, dt.date(2023, 3, 8), 1),
    ('Unlocking Your Potential', 'Mind Over Matter: Exploring the Power of the Human Mind', 1500, dt.date(2023, 3, 15), 1)
]

listenstopodcastepisode_sql = ("INSERT INTO ListensToPodcastEpisode (userEmail, podcastEpisodeTitle, podcastName, "
                               "timestamp) VALUES (%s, %s, %s, %s)")

listenstopodcastepisode_vals = [
    ('lonely_lobster@futuremail.net', '#1951 - Coffeezilla', 'The Joe Rogan Experience', dt.datetime.now()),
    ('cyclopsRULEZ@futuremail.net', 'Florida Legislative Session, Powell Testimony, French Strikes', 'Up First', dt.datetime.now()),
    ('curseWERNSTROM@planetexpress.com', '#284 - Saifedean Ammous: Bitcoin, Anarchy, and Austrian Economics', 'Lex Fridman Podcast', dt.datetime.now()),
    ('girder_guy@planetexpress.com', '#1952 - Michael Malice', 'The Joe Rogan Experience', dt.datetime.now())
]

subscribestopodcast_sql = ("INSERT INTO SubscribesToPodcast (email, podcastName, timestamp) VALUES (%s, %s, %s)")

subscribestopodcast_vals = [
    ('girder_guy@planetexpress.com', 'The Joe Rogan Experience', dt.datetime.now()),
    ('cyclopsRULEZ@futuremail.net', 'Up First', dt.datetime.now()),
    ('curseWERNSTROM@planetexpress.com', 'Lex Fridman Podcast', dt.datetime.now()),
    ('smallfry@aol.com', 'The Joe Rogan Experience', dt.datetime.now())
]

song_sql = ("INSERT INTO Song (creatorId, albumName, edition, songTitle, trackNumber, duration, playCount, releaseDate, releaseCountry, language, royaltyPaidStatus, royaltyRate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

song_vals = [
    (1, 'Amputechture', "Standard", "Title 1", 1, 439, 1029, '2023-01-12', "US", "English", False, 0.23),
    (1, 'Amputechture', "Standard", "Title 2", 2, 200, 890029, '2023-01-12', "US", "English", False, 0.25),
    (1, 'Amputechture', "Standard", "Title 3", 3,  250, 50699, '2023-01-12', "US", "English", False, 0.24),
    (1, 'Amputechture', "Standard", "Title 4", 4, 280, 4600, '2023-01-12', "US", "English", False, 0.10),
    (4, 'Doppelganger', "Standard", "Title a", 1, 310, 60105, '2023-05-07', "US", "English", True, 0.08),
    (4, 'Doppelganger', "Standard", "Title b", 2, 320, 323105, '2023-02-12', "US", "English", True, 0.27),
    (4, 'Doppelganger', "Standard", "Title c", 3, 270, 69105, '2023-05-07', "US", "English", True, 0.07),
    (4, 'Doppelganger', "Standard", "Title d", 4, 250, 760105, '2023-05-07', "US", "English", True, 0.10),
    (4, 'Doppelganger', "Standard", "Title e", 5, 255, 160105, '2023-05-07', "US", "English", True, 0.12),

    (2001, 'Electric Oasis', "Standard", "Electric Dreamscape", 1, 255, 500, '2023-05-07', "US", "English", False, 0.1),
    (2001, 'Electric Oasis', "Standard", "Midnight Mirage", 2, 255, 1000, '2023-05-07', "US", "English", False, 0.1),
    (2002, 'Lost in the Echoes', "Standard", "Echoes of You", 1, 255, 100, '2023-05-07', "US", "English", False, 0.1),
    (2002, 'Lost in the Echoes', "Standard", "Rainy Nights", 2, 255, 200, '2023-05-07', "US", "English", False, 0.1)
]

listentosong_sql = ("INSERT INTO ListensToSong (email, songTitle, creatorId, albumName, edition, timestamp) VALUES (%s, %s, %s, %s, %s, %s)")

listentosong_vals = [
    ('smallfry@aol.com', 'Title 1', 1, 'Amputechture', "Standard", "2011-02-11 00:00:00"),
    ('smallfry@aol.com', "Title 2", 1,  'Amputechture', "Standard", "2011-02-11 00:03:00"),
    ("curseWERNSTROM@planetexpress.com", 'Title 1', 1, 'Amputechture', "Standard", "2011-02-11 00:00:00"),
    ("curseWERNSTROM@planetexpress.com", "Title 4", 1, 'Amputechture', "Standard", "2011-02-11 00:00:00"),
    ("cyclopsRULEZ@futuremail.net", "Title a", 4, 'Doppelganger', "Standard", "2011-02-11 00:00:00"),
    ("cyclopsRULEZ@futuremail.net", "Title a", 4, 'Doppelganger', "Standard", "2011-02-11 00:03:00"),
    ("cyclopsRULEZ@futuremail.net", "Title d", 4, 'Doppelganger', "Standard", "2011-02-11 00:00:00"),
    ('smallfry@aol.com', "Title a", 4, 'Doppelganger', "Standard", "2011-02-11 00:00:00"),
    ('smallfry@aol.com', "Title c", 4, 'Doppelganger', "Standard", "2011-02-11 00:00:00")
]

paytocontentcreator_sql = ("INSERT INTO PayToContentCreator (creatorId, paymentId) VALUES (%s, %s)")

paytocontentcreator_vals = [
    (1, 1),
    (1, 2),
    (6, 3),
    (7, 4),
    (8, 5),
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
    (1, "Clouds Hill"),
    (2, "Clouds Hill"),
    (3, "Equal Vision"),
    (4, "Rostrum"),
    (5, "Equal Vision"),
    (15, "Elevate Records"),
    (16, "Elevate Records"),
    (17, "Elevate Records"),
    (18, "Melodic Avenue Music"),
    (19, "Melodic Avenue Music"),
    (20, "Melodic Avenue Music")
]

collaborateson_sql = ("INSERT INTO CollaboratesOn (creatorId, guestArtistId, songTitle, albumName, edition) VALUES (%s, %s, %s, %s, %s)")

collaborateson_vals = [
    (1, 5, "Title 1", "Amputechture", "Standard"),
    (1, 6, "Title 1", "Amputechture", "Standard"),
    (1, 6, "Title 2", "Amputechture", "Standard"),
    (4, 1, "Title d", "Doppelganger", "Standard"),
    (4, 6, "Title a", "Doppelganger", "Standard"),
    (2001, 2002, "Midnight Mirage", "Electric Oasis", "Standard")
]

owns_sql = ("INSERT INTO Owns (creatorId, recordLabelName, songTitle, albumName, edition) VALUES (%s, %s, %s, %s, %s)")

owns_vals = [
    (1, "Clouds Hill", "Title 1", "Amputechture", "Standard"),
    (1, "Clouds Hill", "Title 2", "Amputechture", "Standard"),
    (1, "Equal Vision", "Title 3", "Amputechture", "Standard"),
    (4, "Sargent House", "Title d", "Doppelganger", "Standard"),
    (4, "Sargent House", "Title a", "Doppelganger", "Standard"),
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
    ("The Joe Rogan Experience", "General Motors"),
    ("The Joe Rogan Experience", "Ford"),
    ("The Joe Rogan Experience", "Dewalt"),
    ("Lex Fridman Podcast", "Ford"),
    ("Lex Fridman Podcast", "Adidas")
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
    ("Lex Fridman Podcast", "Self Improvement"),
    ("The Joe Rogan Experience", "Comedy"),
    ("The Tim Ferriss Show", "Business"),
    ("Up First", "News")
]

special_guest_sql = ("INSERT INTO SpecialGuest (creatorId) VALUES (%s)")

special_guest_vals = [
    (2,),
    (3,),
    (5,),
    (7,),
    (8,)
]

guest_stars_sql = ("INSERT INTO GuestStars (creatorId, title, podcastName) VALUES (%s, %s, %s)")

guest_stars_vals = [
    (5, "#1951 - Coffeezilla", "The Joe Rogan Experience"),
    (2, "#1952 - Michael Malice", "The Joe Rogan Experience"),
    (7, "Florida Legislative Session, Powell Testimony, French Strikes", "Up First")
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
    'sponsors': [sponsors_sql, sponsors_vals],
    'podcast_episode': [podcastepisode_sql, podcastepisode_vals],
    'podcast_genre': [podcast_genre_sql, podcast_genre_vals],
    'describes_podcast': [describes_podcast_sql, describes_podcast_vals],
    'guest_stars': [guest_stars_sql, guest_stars_vals],
    'special_guest': [special_guest_sql, special_guest_vals],
    'subscribes_to_podcast': [subscribestopodcast_sql, subscribestopodcast_vals],
    'listens_to_podcast_episode': [listenstopodcastepisode_sql, listenstopodcastepisode_vals],
    'listen_to_song': [listentosong_sql, listentosong_vals],
    'payment': [payment_sql, payment_vals],
    'pay_to_content_creator': [paytocontentcreator_sql, paytocontentcreator_vals],
    'pay_to_record_label': [paytorecordlabel_sql, paytorecordlabel_vals],
    'pay_from_user': [payfromuser_sql, payfromuser_vals],
}

def main():
    conn, cur = db.Database().connect_to_MariaDB()

    try:
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
            for item in value[1]:
                cur.execute(value[0], item)


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

        cur.execute("SELECT * FROM SubscribesToPodcast;")
        result = cur.fetchall()
        for x in result:
            print(x)

        cur.close()
        conn.close()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        conn.close()

if __name__ == '__main__':
    main()
