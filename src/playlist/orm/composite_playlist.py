from itertools import chain

from playlist.orm.playlist import Playlist


class CompositePlaylist(Playlist):
    """
    Playlist that contains other playlists.

    :ivar __playlists: The playlists
    :type __playlists: set[Media]
    """

    def __init__(self, playlists):
        self.__playlists = set(playlists)

    def __iter__(self):
        return chain(*self.__playlists)

    def __len__(self):
        return sum(map(len, self.__playlists))
