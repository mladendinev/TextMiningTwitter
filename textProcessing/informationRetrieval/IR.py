__author__ = 'mladen'
from datetime import timedelta
from datetime import datetime

import pytz
from pytz import UnknownTimeZoneError
#
# POD_EARLY_MORNING = 'Early morning'
# POD_LATE_MORNING = 'Late morning'
# POD_AFTERNOON = 'Afternoon'
# POD_LATE_AFTERNOON = 'Late afternoon'
# POD_EARLY_AFTERNOON = 'Early afternoon'
# POD_EARLY_EVENING = 'Early evening'
# POD_EVENING = 'Evening'
# POD_NIGHT = 'Night'

early_morning = "early_morning"
morning = "morning"
afternoon = 'afternoon'
evening = 'evening'


def format_date(date):
    format = datetime.strptime(date, '%a %b %d %H:%M:%S ' '+0000 %Y')
    return format


def get_part_of_the_day(ts):
    hour = ts.hour
    minute = ts.minute
    if minute > 45:
        hour += 1

    if 0 <= hour < 5:
        return early_morning
    elif 5 <= hour < 12:
        return morning
    elif 12 <= hour < 18:
        return afternoon
    elif 18 <= 0:
        return evening


def convertTimezoneToLocal(timezoneTweet):
    try:
        localTime = pytz.timezone(timezoneTweet)
        return localTime
    except UnknownTimeZoneError as e:
        print 'unknown'


def calculate_localtime(date, offset):
    date = format_date(date)
    offset /= 3600
    localtime = date + timedelta(hours=offset)
    return localtime

# h += 1
# if 5 <= h < 8:
#     return POD_MORNING, POD_EARLY_MORNING
# elif 11 <= h < 12:
#     return POD_MORNING, POD_LATE_MORNING
# elif 5 <= h < 12:
#     return POD_MORNING, POD_MORNING
# elif 13 <= h < 15:
#     return POD_AFTERNOON, POD_EARLY_AFTERNOON
# elif 16 <= h < 17:
#     return POD_AFTERNOON, POD_LATE_AFTERNOON
# elif 12 <= h < 17:
#     return POD_AFTERNOON, POD_AFTERNOON
# elif 17 <= h < 19:
#     return POD_EVENING, POD_EARLY_EVENING
# elif 17 <= h < 21:
#     return POD_EVENING, POD_EVENING
# elif h >= 21 or h <= 4:
#     return POD_NIGHT, POD_NIGHT
# return None, None
