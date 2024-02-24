"""CLI to WolfMedia.

Perform a variety of operations against the WolfMedia System,
including:

1. Information Processing: Enter/update/delete basic information about
songs, artists, podcast hosts, and podcast episodes. Assign songs and
artists to albums. Assign artists to record labels. Assign podcast
episodes and podcast hosts to podcasts.

2. Maintaining metadata and records: Enter/update play count for
songs.  Enter/update the count of monthly listeners for
artists. Enter/update the total count of subscribers and ratings for
podcasts. Enter/Update the listening count for podcast episodes. Find
songs and podcast episodes given artist, album, and/or podcast.

3.  Maintaining payments: Make royalty payments for a given
song. Monthly royalties are generated based on a royalty rate for each
song times the total play count per month. 30% of the collected
royalties are paid to the record label and the remainder is
distributed evenly among all participating artists. Make payment to
podcast hosts. Podcast hosts are paid a single flat fee per released
episode and an additional bonus based on total advertisements per
podcast episode. Receive payment from subscribers.

4. Reports: Generate all the following reports: Monthly play count per
song/album/artist. Calculate total payments made out to
host/artist/record labels per a given time period. Total revenue of
the streaming service per month, per year. Report all songs/podcast
episodes given an artist, album, and/or podcast.

Usage:

  python3 ./main.py
"""
import cmd, sys

import operations.db
from operations import payments
from operations import reports
from operations import metadata
from operations.informationProcessing import song, user, recordLabel, album, artist, podcast, podcastHost, podcastEpisode


class WolfMediaCLI(cmd.Cmd):
    """CLI for interacting with WolfMediaCLI.

    This class inherits most CLI functionality from cmd.Cmd,
    overriding some methods and adding some helper methods and
    functionality specific to the WolfMedia API.


    Attributes:
        intro: Intro message when the CLI is started.
        prompt: Prompt that is printed before each command runs.
    """

    # TODO: giant wolf face or something using text
    intro = 'Welcome to WolfMedia.   Type help or ? to list commands.\n'
    prompt = '(WF) '

    # overridden methods

    def preloop(self):
        """Hook method executed once when cmdloop() is called.
        """
        # TODO: database connect here?
        print_debug("Starting...")

    def postloop(self):
        """Hook method executed once when cmdloop() is about to return.
        """
        # TODO: database close here?
        print_debug("Ending...")

    # TODO: may be unnecessary
    def precmd(self, line):
        """Executed before the command-line is interpreted.

        Args:
          line:
            line to modify

        Returns:
          modified line which is interpreted
        """
        return line

    # TODOn't: probably don't want to override this

    # def postcmd(self, stop, line):
    #     """Executed after a command dispatch is finished.

    #     The stop argument to postcmd() is the return value from the command’s corresponding do_*() method.

    #     """
    #     pass

    # TODO: catch kill signals making sure to close DB connections?

    # TODO: do we want to override
    # def do_help(self):
    #     """Print help.
    #     """
    #     # All subclasses of Cmd inherit a predefined do_help(). This method, called with an argument 'bar', invokes the corresponding method help_bar(), and if that is not present, prints the docstring of do_bar(), if available. With no argument, do_help() lists all available help topics (that is, all commands with corresponding help_*() methods or commands that have docstrings), and also lists any undocumented commands.

    def do_quit(self, arg):
        """Terminate the program.

        Args:
          arg: dummy argument as required by class

        Returns:
          True always to signal to terminate the program.
        """
        print_debug(arg)
        return True

    # An interpreter instance will recognize a command name foo if and only if it has a method do_foo()
    # Return True to quit; Return False to keep command loop going

    # payment operations

    def do_makeSongPayment(self, arg):
        """Make royalty payments for a song.
        """
        status, results = payments.make_song_payment_interactive()
        print_stdout(results)

    def do_receivePayment(self, arg):
        """Receive subscription payment from user.
        """
        status, results = payments.receive_payment_interactive()
        print_stdout(results)

    def do_payPodcastHosts(self, arg):
        """Pay podcast hosts.
        """
        status, results = payments.pay_podcast_hosts_interactive()
        print_stdout(results)

    # report operations
    def do_monthlyPlayCountSong(self, arg):
        """ Get the play count for a song for a given month.
        """
        reports.calculate_monthly_play_count_song()

    def do_monthlyPlayCountAlbum(self, arg):
        """ Get the play count for an album for a given month.
        """
        reports.calculate_monthly_play_count_album()

    def do_monthlyPlayCountArtist(self, arg):
        """ Get the play count for the artist for a given month.
        """
        reports.calculate_monthly_play_count_artist()

    def do_totalPaymentHost(self, arg):
        """ Get the total payment to a host for a time period provided by the user.
        """
        reports.calculate_total_payment_to_host_per_time_period()

    def do_totalPaymentArtist(self, arg):
        """ Calculate the total payment to an artist for a time period provided by the user.
        """
        reports.calculate_total_payment_to_artist_per_time_period()

    def do_totalPaymentRecordLabel(self, arg):
        """ Calculate the total payment for a record label for a time period provided by the user.
        """
        reports.calculate_total_payment_to_record_label_per_time_period()

    def do_totalRevenueMonth(self, arg):
        """ Calculate the revenue of the streaming service for the given month.
        """
        reports.calculate_total_revenue_per_month()

    def do_totalRevenueYear(self, arg):
        """ Calculate the revenue of the streaming service for the given year.
        """
        reports.calculate_total_revenue_per_year()

    def do_allSongsArtist(self, arg):
        """ Report the songs for a given artist.
        """
        reports.report_songs_artist()

    def do_allSongsAlbum(self, arg):
        """ Report the songs for a given album.
        """
        reports.report_songs_album()

    def do_allSongsAlbumArtist(self, arg):
        """ Report the songs for a given album and artist.
        """
        reports.report_songs_album_and_artist()

    def do_allEpisodesPodcast(self, arg):
        """ Report the episodes in a given podcast.
        """
        reports.report_podcasts_epsiodes()

    # Metadata operations
    def do_updateSongPlayCount(self, arg):
        """
        Updates play count for a given song.
        """
        metadata.update_song_play_count()

    def do_updatePodcastRatings(self, arg):
        """
        Updates rating for a selected podcast.
        """
        metadata.update_podcast_ratings()

    def do_findSongsGivenArtist(self, arg):
        """
        Returns a list of songs for a given artist name.
        """
        metadata.find_songs_given_artist()

    def do_findSongsGivenAlbum(self, arg):
        """
        Returns a list of songs for a given album title. Helps the user find the correct album if there are multiple
        albums with the same name.
        """
        metadata.find_songs_given_album()

    def do_findPodcastEpisodesGivenPodcast(self, arg):
        """
        Returns a list of podcast episodes for a given podcast name.
        """
        metadata.find_podcast_episodes_given_podcast()

    def do_updateArtistMonthlyListeners(self, arg):
        """
        Walks the user through the view monthly listeners or ListenToSong process.
        """
        metadata.update_artist_monthly_listeners()

    def do_updatePodcastSubscribers(self, arg):
        """
        Walks the user through the view subscribers or subscribe/unsubscribe process.
        """
        metadata.update_podcast_subscribers()

    def do_updatePodcastListeners(self, arg):
        """
        Walks user through the podcast listener info.
        """
        metadata.update_podcast_episode_listener_count()

    # Information Processing

    def do_enterSongInfo(self, arg):
        """Create song from user input.
        """
        song.create_song()

    def do_updateSongInfo(self, arg):
        """Update song from user input.
        """
        song.update_song()

    def do_deleteSongInfo(self, arg):
        """Delete song from user input.
        """
        song.delete_song()

    def do_assignCollaborationBetweenArtistsAndSong(self, arg):
        """Assign collaboration between artists and song.
        """
        song.assign_collaboration_between_artists_and_song()

    def do_enterUserInfo(self, arg):
        """Create user from user input.
        """
        user.create_user()

    def do_updateUserInfo(self, arg):
        """Update user from user input.
        """
        user.update_user()

    def do_deleteUserInfo(self, arg):
        """Delete song from user input.
        """
        user.delete_user()

    def do_enterRecordLabelInfo(self, arg):
        """Create record label from user input.
        """
        recordLabel.create_record_label()

    def do_updateRecordLabelInfo(self, arg):
        """Update record label from user input.
        """
        recordLabel.update_record_label()

    def do_deleteRecordLabelInfo(self, arg):
        """Delete record label from user input.
        """
        recordLabel.delete_record_label()

    def do_assignRecordLabelToSong(self, arg):
        """Assign record label to song
        """
        recordLabel.assign_record_label_to_song()

    def do_updateContractedArtist(self, arg):
        """Create Contracts relationship between artist and record label from user input.
        """
        recordLabel.update_contracted_artist()

    def do_enterAlbumInfo(self, arg):
        """Create album from user input.
        """
        album.create_album()

    def do_updateAlbumInfo(self, arg):
        """Update album from user input.
        """
        album.update_album()

    def do_deleteAlbumInfo(self, arg):
        """Delete album from user input.
        """
        album.delete_album()

    def do_enterArtistInfo(self, arg):
        """Create artist from user input.
        """
        artist.create_artist()

    def do_updateArtistInfo(self, arg):
        """Update artist from user input.
        """
        artist.update_artist()

    def do_deleteArtistInfo(self, arg):
        """Delete artist from user input.
        """
        artist.delete_artist()

    def do_enterPodcastInfo(self, arg):
        """Create podcast from user input.
        """
        podcast.create_podcast()

    def do_updatePodcastInfo(self, arg):
        """Update podcast from user input.
        """
        podcast.update_podcast()

    def do_deletePodcastInfo(self, arg):
        """Delete podcast from user input.
        """
        podcast.delete_podcast()

    def do_enterPodcastHostInfo(self, arg):
        """Create podcast host from user input.
        """
        podcastHost.create_podcast_host()

    def do_updatePodcastHostInfo(self, arg):
        """Update podcast host from user input.
        """
        podcastHost.update_podcast_host()


    def do_deletePodcastHostInfo(self, arg):
        """Delete podcast host from user input.
        """
        podcastHost.delete_podcast_host()

    def do_enterPodcastEpisodeInfo(self, arg):
        """Create podcast episode from user input.
        """
        podcastEpisode.create_podcast_episode()

    def do_updatePodcastEpisodeInfo(self, arg):
        """Update podcast episode from user input.
        """
        podcastEpisode.update_podcast_episode()

    def do_deletePodcastEpisodeInfo(self, arg):
        """Delete podcast episode from user input.
        """
        podcastEpisode.delete_podcast_episode()


    # Misc
    def do_queryDB(self, arg):
        """
        Allows user to query the DB with any SQL statement.
        """
        operations.db.query_db()


    def do_generateUsers(self, arg):
        """
        Generates a specified number of users to add to the system.
        """
        operations.db.bulk_add_users()

# TODO: maybe we move these helper functions into separate module

def parse(arg):
    """Parse multiple arguments from whitespace delimited argument.

    Args:
      arg: argument from which to parse arguments

    Returns:
      tuple of arguments parsed
    """
    return arg.split()


def print_debug(msg):
    """Print message to debug.

    Args:
      msg: message to print to stderr
    """
    print(msg, file=sys.stderr)


def print_stdout(msg):
    """Print message to stdout.

    Args:
      msg: message to print to stdout
    """
    print(msg, file=sys.stdout)


if __name__ == '__main__':
    WolfMediaCLI().cmdloop()
