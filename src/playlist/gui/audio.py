from io import BytesIO

import mutagen
from kivy.atlas import CoreImage
from kivy.core.audio import SoundLoader
from kivy.properties import BoundedNumericProperty, ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

__all__ = ['Audio', 'Playlist']


class Audio(Widget):
    image_texture = ObjectProperty(None)
    sound = ObjectProperty(None)
    position = NumericProperty(0)

    def __init__(self, audio_path, position=0, volume=None, **kwargs):
        super().__init__(**kwargs)

        self.position = position
        self.sound = SoundLoader.load(audio_path)
        if volume is not None:
            self.sound.volume = volume

        music_file = mutagen.File(audio_path)
        for k, v in music_file.items():
            if k.startswith('APIC'):
                ext = v.mime[6:]
                data = BytesIO(v.data)
                self.image_texture = CoreImage(data, ext=ext).texture
                break

    def __del__(self):
        self.unload()

    def unload(self):
        self.sound.unload()

    def play(self):
        if self.is_playing:
            self.sound.stop()
            self.seek(self.position)
        else:
            self.sound.play()

    @property
    def is_playing(self):
        return self.sound.state == 'play'

    def reset(self):
        self.position = 0

    def seek(self, position):
        self.position = position
        self.sound.seek(self.position)

    @property
    def volume(self):
        return self.sound.volume

    @volume.setter
    def volume(self, new_volume):
        self.sound.volume = new_volume


class Playlist(Widget):
    current_audio = ObjectProperty(None)
    playlist = ObjectProperty()
    current_index = NumericProperty(0)
    last_sound_position = NumericProperty(0)

    def __init__(self, playlist, current_index=0, **kwargs):
        super().__init__(**kwargs)

        self.playlist = playlist
        self.current_index = current_index
        self.current_audio = None
        self.reload()

    def play(self):
        self.current_audio.play()

    def back(self):
        if self.current_audio.is_playing or self.current_audio.is_playing:
            self.current_audio.seek(0)
        else:
            self.current_index -= 1
            self.current_index %= len(self.playlist)
            self.reload()

    def next(self):
        self.current_index += 1
        self.current_index %= len(self.playlist)
        self.reload()

    def reload(self):
        is_playing = False
        if self.current_audio is not None:
            self.current_audio.unload()
            is_playing = self.current_audio.is_playing
            if is_playing:
                self.current_audio.play()
        self.current_audio = Audio(self.playlist[self.current_index])
        if is_playing:
            self.current_audio.play()

    @property
    def volume(self):
        return self.current_audio.volume

    @volume.setter
    def volume(self, new_volume):
        self.current_audio.volume = new_volume
