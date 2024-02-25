import createTables

tableStatement = [
    "ContentCreator",
    "User",
    "ListensToSong",
    "SubscribesToPodcast",
    "ListensToPodcastEpisode",
    "Payment",
    "PayToContentCreator",
    "PayToRecordLabel",
    "PayFromUser",
    "Song",
    "CollaboratesOn",
    "Album",
    "Artist",
    "Contracts",
    "RecordLabel",
    "Owns",
    "PodcastHost",
    "Hosts",
    "Podcast",
    "Sponsors",
    "Sponsor",
    "PodcastGenre",
    "DescribesPodcast",
    "PodcastEpisode",
    "GuestStars",
    "SpecialGuest",
]

for table in tableStatement:
    print(getattr(createTables, table))
