import datetime


def get_date_to():
    weeks = 8
    days_added = datetime.timedelta(weeks=weeks)
    date_to = (datetime.datetime.now() + days_added).strftime("%Y-%m-%d")
    return date_to
