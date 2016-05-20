from playlist.orm.playlist import Playlist


class StaticPlaylist(Playlist):
    """
    Playlist that contains static.

    :ivar __playlist: The playlist
    :type __playlist: Iterable[str]
    """

    def __init__(self, playlist):
        self.__playlist = playlist

    def __iter__(self):
        return iter(self.__playlist)

    def __len__(self):
        return len(self.__playlist)
