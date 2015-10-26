import os
import sys
import logging
import json
from django.core.management.base import BaseCommand
from dateutil import parser as date_parser
from measurements.models import Measurement
from django.db.utils import IntegrityError

logger = logging.getLogger(__name__)

UNIT_CONVERSION_FACTOR = {
    'mV': 0.001,
    'cV': 0.01,
    'C16': 1./16,
    '%': 1,
    'h': 1,
    'C': 1,
}

def convert_units(val, units):
    if units == None: # unit less
        return val
    elif units not in UNIT_CONVERSION_FACTOR: # unrecognised units
        return None
    return val * UNIT_CONVERSION_FACTOR[units]

class Command(BaseCommand):
    help = 'Help'

    def add_arguments(self, parser):
        parser.add_argument('data_file', nargs='?', default='measurements/trial_data/201501.json')

    def handle(self, *args, **options):
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
        handler.setFormatter(formatter)

        f = open(options['data_file'], 'rb')

        measurements = []
        unrecognised_units = set()
        for line in f:
            datum = json.loads(line)
            datetime = date_parser.parse(datum[0])
            sensor = datum[2]
            if sensor == {}:
                continue
            if '@' not in sensor:
                logger.warning('sensor_id not found in: {}'.format(line))
            sensor_id = sensor['@']
            loop_id = sensor['+'] if '+' in sensor else None
            for key, val in sensor.iteritems():
                if key in ['@', '+']:
                    continue
                split = key.split('|')
                measurement_type = split[0]
                units = split[1] if len(split) == 2 else None
                measurement = Measurement(**{
                    'datetime': datetime,
                    'sensor_id': sensor_id,
                    'loop_id': loop_id,
                    'type': measurement_type,
                    'units': units,
                    'val': val,
                    'val_converted': convert_units(val, units)
                })
                if measurement.val_converted == None:
                    unrecognised_units.add(units)
                measurements.append(measurement)
                # measurement.save()

        logger.info('measurements: {}'.format(len(measurements)))
        logger.info('measurements[:10]: {}'.format(measurements[:10]))
        logger.info('unrecognised_units: {}'.format(unrecognised_units))
        
        for i, measurement in enumerate(measurements):
            # print i,
            # sys.stdout.flush()
            try:
                measurement.save()
            except IntegrityError as e:
                logger.error(e)

        # import time
# import datetime
# import logging
# from data_science_jobs.data_aggregation.background import update_daily_summaries, update_monthly_summaries, logger as bg_logger
# from django.utils import timezone
# from dateutil.parser import parse as parse_date
# from django.core.management.base import BaseCommand
# from data_science_jobs import scraping
# from data_science_jobs.scraping import Scraper
# from data_science_jobs.scraping.models import Session

# logger = logging.getLogger(__name__)

# def convert_start_to_datetime(start):
#     if start == None:
#         return timezone.now() #datetime.datetime.now()
#     else:
#         return parse_date(start)

# def wait_till_start_time(start):
#     now = scraping.get_now()
#     if start - now < datetime.timedelta(seconds=0):
#         time.sleep(0)
#     else:
#         time.sleep((start - now).total_seconds())

# def wait_till_next_session(seconds):
#     time.sleep(seconds)
        
# class Command(BaseCommand):
#     help = 'Closes the specified poll for voting'

#     def add_arguments(self, parser):
#         parser.add_argument('--start', help='Start datetime, ISO 8601 format (default: now)', default=None)
#         parser.add_argument('--frequency', type=int, help='Scraping Frequency in seconds (default: 1 day)', default=86400)
#         parser.add_argument('--log', type=str, help='Log filepath', default='scraper.log')
        
#     def handle(self, *args, **options):
#         logger.setLevel(logging.INFO)
#         handler = logging.StreamHandler()
#         handler.setLevel(logging.INFO)
#         logger.addHandler(handler)
#         formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
#         handler.setFormatter(formatter)
#         scraping.logger.setLevel(logging.INFO)
#         scraping.logger.addHandler(handler)
#         logger.propagate = False
#         file_handler = logging.FileHandler(options['log'])
#         file_handler.setLevel(logging.INFO)
#         file_handler.setFormatter(formatter)
#         logger.addHandler(file_handler)
#         scraping.logger.addHandler(file_handler)
#         bg_logger.setLevel(logging.INFO)
#         bg_logger.addHandler(handler)
#         bg_logger.addHandler(file_handler)

#         start_datetime = convert_start_to_datetime(start=options['start'])
#         scraper = Scraper()
#         wait_till_start_time(start_datetime)
#         while True:
#             logger.info('Current datetime: {}'.format(datetime.datetime.now()))
#             previous_session = Session.get_previous_session()
#             logger.info('Previous Session: {}'.format(previous_session.datetime if previous_session else previous_session))
#             scraper.configure(start_datetime, previous_session)
#             scraper.scrape()
#             update_daily_summaries()
#             update_monthly_summaries()
#             next_datetime = start_datetime + datetime.timedelta(seconds=options['frequency'])
#             start_datetime = next_datetime
#             logger.info('next scraping session: {}\n'.format(next_datetime))
#             if timezone.now() > next_datetime:
#                 continue
#             wait_till_next_session((next_datetime - timezone.now()).total_seconds())

