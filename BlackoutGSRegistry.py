import gspread
from google.oauth2.service_account import Credentials
import json


class BlackoutGSRegistry:
    def __init__(self, config, sheetname):
        json_cred = json.loads('''{
           "type": "service_account",
           "project_id": "mythic-reach-234308",
           "private_key_id": "29824b4087152cd33e85cfeddbddb0741c6a8c03",
           "private_key": "''' + config['GooglePrivateKey'] + '''",
           "client_email": "colab-anon@mythic-reach-234308.iam.gserviceaccount.com",
           "client_id": "100248853631255137862",
           "auth_uri": "https://accounts.google.com/o/oauth2/auth",
           "token_uri": "https://oauth2.googleapis.com/token",
           "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
           "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/colab-anon%40mythic-reach-234308.iam.gserviceaccount.com"
         }''')

        # colab-anon@mythic-reach-234308.iam.gserviceaccount.com

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials = Credentials.from_service_account_info(
            json_cred,
            scopes=scopes
        )

        gc = gspread.authorize(credentials)

        spreadsheet = gc.open_by_url(
            'https://docs.google.com/spreadsheets/d/1ZLH7fvezsIXgZ2I_qq9v6smrVuUemFqQyA2DoEq9x4A/edit?usp=sharing')
        self.worksheet = spreadsheet.worksheet(sheetname)
        last_row_number = len(self.worksheet.col_values(1))
        row = self.worksheet.row_values(last_row_number)
        self.recent_timestamp = row[0]
        self.is_on = row[1]

    def add_record(self, is_on, timestamp):
        row = [timestamp, is_on]
        self.worksheet.append_row(row)
        self.is_on = is_on
        self.recent_timestamp = timestamp
