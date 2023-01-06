import logging

from Toolkit import Toolkit

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

toolkit = Toolkit()

csv_registry = toolkit.get_csv_registry()

logging.info("Open gs registry...")
gs_registry = toolkit.get_gs_registry()

logging.info("Uploading new records...")
gs_ts = gs_registry.recent_timestamp
for row in csv_registry.rows():
    if row['timestamp'] > gs_ts:
        logging.info("Uploading record: " + str(row))
        gs_registry.add_record(row['is_on'], row['timestamp'])

logging.info("All data processed")
