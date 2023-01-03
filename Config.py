import configparser


class Config:
    _KEY_BLACKOUT_TRACK_PAUSED = "BlackoutTrackPaused"

    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.section_default = self.config['DEFAULT']

    def is_blackout_track_paused(self):
        return self.section_default[self._KEY_BLACKOUT_TRACK_PAUSED] == 'True'

    def blackout_track_paused(self, pause):
        self.section_default[self._KEY_BLACKOUT_TRACK_PAUSED] = pause
        self._save()

    def get_section(self, name):
        return self.config[name]

    def _save(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
