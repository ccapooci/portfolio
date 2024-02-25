"""
Module to handle creation of all tables for the database.
"""

import mariadb
from operations import db

ContentCreator = """
CREATE TABLE ContentCreator (
    creatorId INT,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255),
    PRIMARY KEY(creatorId)
);
"""

User = """
CREATE TABLE User (
    email VARCHAR(255),
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    subscriptionFee DECIMAL(9,2) NOT NULL,
    statusOfSubscription CHAR(1) NOT NULL
    CHECK (statusOfSubscription IN ('A', 'I')),
    phone VARCHAR(16),
    registrationDate DATE NOT NULL,
    PRIMARY KEY(email)
);
"""

ListensToSong = """
CREATE TABLE ListensToSong (
    email VARCHAR(255),
    songTitle VARCHAR(255),
    creatorId INT,
    albumName VARCHAR(255),
    edition VARCHAR(255),
    timestamp DATETIME,
    PRIMARY KEY(email, songTitle, creatorId, albumName, edition, timestamp),
    FOREIGN KEY (email) REFERENCES User(email) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (creatorId, albumName, edition, songTitle)
    REFERENCES Song(creatorId, albumName, edition, songTitle) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

SubscribesToPodcast = """
CREATE TABLE SubscribesToPodcast (
    email VARCHAR(255),
    podcastName VARCHAR(255),
    timestamp DATETIME,
    PRIMARY KEY(email, podcastName, timestamp),
    FOREIGN KEY(email) REFERENCES User(email) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(podcastName) REFERENCES Podcast(podcastName) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

ListensToPodcastEpisode = """
CREATE TABLE ListensToPodcastEpisode (
    userEmail VARCHAR(255),
    podcastEpisodeTitle VARCHAR(255),
    podcastName VARCHAR(255),
    timestamp DATETIME,
    PRIMARY KEY(userEmail, podcastEpisodeTitle, podcastName, timestamp),
    FOREIGN KEY(userEmail) REFERENCES User(email) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(podcastEpisodeTitle) REFERENCES PodcastEpisode(title) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(podcastName) REFERENCES Podcast(podcastName) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

Payment = """
CREATE TABLE Payment (
    paymentId INT,
    date DATE NOT NULL,
    value DECIMAL(9,2) NOT NULL,
    PRIMARY KEY(paymentId)
);
"""

PayToContentCreator = """
CREATE TABLE PayToContentCreator (
    creatorId INT,
    paymentId INT,
    PRIMARY KEY(creatorId, paymentId),
    FOREIGN KEY (creatorId) REFERENCES ContentCreator(creatorId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(paymentId) REFERENCES Payment(paymentId) ON UPDATE CASCADE
);
"""

PayToRecordLabel = """
CREATE TABLE PayToRecordLabel(
    paymentId INT,
    recordLabelName VARCHAR(255),
    PRIMARY KEY(paymentId, recordLabelName),
    FOREIGN KEY(paymentId) REFERENCES Payment(paymentId) ON UPDATE CASCADE,
    FOREIGN KEY (recordLabelName) REFERENCES RecordLabel(labelName) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

PayFromUser = """
CREATE TABLE PayFromUser(
    paymentId INT,
    userEmail VARCHAR(255),
    PRIMARY KEY(paymentId, userEmail),
    FOREIGN KEY(paymentId) REFERENCES Payment(paymentId) ON UPDATE CASCADE,
    FOREIGN KEY(userEmail) REFERENCES User(email) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

Song = """
CREATE TABLE Song (
    creatorId INT,
    albumName VARCHAR(255),
    edition VARCHAR(255),
    songTitle VARCHAR(255),
    trackNumber INT NOT NULL,
    duration INT NOT NULL,
    playCount INT NOT NULL,
    releaseDate DATE NOT NULL,
    releaseCountry VARCHAR(255) NOT NULL,
    language VARCHAR(25) NOT NULL,
    royaltyPaidStatus BOOLEAN,
    royaltyRate DECIMAL(2,2) NOT NULL,
    PRIMARY KEY(creatorId, albumName, edition, songTitle),
    FOREIGN KEY(creatorId, albumName, edition) REFERENCES Album(creatorId, albumName, edition) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

CollaboratesOn = """
CREATE TABLE CollaboratesOn (
    creatorId INT,
    guestArtistId INT,
    songTitle VARCHAR(255),
    albumName VARCHAR(255),
    edition VARCHAR(255),
    PRIMARY KEY(creatorId, guestArtistId, songTitle, albumName, edition),
    FOREIGN KEY (guestArtistId) REFERENCES ContentCreator(creatorId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (creatorId, albumName, edition, songTitle)
    REFERENCES Song(creatorId, albumName, edition, songTitle) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

Album = """
CREATE TABLE Album (
    creatorId INT,
    albumName VARCHAR(255),
    edition VARCHAR(255),
    releaseYear INT(4),
    PRIMARY KEY(creatorId, albumName, edition),
    FOREIGN KEY (creatorId) REFERENCES ContentCreator(creatorId) ON UPDATE CASCADE ON DELETE CASCADE
    
);
"""

Artist = """
CREATE TABLE Artist (
    creatorId INT,
    status CHAR(1) NOT NULL
    CHECK (statusOfSubscription IN ('A', 'I')),
    type VARCHAR(25) NOT NULL,
    country VARCHAR(255) NOT NULL,
    primaryGenre VARCHAR(255) NOT NULL,
    PRIMARY KEY(creatorId),
    FOREIGN KEY(creatorId) REFERENCES ContentCreator(creatorId) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

Contracts = """
CREATE TABLE Contracts (
    creatorId INT,
    recordLabelName VARCHAR(255),
    PRIMARY KEY(creatorId, recordLabelName),
    FOREIGN KEY(creatorId) REFERENCES ContentCreator(creatorId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(recordLabelName) REFERENCES RecordLabel(labelName) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

RecordLabel = """
CREATE TABLE RecordLabel (
    labelName VARCHAR(255),
    PRIMARY KEY (labelName)
);
"""

Owns = """
CREATE TABLE Owns (
    creatorId INT,
    recordLabelName VARCHAR(255),
    songTitle VARCHAR(255),
    albumName VARCHAR(255),
    edition VARCHAR (255),
    PRIMARY KEY(creatorId, recordLabelName, songTitle, albumName, edition),
    FOREIGN KEY(recordLabelName) REFERENCES RecordLabel(labelName) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(creatorId, albumName, edition, songTitle) REFERENCES Song(creatorId, albumName, edition, songTitle) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

PodcastHost = """
CREATE TABLE PodcastHost (
    creatorId INT,
    email VARCHAR(255),
    phone VARCHAR(16),
    city VARCHAR(255),
    PRIMARY KEY(creatorId),
    FOREIGN KEY(creatorId) REFERENCES ContentCreator(creatorId) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

Hosts = """
CREATE TABLE Hosts (
    podcastName VARCHAR(255) NOT NULL,
    creatorId INT,
    PRIMARY KEY(podcastName, creatorId),
    FOREIGN KEY(podcastName) REFERENCES Podcast(podcastName) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(creatorId) REFERENCES ContentCreator(creatorId) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

Podcast = """
CREATE TABLE Podcast (
    podcastName VARCHAR(255),
    language VARCHAR(25) NOT NULL,
    country VARCHAR(255) NOT NULL,
    rating DECIMAL(2,1) NOT NULL,
    PRIMARY KEY(podcastName)
);
"""

Sponsors = """
CREATE TABLE Sponsors (
    podcastName VARCHAR(255),
    sponsorName VARCHAR(255),
    PRIMARY KEY(podcastName, sponsorName),
    FOREIGN KEY(podcastName) REFERENCES Podcast(podcastName) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(sponsorName) REFERENCES Sponsor(sponsorName) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

Sponsor = """
CREATE TABLE Sponsor (
    sponsorName VARCHAR(255),
    PRIMARY KEY(sponsorName)
);
"""

PodcastGenre = """
CREATE TABLE PodcastGenre (
    genreName VARCHAR(255),
    PRIMARY KEY(genreName)
);
"""

DescribesPodcast = """
CREATE TABLE DescribesPodcast (
    podcastName VARCHAR(255),
    genreName VARCHAR(255),
    PRIMARY KEY(podcastName, genreName),
    FOREIGN KEY(podcastName) REFERENCES Podcast(podcastName) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(genreName) REFERENCES PodcastGenre(genreName) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

PodcastEpisode = """
CREATE TABLE PodcastEpisode (
    title VARCHAR(255),
    podcastName VARCHAR(255),
    duration INT NOT NULL,
    releaseDate DATE NOT NULL,
    advertisementCount INT NOT NULL,
    PRIMARY KEY(title, podcastName),
    FOREIGN KEY(podcastName) REFERENCES Podcast(podcastName) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

GuestStars = """
CREATE TABLE GuestStars (
    creatorId INT,
    title VARCHAR(255),
    podcastName VARCHAR(255),
    PRIMARY KEY(creatorId, title, podcastName),
    FOREIGN KEY(creatorId) REFERENCES ContentCreator(creatorId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(title, podcastName) REFERENCES PodcastEpisode(title, podcastName) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

SpecialGuest = """
CREATE TABLE SpecialGuest (
    creatorId INT,
    PRIMARY KEY(creatorId),
    FOREIGN KEY(creatorId) REFERENCES ContentCreator(creatorId) ON UPDATE CASCADE ON DELETE CASCADE
);
"""

def createTables():
    conn, cur = db.Database().connect_to_MariaDB()

    try:
        cur.execute(User)
        cur.execute(ContentCreator)
        cur.execute(Artist)
        cur.execute(Album)
        cur.execute(Song)
        cur.execute(CollaboratesOn)
        cur.execute(RecordLabel)
        cur.execute(Contracts)
        cur.execute(Owns)
        cur.execute(PodcastHost)
        cur.execute(Podcast)
        cur.execute(Hosts)
        cur.execute(Sponsor)
        cur.execute(Sponsors)
        cur.execute(PodcastEpisode)
        cur.execute(PodcastGenre)
        cur.execute(DescribesPodcast)
        cur.execute(GuestStars)
        cur.execute(SpecialGuest)
        cur.execute(SubscribesToPodcast)
        cur.execute(ListensToPodcastEpisode)
        cur.execute(ListensToSong)
        cur.execute(Payment)
        cur.execute(PayToContentCreator)
        cur.execute(PayToRecordLabel)
        cur.execute(PayFromUser)
        print('Table creation successful!')

        conn.close()

    except mariadb.Error as e:
        print(f"Error with table creation: {e}")
        conn.close()

def main():
    createTables()

if __name__ == '__main__':
    main()
