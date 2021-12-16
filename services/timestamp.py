from datetime import datetime, time

class timestamp:
    def timestamp(self):
        dateTimeObj = datetime.now()
        day = dateTimeObj.day
        month = dateTimeObj.month
        year = dateTimeObj.year
        hour = dateTimeObj.hour
        minu = dateTimeObj.minute
        sec = dateTimeObj.second
        return day, month, year, hour, minu, sec