import kivy
kivy.require("1.9.1")
from kivy.config import Config
Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '350')
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.settings import SettingsWithNoMenu
from kivy.app import App
from playlist.gui.main_screen import MainScreen


class MediaPlayerApp(App):
    size = (20, 20)

    def build(self):
        self.settings_cls = SettingsWithNoMenu
        screen_manager = ScreenManager()
        main_screen = MainScreen()
        screen_manager.add_widget(main_screen)

        return screen_manager

    def build_config(self, config):
        config.setdefaults('example', {
            'volume': True
        })

    def build_settings(self, settings):
        settings.add_json_panel('Settings',
                                self.config, filename='settings/MediaPlayer.json')

    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)


def main():
    app = MediaPlayerApp()
    app.run()


if __name__ == '__main__':
    MediaPlayerApp().run()
