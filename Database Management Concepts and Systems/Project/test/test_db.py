#!/usr/bin/env python3

import mariadb
from operations import db
import unittest
from legacySchema import inserts
import dropTables
import createTables
import main

def listsAlmostEqual(list1, list2):
    """Assert whether or not lists are almost equal.

    Compare two lists making sure that they are the same in the sense
    that each item is equal to its counterpart within two decimal
    places.

    Args:
      list1: first list to compare
      list2: second list to compare

    Returns:
      True if the lists are equal as defined within this method.
    """

    for i, j in zip(list1, list2):
        try:
            unittest.TestCase().assertAlmostEqual(i, j)

        except Exception as e:
            main.print_debug(f"Lists not equal {e}...")
            return False

    return True

def printQueries(description, queries):
    print()
    print(description)
    print()
    for q in queries:
        print(q)


def createTablesWrapper():
    dropTables.dropTables()
    createTables.createTables()
    conn, cur = db.Database().connect_to_MariaDB()

    try:

        # setup creators

        cur.executemany(inserts.creator_sql, inserts.creator_vals)

        # setup user data

        cur.executemany(inserts.user_sql, inserts.user_vals)

        # setup podcast data

        cur.executemany(inserts.podcast_genre_sql, inserts.podcast_genre_vals)
        cur.executemany(inserts.podcast_sql, inserts.podcast_vals)

        cur.executemany(inserts.podcasthost_sql, inserts.podcasthost_vals)
        cur.executemany(inserts.hosts_sql, inserts.hosts_vals)

        cur.executemany(inserts.podcastepisode_sql, inserts.podcastepisode_vals)
        cur.executemany(inserts.describes_podcast_sql, inserts.describes_podcast_vals)
        cur.executemany(inserts.guest_stars_sql, inserts.guest_stars_vals)
        cur.executemany(inserts.special_guest_sql, inserts.special_guest_vals)

        # setup song data

        cur.executemany(inserts.recordlabel_sql, inserts.recordlabel_vals)
        cur.executemany(inserts.artist_sql, inserts.artist_vals)
        cur.executemany(inserts.contracts_sql, inserts.contracts_vals)
        cur.executemany(inserts.album_sql, inserts.album_vals)
        cur.executemany(inserts.song_sql, inserts.song_vals)
        cur.executemany(inserts.collaborateson_sql, inserts.collaborateson_vals)
        cur.executemany(inserts.owns_sql, inserts.owns_vals)

        #

        cur.executemany(inserts.subscribestopodcast_sql, inserts.subscribestopodcast_vals)
        cur.executemany(inserts.listenstopodcastepisode_sql, inserts.listenstopodcastepisode_vals)
        cur.executemany(inserts.listentosong_sql, inserts.listentosong_vals)

        # commit

        conn.commit()

    except Exception as e:
        cur.close()
        conn.close()
        raise Exception(e)

    cur.close()
    conn.close()

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createTablesWrapper()

        cls.conn, cls.cur = db.Database().connect_to_MariaDB()

    @classmethod
    def tearDownClass(cls):
        cls.cur.close()
        cls.conn.close()
        dropTables.dropTables()

    def test_accept_payment(self):
        print(self)
        try:
            email = 'smallfry@aol.com'
            # TODO: insert into multiple tables from the select query
            # Known Alternative: use a temporary table
            queries = [
                "SET @email = 'smallfry@aol.com';",
                "SET @newPaymentId = (SELECT COUNT(*) from Payment);",
                f"SELECT subscriptionFee FROM User WHERE email = @email AND statusOfSubscription = 'A' INTO @value;",
                "INSERT into Payment(paymentId, date, value) values(@newPaymentId, CURRENT_DATE(), @value);",
                "INSERT into PayFromUser (paymentId, userEmail) values(@newPaymentId, @email);"
            ]

            printQueries(self, queries)

            for q in queries:
                Test.cur.execute(q)

            Test.conn.commit()

            Test.cur.execute(f"SELECT COUNT(*) FROM PayFromUser NATURAL JOIN Payment WHERE userEmail = '{email}'")

            self.assertEquals(1,
                              len(Test.cur.fetchall()),
                              f"Expected to find 1 payment record for {email}...")

        except Exception as e:
            print(e)
            self.fail()

    @unittest.skip('no longer needed')
    def test_pay_podcast_host(self):
        try:
            # TODO: insert into multiple tables from the select query
            # Known Alternative: use a temporary table

            creatorId = '3'
            queries = ["SET @baseAmount = 20.00;",
                       "SET @bonus = 5.00;",
                       "SET @creatorId = '3';",
                       "SELECT SUM(@baseAmount + @bonus * advertisementCount) FROM Hosts NATURAL JOIN Podcast NATURAL JOIN PodcastEpisode WHERE creatorId = @creatorId INTO @value;",
                       "SET @newPaymentId = (SELECT COUNT(*) from Payment);",
                       "INSERT Payment(paymentId, date, value) values(@newPaymentId, CURRENT_DATE(), @value);",
                       "INSERT into PayToContentCreator(paymentId, creatorId) values(@newPaymentId, @creatorId);"
                       ]

            printQueries(self, queries)

            for q in queries:
                Test.cur.execute(q)

            Test.conn.commit()

            Test.cur.execute(f"SELECT COUNT(*) FROM PayToContentCreator NATURAL JOIN Payment WHERE creatorId = '{creatorId}'")

            self.assertEquals(1,
                              len(Test.cur.fetchall()),
                              f"Expected to find 1 payment record for {creatorId}...")

        except Exception as e:
            print(e)
            self.fail()

    def test_select_queries(self):
        try:
            queries = [
                "SELECT * FROM PodcastGenre;",
                "SELECT * FROM DescribesPodcast;",
                "SELECT * FROM SpecialGuest;",
                "SELECT * FROM GuestStars;",
            ]

            for q in queries:
                Test.cur.execute(q)
                print(Test.cur.fetchall())

            printQueries(self, queries)

            Test.conn.commit()

        except Exception as e:
            print(e)
            self.fail()

    def test_podcast_genre_deletion(self):
        try:
            Test.cur.execute("SELECT * FROM DescribesPodcast;")

            self.assertEquals(4, len(Test.cur.fetchall()), f"Expected to find 4 DescribesPodcast relationships...")

            Test.cur.execute("SELECT * FROM PodcastGenre;")

            number_of_genres = len(Test.cur.fetchall())

            self.assertEquals(7, number_of_genres, f"Expected to find 7 podcast genres...")

            Test.cur.execute("DELETE FROM PodcastGenre WHERE genreName='News';")

            Test.cur.execute("SELECT * FROM PodcastGenre;")

            number_of_genres = len(Test.cur.fetchall())

            self.assertEquals(6, number_of_genres, f"Expected to find 6 podcast genres...")

            Test.cur.execute("SELECT * FROM DescribesPodcast;")

            self.assertEquals(3, len(Test.cur.fetchall()), f"Expected to find 3 DescribesPodcast relationships...")

            Test.conn.commit()

        except Exception as e:
            print(e)
            self.fail()
    def test_pay_royalties(self):
        try:

            Test.cur.execute("SELECT * FROM PayToContentCreator NATURAL JOIN Payment;")

            currentContentCreatorPayments = len(Test.cur.fetchall())

            # TODO: add to query after project2
            aristsToPay = [1, 5, 6]

            queries = [
                "SET @artistsShare = 0.70;",
                "SET @recordLabelShare = 0.30;",
                "SET @creatorId = 1;",
                "SET @albumName = 'Amputechture';",
                "SET @edition = 'Standard';",
                "SET @songTitle = 'Title 1';",

                # get play count, royalty rate, and record label for song
                "SELECT playCount, royaltyRate, recordLabelName  FROM Song natural join Owns WHERE creatorId = @creatorId AND albumName = @albumName AND edition = @edition AND songTitle = @songTitle INTO @playCount, @royaltyRate, @recordLabelName;",

                # create a temporary table with just the ids of the artists that will be paid
                "CREATE TEMPORARY TABLE ArtistsToPay(SELECT guestArtistId FROM CollaboratesOn WHERE creatorId = @creatorId AND albumName = @albumName AND edition = @edition AND songTitle = @songTitle);",

                "SET @totalArtists = (SELECT COUNT(*) FROM ArtistsToPay);",
                "SET @artistValue = @royaltyRate * @playCount * @artistsShare / (@totalArtists + 1);",
                "SET @recordLabelValue = @royaltyRate * @playCount * @recordLabelShare / (@totalArtists + 1);",

                # pay record label

                "SET @paymentId = (SELECT COUNT(*) from Payment);",
                "INSERT INTO Payment(paymentId, date, value) values(@paymentId, CURRENT_DATE(), @recordLabelValue);",
                "INSERT INTO PayToRecordLabel(recordLabelName, paymentId) values(@recordLabelName, @paymentId);",

                # # pay primary artist

                "SET @paymentId = (SELECT COUNT(*) from Payment);",
                "INSERT Payment(paymentId, date, value) values(@paymentId, CURRENT_DATE(), @artistValue);",
                "INSERT into PayToContentCreator(creatorId, paymentId) values(@creatorId, @paymentId);",

                # pay the guest artists
                # TODO: use a loop

                "SET @paymentId = (SELECT COUNT(*) from Payment);",
                "INSERT Payment(paymentId, date, value) values(@paymentId, CURRENT_DATE(), @artistValue);",
                "INSERT into PayToContentCreator(creatorId, paymentId) values(5, @paymentId);",

                "SET @paymentId = (SELECT COUNT(*) from Payment);",
                "INSERT Payment(paymentId, date, value) values(@paymentId, CURRENT_DATE(), @artistValue);",
                "INSERT into PayToContentCreator(creatorId, paymentId) values(6, @paymentId);",
            ]

            printQueries(self, queries)

            for q in queries:
                Test.cur.execute(q)

            Test.conn.commit()

            Test.cur.execute("SELECT * FROM PayToRecordLabel NATURAL JOIN Payment;")

            # TODO: assert no NULL values inserted especially with amounts

            self.assertEquals(1,
                              len(Test.cur.fetchall()),
                              f"Expected to find 1 payment records for record label...")


            Test.cur.execute("SELECT * FROM PayToContentCreator NATURAL JOIN Payment;")

            expected = currentContentCreatorPayments + 3
            self.assertEquals(expected,
                              len(Test.cur.fetchall()),
                              f"Expected to find {expected} payment records for content creators...")

        except Exception as e:
            print(e)
            self.fail()

if __name__ == '__main__':
    unittest.main()
