import os
from Config import Config


class Toolkit:
    def __init__(self):
        self.location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.csv_registry = None
        self.gs_registry = None
        self.config = Config(self.path("solvek.cfg"))

    def path(self, filename):
        return os.path.join(self.location, filename)

    def get_csv_registry(self):
        if self.csv_registry is None:
            from BlackoutCSVRegistry import BlackoutCSVRegistry
            self.csv_registry = BlackoutCSVRegistry(self.path("blackouts.csv"))
        return self.csv_registry

    def get_gs_registry(self):
        if self.gs_registry is None:
            from BlackoutGSRegistry import BlackoutGSRegistry
            # sheet_name = 'DevSheet' if config.is_test() else 'GatewayPetrushky'
            config_spreadsheet = self.config.get_section('GOOGLE_SPREADSHEET')
            sheet_name = config_spreadsheet['SheetName']
            self.gs_registry = BlackoutGSRegistry(config_spreadsheet, sheet_name)

        return self.gs_registry
