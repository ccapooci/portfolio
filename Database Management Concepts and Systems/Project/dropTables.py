from operations import db
import mariadb

def dropTables():
    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute('START TRANSACTION;')
        cur.execute('SET FOREIGN_KEY_CHECKS=0;')
        cur.execute('DROP TABLE IF EXISTS Artist;')
        cur.execute('DROP TABLE IF EXISTS Contracts;')
        cur.execute('DROP TABLE IF EXISTS DescribesPodcast;')
        cur.execute('DROP TABLE IF EXISTS GuestStars;')
        cur.execute('DROP TABLE IF EXISTS Hosts;')
        cur.execute('DROP TABLE IF EXISTS ListensToPodcastEpisode;')
        cur.execute('DROP TABLE IF EXISTS ListensToSong;')
        cur.execute('DROP TABLE IF EXISTS PayFromUser;')
        cur.execute('DROP TABLE IF EXISTS PayToContentCreator;')
        cur.execute('DROP TABLE IF EXISTS PayToRecordLabel;')
        cur.execute('DROP TABLE IF EXISTS Payment;')
        cur.execute('DROP TABLE IF EXISTS Podcast;')
        cur.execute('DROP TABLE IF EXISTS PodcastEpisode;')
        cur.execute('DROP TABLE IF EXISTS PodcastGenre;')
        cur.execute('DROP TABLE IF EXISTS PodcastHost;')
        cur.execute('DROP TABLE IF EXISTS RecordLabel;')
        cur.execute('DROP TABLE IF EXISTS SpecialGuest;')
        cur.execute('DROP TABLE IF EXISTS Sponsor;')
        cur.execute('DROP TABLE IF EXISTS Sponsors;')
        cur.execute('DROP TABLE IF EXISTS SubscribesToPodcast;')
        cur.execute('DROP TABLE IF EXISTS User;')
        cur.execute('DROP TABLE IF EXISTS Album;')
        cur.execute('DROP TABLE IF EXISTS CollaboratesOn;')
        cur.execute('DROP TABLE IF EXISTS Owns;')
        cur.execute('DROP TABLE IF EXISTS Song;')
        cur.execute('DROP TABLE IF EXISTS ContentCreator;')
        cur.execute('SET FOREIGN_KEY_CHECKS=1;')
        cur.execute('COMMIT;')

        print('Tables dropped successfully!')

        conn.close()

    except mariadb.Error as e:
        print(f"Error dropping tables: {e}")
        cur.execute('ROLLBACK;')
        conn.close()

def main():
    dropTables()

if __name__ == '__main__':
    main()
