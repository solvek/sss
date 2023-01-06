import csv


class BlackoutCSVRegistry:
    def __init__(self, file):
        self.file = file
        for row in self.rows():
            self.recent_timestamp = row['timestamp']
            self.is_on = row['is_on']

    def add_record(self, is_on, timestamp):
        with open(self.file, mode='a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([timestamp, is_on])

        self.recent_timestamp = timestamp
        self.is_on = is_on

    def rows(self):
        is_header = True
        with open(self.file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if is_header:
                    is_header = False
                else:
                    yield {'timestamp': float(row[0]), 'is_on': int(row[1])}
