import os

from watchdog.events import RegexMatchingEventHandler, DirDeletedEvent, FileDeletedEvent, DirCreatedEvent,\
    FileCreatedEvent
from watchdog.observers import Observer

from playlist.orm.playlist import Playlist


class DirectoryPlaylist(Playlist):
    """
    Playlist that contains all songs from a directory

    :ivar path: The directory
    :type path: str
    :ivar __playlist: The playlist
    :type __playlist: set[str]
    """

    observers = list()
    AUDIO_PREFIX = ["mp3"]

    def __init__(self, path, recursive):
        self.__playlist = set()
        observer = Observer()
        observer.schedule(DirectoryPlaylistEventHandler(path, self.__playlist, self.AUDIO_PREFIX), path, recursive)
        observer.start()
        self.observers.append(observer)

    def __iter__(self):
        return iter(self.__playlist)

    def __len__(self):
        return len(self.__playlist)


class DirectoryPlaylistEventHandler(RegexMatchingEventHandler):
        def __init__(self, path, playlist, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__path = path
            self.__playlist = playlist

        def on_moved(self, event):
            """

            :param event:
            :type event: DirMovedEvent or FileMovedEvent
            """
            if event.src_path.startswith(self.__path) and not event.dest_path.startswith(self.__path):
                new_event_class = DirDeletedEvent if event.is_directory else FileDeletedEvent
                self.on_deleted(new_event_class(event.dest_path))
            elif not event.src_path.startswith(self.__path) and event.dest_path.startswith(self.__path):
                new_event_class = DirCreatedEvent if event.is_directory else FileCreatedEvent
                self.on_created(new_event_class(event.dest_path))

        def on_deleted(self, event):
            """

            :param event:
            :type event: DirDeletedEvent or FileDeletedEvent
            """
            if event.is_directory:
                self.__playlist.difference_update(filter(lambda x: x.startswith(event.src_path), self.__playlist))
            else:
                self.__playlist.remove(event.src_path)

        def on_created(self, event):
            """

            :param event:
            :type event: DirCreatedEvent or FileCreatedEvent
            """
            if event.is_directory:
                self.__playlist.update(os.listdir(event.src_path))
            else:
                self.__playlist.add(event.src_path)
