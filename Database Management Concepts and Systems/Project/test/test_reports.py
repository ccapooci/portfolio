"""Test reports module.
"""

import unittest

import dropTables
from test import test_db
from operations import reports
from operations import db
from decimal import Decimal
import datetime

class Test(unittest.TestCase):
    """A general test class for all tests.
    """
    @classmethod
    def setUpClass(cls):
        """Setup the database.
        """

    @classmethod
    def tearDownClass(cls):
        """Teardown the database.
        """


    def test_monthly_play_count_song(self):
        """Test monthly play count for a song input.
        """
        with self.subTest():
            try:

                #################################################

                song_title = "Electric Dreamscape" 
                month = 1
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                expected = [(10, )]

                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:

                #################################################
                
                song_title = "Electric Dreamscape" 
                month = 2
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                expected = [(20, )]

                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Electric Dreamscape" 
                month = 3
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                expected = [(30, )]

                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Electric Dreamscape" 
                month = 4
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                expected = [(500, )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Midnight Mirage" 
                month = 1
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                expected = [(100, )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Midnight Mirage" 
                month = 2
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                expected = [(200, )]
                
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Midnight Mirage" 
                month = 3
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                expected = [(300, )]
                
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Midnight Mirage" 
                month = 4
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                expected = [((1000), )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Echoes of You" 
                month = 1
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                expected = [((1000), )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Echoes of You" 
                month = 2
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                expected = [((2000), )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Echoes of You" 
                month = 3
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                expected = [((3000), )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Echoes of You" 
                month = 4
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                expected = [((100), )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Rainy Nights" 
                month = 1
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                expected = [((10000), )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Rainy Nights" 
                month = 2
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                expected = [((20000), )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Rainy Nights" 
                month = 3
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                expected = [((30000), )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                
                song_title = "Rainy Nights" 
                month = 4
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                expected = [((200), )]
                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                #################################################
                # Bad query
                song_title = "Rain Nights" 
                month = 1
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                expected = [((0), )]

                status, values = reports.sql_calculate_monthly_play_count_song(song_title, creator_id, album_name, edition, month, year)

                self.assertTrue(status)
                self.assertEqual(expected, values)

            except Exception as err:
                print(err)
                self.fail()

    def test_monthly_play_count_album(self):
        """Test monthly play with album input.
        """

        with self.subTest():
            try:
                ###################################################
                month = 1
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                status, values = reports.sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year)
                expected = [(110, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 2
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                status, values = reports.sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year)
                expected = [(220, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 3
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                status, values = reports.sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year)
                expected = [(330, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 4
                year = 2023
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"

                status, values = reports.sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year)
                expected = [(1500, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 1
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                status, values = reports.sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year)
                expected = [(11000, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 2
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                status, values = reports.sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year)
                expected = [(22000, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 3
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                status, values = reports.sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year)
                expected = [(33000, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 4
                year = 2023
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"

                status, values = reports.sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year)
                expected = [(300, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 1
                year = 2023
                creator_id = 2002
                album_name = "Lost Echoes"
                edition = "Standard"

                status, values = reports.sql_calculate_monthly_play_count_album(album_name, edition, creator_id, month, year)
                expected = [(0, )]

                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)

            except Exception as err:
                print(err)
                self.fail()

    def test_monthly_play_count_artist(self):
        """Test monthly play count for artist input.
        """

        with self.subTest():
            try:
                ###################################################
                month = 1
                year = 2023
                creator_id = 2001

                status, values = reports.sql_calculate_monthly_play_count_artist(creator_id, month, year)
                expected = [(110, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 2
                year = 2023
                creator_id = 2001

                status, values = reports.sql_calculate_monthly_play_count_artist(creator_id, month, year)
                expected = [(220, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 3
                year = 2023
                creator_id = 2001

                status, values = reports.sql_calculate_monthly_play_count_artist(creator_id, month, year)
                expected = [(330, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 4
                year = 2023
                creator_id = 2001

                status, values = reports.sql_calculate_monthly_play_count_artist(creator_id, month, year)
                expected = [(1500, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 1
                year = 2023
                creator_id = 2002

                status, values = reports.sql_calculate_monthly_play_count_artist(creator_id, month, year)
                expected = [(11000, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 2
                year = 2023
                creator_id = 2002

                status, values = reports.sql_calculate_monthly_play_count_artist(creator_id, month, year)
                expected = [(22000, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 3
                year = 2023
                creator_id = 2002

                status, values = reports.sql_calculate_monthly_play_count_artist(creator_id, month, year)
                expected = [(33000, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 4
                year = 2023
                creator_id = 2002

                status, values = reports.sql_calculate_monthly_play_count_artist(creator_id, month, year)
                expected = [(300, )]
                
                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###################################################
                month = 1
                year = 2023
                creator_id = 20012

                status, values = reports.sql_calculate_monthly_play_count_artist(creator_id, month, year)
                expected = [(0, )]

                self.assertTrue(status, "Query status False...")
                self.assertEqual(expected, values)            

            except Exception as err:
                print(err)
                self.fail()

    def test_host_payment_time_period(self):
        """Test host payment for a given time period.
        """
        with self.subTest():
            try:

                ###########################################################
                creator_id = 6001
                start_date = '2023-01-01'
                stop_date = '2023-02-01'

                status, values = reports.sql_calculate_total_payment_to_host_per_time_period(creator_id, start_date, stop_date)
                expected = [(round(Decimal(20), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                creator_id = 6001
                start_date = '2023-02-01'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_host_per_time_period(creator_id, start_date, stop_date)
                expected = [(round(Decimal(70), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                creator_id = 6001
                start_date = '2023-01-01'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_host_per_time_period(creator_id, start_date, stop_date)
                expected = [(round(Decimal(90), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                creator_id = 6001
                start_date = '2024-01-01'
                stop_date = '2024-02-01'

                status, values = reports.sql_calculate_total_payment_to_host_per_time_period(creator_id, start_date, stop_date)
                expected = [(round(Decimal(0), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)

            except Exception as err:
                print(err)
                self.fail()

    def test_artist_payment_time_period(self):
        """Test artist payment for a given time period.
        """
        with self.subTest():
            try:
                ###########################################################
                creator_id = 2001
                start_date = '2023-01-01'
                stop_date = '2023-02-01'

                status, values = reports.sql_calculate_total_payment_to_artist_per_time_period(creator_id, start_date, stop_date)
                expected = [((round(Decimal(4.2), 2)),)]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                creator_id = 2001
                start_date = '2023-2-1'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_artist_per_time_period(creator_id, start_date, stop_date)
                expected = [(round(Decimal(21), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                creator_id = 2001
                start_date = '2023-01-01'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_artist_per_time_period(creator_id, start_date, stop_date)
                expected = [(round(Decimal(25.2), 2),)]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                creator_id = 2002
                start_date = '2023-01-01'
                stop_date = '2023-02-01'

                status, values = reports.sql_calculate_total_payment_to_artist_per_time_period(creator_id, start_date, stop_date)
                expected = [(round(Decimal(703.5), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                creator_id = 2002
                start_date = '2023-02-01'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_artist_per_time_period(creator_id, start_date, stop_date)
                expected = [(round(Decimal(3867.5), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                creator_id = 2002
                start_date = '2023-01-01'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_artist_per_time_period(creator_id, start_date, stop_date)
                expected = [(round(Decimal(4571), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                creator_id = 2002
                start_date = '2024-01-01'
                stop_date = '2024-02-01'

                status, values = reports.sql_calculate_total_payment_to_artist_per_time_period(creator_id, start_date, stop_date)
                expected = [(round(Decimal(0), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)

            except Exception as err:
                print(err)
                self.fail()

    def test_record_label_payment_time_period(self):
        """Test record label payment for a given time period.
        """
        with self.subTest():
            try:
                ###########################################################
                record_label_name = "Elevate Records"
                start_date = '2023-01-01'
                stop_date = '2023-02-01'

                status, values = reports.sql_calculate_total_payment_to_record_label_per_time_period(record_label_name, start_date, stop_date)
                expected = [(round(Decimal(3.3), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                record_label_name = "Elevate Records"
                start_date = '2023-2-1'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_record_label_per_time_period(record_label_name, start_date, stop_date)
                expected = [(round(Decimal(16.5), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                record_label_name = "Elevate Records"
                start_date = '2023-01-01'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_record_label_per_time_period(record_label_name, start_date, stop_date)
                expected = [(round(Decimal(19.8), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                record_label_name = "Melodic Avenue Music"
                start_date = '2023-01-01'
                stop_date = '2023-02-01'

                status, values = reports.sql_calculate_total_payment_to_record_label_per_time_period(record_label_name, start_date, stop_date)
                expected = [(round(Decimal(330), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                record_label_name = "Melodic Avenue Music"
                start_date = '2023-2-1'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_record_label_per_time_period(record_label_name, start_date, stop_date)
                expected = [(round(Decimal(1650), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                record_label_name = "Melodic Avenue Music"
                start_date = '2023-01-01'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_record_label_per_time_period(record_label_name, start_date, stop_date)
                expected = [(round(Decimal(1980), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                record_label_name = "Elevate Recor"
                start_date = '2023-01-01'
                stop_date = '2023-04-01'

                status, values = reports.sql_calculate_total_payment_to_record_label_per_time_period(record_label_name, start_date, stop_date)
                expected = [(round(Decimal(0), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)

            except Exception as err:
                print(err)
                self.fail()


    def test_total_revenue_month(self):
        """Test total revenue for a given month.
        """
        with self.subTest():
            try:
                ###########################################################
                month = 1
                year = 2023

                status, values = reports.sql_calculate_total_revenue_per_month(month, year)
                expected = [(round(Decimal(1111), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                month = 2
                year = 2023

                status, values = reports.sql_calculate_total_revenue_per_month(month, year)
                expected = [(round(Decimal(2222), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                month = 3
                year = 2023

                status, values = reports.sql_calculate_total_revenue_per_month(month, year)
                expected = [(round(Decimal(3333), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                month = 4
                year = 2023

                status, values = reports.sql_calculate_total_revenue_per_month(month, year)
                expected = [(round(Decimal(123000), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                month = 5
                year = 2023

                status, values = reports.sql_calculate_total_revenue_per_month(month, year)
                expected = [(round(Decimal(0), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)

            except Exception as err:
                print(err)
                self.fail()

    def test_total_revenue_year(self):
        """Test total revenue given year.
        """
        with self.subTest():
            try:

                ###########################################################
                year = 2023

                status, values = reports.sql_calculate_total_revenue_per_year(year)
                expected = [(round(Decimal(129666), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)
            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:
                ###########################################################
                year = 2024

                status, values = reports.sql_calculate_total_revenue_per_year(year)
                expected = [(round(Decimal(0), 2), )]

                self.assertTrue(status)
                self.assertEqual(expected, values)

            except Exception as err:
                print(err)
                self.fail()

    
    def test_report_songs_artist(self):
        """ Test reporting songs given artist.
        """
        creator_id = None

        with self.subTest():
            try:            
                creator_id = 2001
                status, results = reports.sql_report_songs_artist(creator_id)
                # demo data
                expected = [[1001, 'Electric Dreamscape', 2001, 'Electric Oasis', 'Standard', 500, Decimal('0.10'), None, False], [1002, 'Midnight Mirage', 2001, 'Electric Oasis', 'Standard', 1000, Decimal('0.10'), 2002, False]]
                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:            
                creator_id = 2002
                status, results = reports.sql_report_songs_artist(creator_id)
                #demo data
                expected = [[1003, 'Echoes of You', 2002, 'Lost in the Echoes', 'Standard', 100, Decimal('0.10'), None, False], [1004, 'Rainy Nights', 2002, 'Lost in the Echoes', 'Standard', 200, Decimal('0.10'), None, False]]

                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:            
                creator_id = 1999
                status, results = reports.sql_report_songs_artist(creator_id)
                expected = []

                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()


    def test_report_songs_album(self):       
        """ Test reporting songs given album.
        """
        with self.subTest():
            try:            
                album_name = "Electric Oasis"
                edition = "Standard"
                status, results = reports.sql_report_songs_album(album_name, edition)
                # demo data
                expected = [[1001, 'Electric Dreamscape', 2001, 'Electric Oasis', 'Standard', 500, Decimal('0.10'), None, False], [1002, 'Midnight Mirage', 2001, 'Electric Oasis', 'Standard', 1000, Decimal('0.10'), 2002, False]]

                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:            
                album_name = "Lost in the Echoes"
                edition = "Standard"
                status, results = reports.sql_report_songs_album(album_name, edition)
                #demo data
                expected = [[1003, 'Echoes of You', 2002, 'Lost in the Echoes', 'Standard', 100, Decimal('0.10'), None, False], [1004, 'Rainy Nights', 2002, 'Lost in the Echoes', 'Standard', 200, Decimal('0.10'), None, False]]

                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:            
                album_name = "Lost echos"
                edition = "Standard"
                status, results = reports.sql_report_songs_album(album_name, edition)
                expected = []

                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()

    
    def test_report_songs_album_and_artist(self):       
        """Test reporting songs given album and artist.
        """
        with self.subTest():
            try:            
                creator_id = 2001
                album_name = "Electric Oasis"
                edition = "Standard"
                status, results = reports.sql_report_songs_album_and_artist(album_name, edition, creator_id)
                # demo data
                expected = [[1001, 'Electric Dreamscape', 2001, 'Electric Oasis', 'Standard', 500, Decimal('0.10'), None, False], [1002, 'Midnight Mirage', 2001, 'Electric Oasis', 'Standard', 1000, Decimal('0.10'), 2002, False]]

                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:            
                creator_id = 2002
                album_name = "Lost in the Echoes"
                edition = "Standard"
                status, results = reports.sql_report_songs_album_and_artist(album_name, edition, creator_id)
                #demo data
                expected = [[1003, 'Echoes of You', 2002, 'Lost in the Echoes', 'Standard', 100, Decimal('0.10'), None, False], [1004, 'Rainy Nights', 2002, 'Lost in the Echoes', 'Standard', 200, Decimal('0.10'), None, False]]

                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:            
                album_name = "Electric Oasis"
                edition = "Standard"
                creator_id = 2002
                status, results = reports.sql_report_songs_album_and_artist(album_name, edition, creator_id)
                expected = []

                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()

    def test_report_podcast_episodes(self):
        """Test reporting podcast episodes given podcast."""
        with self.subTest():
            try:            
                podcast_name = "Mind Over Matter: Exploring the Power of the Human Mind"
                status, results = reports.sql_report_podcasts_epsiodes(podcast_name)
                expected = [[7003,'Ep 3', 'Mind Over Matter: Exploring the Power of the Human Mind', None, 0, 30], [7004,'Ep 4', 'Mind Over Matter: Exploring the Power of the Human Mind', None, 0, 40], [7005, 'Ep 5', 'Mind Over Matter: Exploring the Power of the Human Mind', None, 0, 50], [7001, 'The Science of Mindfulness', 'Mind Over Matter: Exploring the Power of the Human Mind', None, 0, 100], [7002, 'Unlocking Your Potential', 'Mind Over Matter: Exploring the Power of the Human Mind', None, 0, 200]]

                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()

        with self.subTest():
            try:            
                podcast_name = "Brain Over Matter"
                status, results = reports.sql_report_podcasts_epsiodes(podcast_name)
                expected = []

                self.assertTrue(status)
                self.assertEqual(expected, results)

            except Exception as err:
                print(err)
                self.fail()


if __name__ == '__main__':
    unittest.main()
