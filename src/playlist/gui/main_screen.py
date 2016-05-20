from io import BytesIO

import mutagen
from kivy.core.audio import SoundLoader, Sound
from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty, NumericProperty, BoundedNumericProperty, Clock
from kivy.uix.screenmanager import Screen

from playlist.orm import DirectoryPlaylist
from playlist.orm.static_playlist import StaticPlaylist


class MainScreen(Screen):
    """
    :var image_texture:
    :type image_texture: kivy.graphics.texture.Texture
    :var sound: the sound
    :type sound: Sound
    :var playlist:
    :type playlist: playlist.orm.playlist.Playlist
    :var playlist_current_index: The current index
    :type playlist_current_index: int
    :var last_sound_position: The last position in the song
    :type last_sound_position: float
    :var volume: The volume of the song
    :type volume: float
    :var __cached_playlist: The playlist loaded from the playlist
    :type __cached_playlist: list[Media]
    """

    image_texture = ObjectProperty(None)
    sound = ObjectProperty(None)
    playlist = ObjectProperty()
    playlist_current_index = NumericProperty(0)
    last_sound_position = NumericProperty(0)
    volume = BoundedNumericProperty(1., min=0, max=1)

    def __init__(self, **kw):
        super().__init__(**kw)

        self.playlist = StaticPlaylist([

        ])
        self.__cached_playlist = list(self.playlist)
        self.load_audio()

        def update_position(_):
            if self.sound and self.sound.state == 'play':
                self.last_sound_position = self.sound.get_pos()

        Clock.schedule_interval(update_position, 1.5)

    def play(self):
        if self.sound.state == 'stop':
            self.sound.play()
            self.sound.seek(self.last_sound_position)
        else:
            self.last_sound_position = self.sound.get_pos()
            self.sound.stop()

    def back(self):
        is_played = self.sound.state == 'play'
        self.sound.stop()
        self.last_sound_position = 0
        if self.last_sound_position < 1:
            self.playlist_current_index -= 1
            if -1 == self.playlist_current_index:
                self.__cached_playlist = list(self.playlist)
                self.playlist_current_index = len(self.__cached_playlist) - 1
            self.load_audio()
            if is_played:
                self.play()
        else:
            self.play()

    def next(self):
        is_played = self.sound.state == 'play'
        self.sound.stop()
        self.last_sound_position = 0
        self.playlist_current_index += 1
        if len(self.__cached_playlist) == self.playlist_current_index:
            self.__cached_playlist = list(self.playlist)
            self.playlist_current_index = 0
        self.load_audio()
        if is_played:
            self.play()

    def load_audio(self):
        if self.sound:
            self.sound.unload()
        if len(self.__cached_playlist) == 0:
            return
        self.sound = SoundLoader.load(self.__cached_playlist[self.playlist_current_index])
        self.sound.volume = self.volume
        audio_path = self.__cached_playlist[self.playlist_current_index]
        music_file = mutagen.File(audio_path)
        for k, v in music_file.items():
            if k.startswith('APIC'):
                ext = v.mime[6:]
                data = BytesIO(v.data)
                self.image_texture = CoreImage(data, ext=ext).texture
                break
