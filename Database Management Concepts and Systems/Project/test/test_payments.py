"""Test operations/payments module.
"""

import unittest

from decimal import Decimal

from operations import db
import inserts
import dropTables
import test_db

from operations import payments

class Test(unittest.TestCase):
    """A general test class for all tests.
    """
    @classmethod
    def setUpClass(cls):
        """Setup the database.
        """
        test_db.createTablesWrapper()
        cls.conn, cls.cur = db.Database().connect_to_MariaDB()

    @classmethod
    def tearDownClass(cls):
        """Teardown the database.
        """
        cls.cur.close()
        cls.conn.close()
        dropTables.dropTables()

    def test_accept_one_payment(self):
        """Test accepting of a single payment.
        """
        try:
            email = 'smallfry@aol.com'
            month = 1
            year = 2023

            expected = [(email, round(Decimal(9.99), 2))]

            status, values = payments.receivePayment(userEmail=email, month=month, year=year)

            self.assertTrue(status)
            self.assertEqual(expected, values)

        except Exception as err:
            print(err)
            self.fail()

    def test_accept_all_payments(self):
        """Test accepting of all subscriber payments.
        """
        year = 2023
        month = 4

        try:
            status, values = payments.receivePayment(year=year,
                                                     month=month)

            expected = [('alexa@alexa.dev', Decimal('10.00')), ('curseWERNSTROM@planetexpress.com', Decimal('1.00')), ('cyclopsRULEZ@futuremail.net', Decimal('99.99')), ('girder_guy@planetexpress.com', Decimal('0.99')), ('johnj@johnj.dev', Decimal('10.00')), ('lonely_lobster@futuremail.net', Decimal('99.99')), ('smallfry@aol.com', Decimal('9.99'))]

            self.assertTrue(status, "Query status False...")
            self.assertEqual(expected, values)

        except Exception as err:
            print(err)
            self.fail()

    def test_pay_one_podcast_host(self):
        """Test payment for one podcast host.
        """
        podcast_show_name = inserts.podcast_vals[1][0]
        podcast_episode = inserts.podcastepisode_vals[0][1]
        year = 2023
        month = 4

        try:
            status, values = payments.payPodcastHosts(podcastName=podcast_show_name,
                                                      podcastEpisode=podcast_episode,
                                                      year=year,
                                                      month=month)

            expected = [(3, 35)]

            self.assertTrue(status)
            self.assertEqual(expected, values)

        except Exception as err:
            print(err)
            self.fail()

    def test_pay_one_podcast_host_rollback(self):
        """Test payment for non-existent podcast show.
        """
        podcast_show_name = "podcast show that does not exist"
        podcast_episode = inserts.podcastepisode_vals[0][1]
        year = 2023
        month = 4

        try:
            status, values = payments.payPodcastHosts(podcastName=podcast_show_name,
                                                      podcastEpisode=podcast_episode,
                                                      year=year,
                                                      month=month)

            self.fail()

            self.assertTrue(status)
            self.assertEqual(expected, values)

        except Exception as err:
            print(err)
            self.assertFalse(status)
            self.assertEqual([], values)

    def test_pay_all_podcast_hosts(self):
        """Test payment for all podcast hosts.
        """
        podcast_show_name = None
        podcast_episode = None
        year = 2023
        month = 4

        try:
            status, values = payments.payPodcastHosts(podcastName=podcast_show_name,
                                                      podcastEpisode=podcast_episode,
                                                      year=year,
                                                      month=month)

            expected = [(3, 35), (3, 35), (2, 40), (8, 25), (6001, 25), (6001, 25)]

            self.assertTrue(status)
            self.assertEqual(expected, values)

        except Exception as err:
            print(err)
            self.fail()

    def test_pay_royalties_for_one_song(self):
        """Test payment of royalties for a single song.
        """
        song_data = inserts.song_vals[0]
        song_title = song_data[3]
        album_name = song_data[1]
        edition = song_data[2]
        creator_id = song_data[0]
        month = 3
        year = 2023

        try:
            status, results = payments.makeSongPayment(songTitle=song_title,
                                                       albumName=album_name,
                                                       edition=edition,
                                                       creatorId=creator_id,
                                                       month=month,
                                                       year=year)

            expected = [{5: Decimal('55.22'), 6: Decimal('55.22'), 'Clouds Hill': Decimal('71.00'), 1: Decimal('55.22')}, {6: Decimal('77877.54'), 'Clouds Hill': Decimal('66752.17'), 1: Decimal('77877.54')}, {'Equal Vision': Decimal('3650.33'), 1: Decimal('8517.43')}, {6: Decimal('1682.94'), 'Sargent House': Decimal('1442.52'), 4: Decimal('1682.94')}, {1: Decimal('26603.67'), 'Sargent House': Decimal('22803.15'), 4: Decimal('26603.67')}, {'Elevate Records': Decimal('15.00'), 2001: Decimal('35.00')}, {2002: Decimal('35.00'), 'Elevate Records': Decimal('30.00'), 2001: Decimal('35.00')}, {'Melodic Avenue Music': Decimal('3.00'), 2002: Decimal('7.00')}, {'Melodic Avenue Music': Decimal('6.00'), 2002: Decimal('14.00')}]

            self.assertTrue(status)
            self.assertEqual(expected, results)

        except Exception as err:
            print(err)
            self.fail()

    def test_pay_royalties_for_all_songs(self):
        """Test payment of royalties for all songs.
        """
        song_title = None
        album_name = None
        edition = None
        creator_id = None
        month = 3
        year = 2023

        try:
            status, results = payments.makeSongPayment(songTitle=song_title,
                                                       albumName=album_name,
                                                       edition=edition,
                                                       creatorId=creator_id,
                                                       month=month,
                                                       year=year)

            expected = [{5: Decimal('55.22'), 6: Decimal('55.22'), 'Clouds Hill': Decimal('71.00'), 1: Decimal('55.22')}, {6: Decimal('77877.54'), 'Clouds Hill': Decimal('66752.17'), 1: Decimal('77877.54')}, {'Equal Vision': Decimal('3650.33'), 1: Decimal('8517.43')}, {6: Decimal('1682.94'), 'Sargent House': Decimal('1442.52'), 4: Decimal('1682.94')}, {1: Decimal('26603.67'), 'Sargent House': Decimal('22803.15'), 4: Decimal('26603.67')}, {'Elevate Records': Decimal('15.00'), 2001: Decimal('35.00')}, {2002: Decimal('35.00'), 'Elevate Records': Decimal('30.00'), 2001: Decimal('35.00')}, {'Melodic Avenue Music': Decimal('3.00'), 2002: Decimal('7.00')}, {'Melodic Avenue Music': Decimal('6.00'), 2002: Decimal('14.00')}]

            self.assertTrue(status)
            self.assertEqual(expected, results)

        except Exception as err:
            print(err)
            self.fail()

if __name__ == '__main__':
    unittest.main()
