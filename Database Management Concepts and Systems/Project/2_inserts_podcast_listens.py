from operations import db
import mariadb
import datetime as dt
import time

start = time.time()


listenstopodcastepisode_sql = ("INSERT INTO ListensToPodcastEpisode (userEmail, podcastEpisodeTitle, podcastName, "
                               "timestamp) VALUES (%s, %s, %s, %s)")

listenstopodcastepisode_vals = [
]

seconds = 0
minutes = 0
hours = 0
days = 0
for i in range(100):
    seconds = i % 60
    minutes = (int(i / 60) % 60)
    hours = (int(i / 3600) % 24)
    days = int(i / 86400) + 1
    listenstopodcastepisode_vals.append(("alexa@alexa.dev", "The Science of Mindfulness", "Mind Over Matter: Exploring the Power of the Human Mind", "2023-04-" + str(days) + " " + str(hours) + ":" + str(minutes) + ":" + str(seconds)))

seconds = 0
minutes = 0
hours = 0
days = 0
for i in range(200):
    seconds = i % 60
    minutes = (int(i / 60) % 60)
    hours = (int(i / 3600) % 24)
    days = int(i / 86400) + 1
    listenstopodcastepisode_vals.append(("johnj@johnj.dev", "Unlocking Your Potential", "Mind Over Matter: Exploring the Power of the Human Mind", "2023-04-" + str(days) + " " + str(hours) + ":" + str(minutes) + ":" + str(seconds)))

seconds = 0
minutes = 0
hours = 0
days = 0
for i in range(30):
    seconds = i % 60
    minutes = (int(i / 60) % 60)
    hours = (int(i / 3600) % 24)
    days = int(i / 86400) + 2
    listenstopodcastepisode_vals.append(("alexa@alexa.dev", "Ep 3", "Mind Over Matter: Exploring the Power of the Human Mind", "2023-04-" + str(days) + " " + str(hours) + ":" + str(minutes) + ":" + str(seconds)))

seconds = 0
minutes = 0
hours = 0
days = 0
for i in range(40):
    seconds = i % 60
    minutes = (int(i / 60) % 60)
    hours = (int(i / 3600) % 24)
    days = int(i / 86400) + 2
    listenstopodcastepisode_vals.append(("johnj@johnj.dev", "Ep 4", "Mind Over Matter: Exploring the Power of the Human Mind", "2023-04-" + str(days) + " " + str(hours) + ":" + str(minutes) + ":" + str(seconds)))

seconds = 0
minutes = 0
hours = 0
days = 0
for i in range(50):
    seconds = i % 60
    minutes = (int(i / 60) % 60)
    hours = (int(i / 3600) % 24)
    days = int(i / 86400) + 3
    listenstopodcastepisode_vals.append(("alexa@alexa.dev", "Ep 5", "Mind Over Matter: Exploring the Power of the Human Mind", "2023-04-" + str(days) + " " + str(hours) + ":" + str(minutes) + ":" + str(seconds)))



inserts = {
    'listens_to_podcast_episode': [listenstopodcastepisode_sql, listenstopodcastepisode_vals],
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
