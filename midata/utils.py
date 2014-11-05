from datetime import datetime

def parse_midata_datetime(date_string):
    date_string = date_string[0:-3] + date_string[-2:]
    date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
    return date
