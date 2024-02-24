from operations import db
import mariadb
import datetime as dt
import time

start = time.time()


listentosong_sql = ("INSERT INTO ListensToSong (email, songTitle, creatorId, albumName, edition, timestamp) VALUES (%s, %s, %s, %s, %s, %s)")

listentosong_vals = [
]

seconds = 0
minutes = 0
hours = 0
days = 0
for i in range(1000):
    seconds = i % 60
    minutes = (int(i / 60) % 60)
    hours = (int(i / 3600) % 24)
    days = int(i / 86400) + 2
    listentosong_vals.append(("johnj@johnj.dev", "Echoes of You", 2002, "Lost in the Echoes", "Standard", "2023-01-" + str(days) + " " + str(hours) + ":" + str(minutes) + ":" + str(seconds)))

inserts = {
    'listen_to_song': [listentosong_sql, listentosong_vals],
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
