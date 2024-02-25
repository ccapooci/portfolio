import unittest

from operations import db
import dropTables
import test_db
from operations.informationProcessing.album import create_album_helper, update_album_helper, delete_album_helper
from operations.informationProcessing.artist import create_artist_helper, update_artist_helper, delete_artist_helper
from operations.informationProcessing.podcast import create_podcast_helper, update_podcast_helper, delete_podcast_helper
from operations.informationProcessing.podcastEpisode import create_podcast_episode_helper, \
    update_podcast_episode_helper, delete_podcast_episode_helper
from operations.informationProcessing.podcastHost import create_podcast_host_helper, update_podcast_host_helper, \
    delete_podcast_host_helper
from operations.informationProcessing.recordLabel import create_record_label_helper, update_record_label_helper, \
    delete_record_label_helper, assign_record_label_to_song_helper, update_contracted_artist_helper
from operations.informationProcessing.song import create_song_helper, update_song_helper, delete_song_helper, \
    enter_collaboration_info_helper
from operations.informationProcessing.user import create_user_helper, update_user_helper, delete_user_helper


class InformationProcessingTests(unittest.TestCase):

    @classmethod
    def setUp(cls):
        test_db.createTablesWrapper()
        cls.conn, cls.cur = db.Database().connect_to_MariaDB()

    @classmethod
    def tearDown(cls):
        cls.cur.close()
        cls.conn.close()
        dropTables.dropTables()

    def test_create_song(self):
        try:

            InformationProcessingTests.cur.execute("SELECT * FROM Song;")

            original_count = len(InformationProcessingTests.cur.fetchall())

            create_song_helper(content_creator_id=4, album_title="Manipulator", edition="Standard",
                               song_title="test_song", track_number=10, duration=30, play_count=4,
                               release_date="2020-01-01", country="USA", language="English",
                               royalty_paid_status=False, royalty_rate=0.55)

            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM Song;")

            new_count = len(InformationProcessingTests.cur.fetchall())

            self.assertEqual(original_count + 1, new_count)

            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_update_song(self):
        try:
            InformationProcessingTests.cur.execute("SELECT * FROM Song WHERE songTitle='Title 1';")
            royalty_paid_status = InformationProcessingTests.cur.fetchall()[0][11]

            self.assertEqual(False, royalty_paid_status)

            update_song_helper(field_name="royaltyPaidStatus", field_value="true", content_creator_id=1,
                               album_title="Amputechture", edition="Standard", song_title="Title 1")
            #
            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM Song WHERE songTitle='Title 1';")
            royalty_paid_status = InformationProcessingTests.cur.fetchall()[0][11]

            self.assertEqual(True, royalty_paid_status)
            #
            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_delete_song(self):
        InformationProcessingTests.cur.execute("SELECT * FROM Song;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        delete_song_helper(content_creator_id=1, album_title="Amputechture", edition="Standard", song_title="Title 1")

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM Song;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count - 1, new_count)

    def test_enter_collaboration_info(self):
        InformationProcessingTests.cur.execute("SELECT * FROM CollaboratesOn;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        enter_collaboration_info_helper(content_creator_id_one=1, content_creator_id_two=4, song_title="Title 1",
                                        album_title="Amputechture", edition="Standard")

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM CollaboratesOn;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count + 1, new_count)

    def test_create_user(self):
        try:

            InformationProcessingTests.cur.execute("SELECT * FROM User;")

            original_count = len(InformationProcessingTests.cur.fetchall())

            create_user_helper(email="test1@email.com", first_name="Spongebob", last_name="Squarepants",
                               subscription_fee=100, subscription_status="A", phone="9191234567",
                               registration_date="2020-01-01")

            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM User;")

            new_count = len(InformationProcessingTests.cur.fetchall())

            self.assertEqual(original_count + 1, new_count)

            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_update_user(self):
        try:
            InformationProcessingTests.cur.execute("SELECT * FROM User WHERE email='smallfry@aol.com';")
            current_email = InformationProcessingTests.cur.fetchall()[0][1]

            self.assertEqual("smallfry@aol.com", current_email)

            update_user_helper(field_name="email", field_value="'sf@gmail.com'", email='smallfry@aol.com')
            #
            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM User WHERE email='smallfry@aol.com';")
            self.assertEqual(0, len(InformationProcessingTests.cur.fetchall()))

            InformationProcessingTests.cur.execute("SELECT * FROM User WHERE email='sf@gmail.com';")
            self.assertEqual(1, len(InformationProcessingTests.cur.fetchall()))

            #
            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_delete_user(self):
        InformationProcessingTests.cur.execute("SELECT * FROM User;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        delete_user_helper(email='smallfry@aol.com')

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM User;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count - 1, new_count)

    def test_create_album(self):
        try:

            InformationProcessingTests.cur.execute("SELECT * FROM Album;")

            original_count = len(InformationProcessingTests.cur.fetchall())

            create_album_helper(content_creator_id=4, album_title="Ghost Stories", edition="Limited", release_year=2014)

            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM Album;")

            new_count = len(InformationProcessingTests.cur.fetchall())

            self.assertEqual(original_count + 1, new_count)

            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_update_album(self):
        try:
            InformationProcessingTests.cur.execute("SELECT * FROM Album WHERE albumName='Manipulator';")
            release_year = InformationProcessingTests.cur.fetchall()[0][4]

            self.assertEqual(2007, release_year)

            update_album_helper(field_name="releaseYear", field_value=2014, content_creator_id=4,
                                album_title="Manipulator", edition="Standard")
            #
            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM Album WHERE albumName='Manipulator';")
            release_year = InformationProcessingTests.cur.fetchall()[0][4]

            self.assertEqual(2014, release_year)
            #
            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_delete_album(self):
        InformationProcessingTests.cur.execute("SELECT * FROM Album;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        delete_album_helper(content_creator_id=4, album_title="Manipulator", edition="Standard")

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM Album;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count - 1, new_count)

    def test_create_artist(self):
        try:

            InformationProcessingTests.cur.execute("SELECT * FROM Artist;")

            original_count = len(InformationProcessingTests.cur.fetchall())

            create_artist_helper(content_creator_id=2, subscription_status="A", artist_type="Band",
                                 country="USA", genre="Rap")

            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM Artist;")

            new_count = len(InformationProcessingTests.cur.fetchall())

            self.assertEqual(original_count + 1, new_count)

            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_update_artist(self):
        try:
            InformationProcessingTests.cur.execute("SELECT * FROM Artist WHERE creatorId=1;")
            artist_type = InformationProcessingTests.cur.fetchall()[0][2]

            self.assertEqual("Band", artist_type)

            update_artist_helper(field_name="type", field_value="'solo artist'", content_creator_id=1)

            InformationProcessingTests.conn.commit()
            #
            InformationProcessingTests.cur.execute("SELECT * FROM Artist WHERE creatorId=1;")
            artist_type = InformationProcessingTests.cur.fetchall()[0][2]

            self.assertEqual("solo artist", artist_type)
            #
            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_delete_artist(self):
        InformationProcessingTests.cur.execute("SELECT * FROM Artist;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        delete_artist_helper(content_creator_id=1)

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM Artist;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count - 1, new_count)

    def test_create_podcast(self):
        try:

            InformationProcessingTests.cur.execute("SELECT * FROM Podcast;")

            original_count = len(InformationProcessingTests.cur.fetchall())

            create_podcast_helper(podcast_name="Waveform Podcast", language="English", country="USA", rating=4.9)

            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM Podcast;")

            new_count = len(InformationProcessingTests.cur.fetchall())

            self.assertEqual(original_count + 1, new_count)

            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_update_podcast(self):
        try:
            InformationProcessingTests.cur.execute("SELECT * FROM Podcast WHERE podcastName='Up First';")
            language = InformationProcessingTests.cur.fetchall()[0][2]

            self.assertEqual("English", language)

            update_podcast_helper(field_name="language", field_value="'Korean'", podcast_name="Up First")

            InformationProcessingTests.conn.commit()
            #
            InformationProcessingTests.cur.execute("SELECT * FROM Podcast WHERE podcastName='Up First';")
            language = InformationProcessingTests.cur.fetchall()[0][2]

            self.assertEqual("Korean", language)
            #
            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_delete_podcast(self):
        InformationProcessingTests.cur.execute("SELECT * FROM Podcast;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        delete_podcast_helper(podcast_name="Up First")

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM Podcast;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count - 1, new_count)

    def test_create_podcast_host(self):
        try:

            InformationProcessingTests.cur.execute("SELECT * FROM PodcastHost;")

            original_count = len(InformationProcessingTests.cur.fetchall())

            create_podcast_host_helper(content_creator_id=4, email="podcastman@email.com",
                                       phone_number="12345", city="NC")

            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM PodcastHost;")

            new_count = len(InformationProcessingTests.cur.fetchall())

            self.assertEqual(original_count + 1, new_count)

            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_update_podcast_host(self):
        try:
            InformationProcessingTests.cur.execute("SELECT * FROM PodcastHost WHERE creatorId=7;")
            city = InformationProcessingTests.cur.fetchall()[0][3]

            self.assertEqual("East Hampton", city)

            update_podcast_host_helper(field_name="city", field_value="'Raleigh'", content_creator_id=7)

            InformationProcessingTests.conn.commit()
            #
            InformationProcessingTests.cur.execute("SELECT * FROM PodcastHost WHERE creatorId=7;")
            city = InformationProcessingTests.cur.fetchall()[0][3]

            self.assertEqual("Raleigh", city)
            #
            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_delete_podcast_host(self):
        InformationProcessingTests.cur.execute("SELECT * FROM PodcastHost;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        delete_podcast_host_helper(content_creator_id=2)

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM PodcastHost;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count - 1, new_count)

    def test_create_podcast_episode(self):
        try:

            InformationProcessingTests.cur.execute("SELECT * FROM PodcastEpisode;")

            original_count = len(InformationProcessingTests.cur.fetchall())

            create_podcast_episode_helper(title="A funny episode", podcast_name="The Joe Rogan Experience",
                                          duration=60, release_date="2020-01-31", advertisement_count=2)

            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM PodcastEpisode;")

            new_count = len(InformationProcessingTests.cur.fetchall())

            self.assertEqual(original_count + 1, new_count)

            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_update_podcast_episode(self):
        try:
            InformationProcessingTests.cur.execute("SELECT * FROM PodcastEpisode WHERE title="
                                                   "'#1952 - Michael Malice';")
            advertisement_count = InformationProcessingTests.cur.fetchall()[0][5]

            self.assertEqual(3, advertisement_count)

            update_podcast_episode_helper(field_name="advertisementCount", field_value="'100'",
                                          podcast_name="The Joe Rogan Experience", title="#1952 - Michael Malice")

            InformationProcessingTests.conn.commit()
            #
            InformationProcessingTests.cur.execute("SELECT * FROM PodcastEpisode WHERE title="
                                                   "'#1952 - Michael Malice';")
            advertisement_count = InformationProcessingTests.cur.fetchall()[0][5]

            self.assertEqual(100, advertisement_count)
            #
            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_delete_podcast_episode(self):
        InformationProcessingTests.cur.execute("SELECT * FROM PodcastEpisode;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        delete_podcast_episode_helper(podcast_name="The Joe Rogan Experience", title="#1951 - Coffeezilla")

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM PodcastEpisode;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count - 1, new_count)

    def test_create_record_label(self):
        try:

            InformationProcessingTests.cur.execute("SELECT * FROM RecordLabel;")

            original_count = len(InformationProcessingTests.cur.fetchall())

            create_record_label_helper(label_name="Spongebob")

            InformationProcessingTests.conn.commit()

            InformationProcessingTests.cur.execute("SELECT * FROM RecordLabel;")

            new_count = len(InformationProcessingTests.cur.fetchall())

            self.assertEqual(original_count + 1, new_count)

            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_update_record_label(self):
        try:
            InformationProcessingTests.cur.execute("SELECT * FROM RecordLabel WHERE labelName='Clouds Hill';")
            label_name = InformationProcessingTests.cur.fetchall()[0][1]

            self.assertEqual("Clouds Hill", label_name)

            update_record_label_helper(label_name="Clouds Hill", new_label_name="Spongebob")

            InformationProcessingTests.conn.commit()
            #
            InformationProcessingTests.cur.execute("SELECT * FROM RecordLabel WHERE labelName='Spongebob';")

            label_name = InformationProcessingTests.cur.fetchall()[0][1]

            self.assertEqual("Spongebob", label_name)

            #
            InformationProcessingTests.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_delete_record_label(self):
        InformationProcessingTests.cur.execute("SELECT * FROM RecordLabel;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        delete_record_label_helper(label_name="Clouds Hill")

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM RecordLabel;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count - 1, new_count)

    def test_assign_record_label_to_song(self):
        InformationProcessingTests.cur.execute("SELECT * FROM Owns;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        assign_record_label_to_song_helper(label_name="Clouds Hill", content_creator_id=1,
                                           song_title='Title 4', album_title="Amputechture",
                                           edition="Standard")

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM Owns;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count + 1, new_count)

    def test_update_contracted_artist(self):
        InformationProcessingTests.cur.execute("SELECT * FROM Contracts;")

        original_count = len(InformationProcessingTests.cur.fetchall())

        update_contracted_artist_helper(content_creator_id=2, label_name="Clouds Hill")

        InformationProcessingTests.conn.commit()

        InformationProcessingTests.cur.execute("SELECT * FROM Contracts;")

        new_count = len(InformationProcessingTests.cur.fetchall())

        self.assertEqual(original_count + 1, new_count)


if __name__ == '__main__':
    unittest.main()
