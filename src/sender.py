from datetime import datetime, timedelta
from track_calendar import Calendar

class ConfigError(Exception): ...

class Sender:
    '''Handles days and time tracking'''
    def __init__(self, send_time: str, timespan: int, calendar: Calendar):
        try:
            self.send_time = datetime.strptime(send_time, "%H:%M").time()
        except Exception as e:
            raise ConfigError(e)
        self.last_sent_date = None
        self.calendar: Calendar = calendar
        self.timespan: int = timespan

    def is_to_send(self, datetime_now: datetime) -> bool:
        '''A function that returns whether or not the message should be sent now'''

        def is_in_timespan(time: datetime.time, target_time: datetime.time, timespan: int) -> bool:
            time_diff = datetime.combine(datetime.today(), time) - datetime.combine(datetime.today(), target_time)
            return (time_diff <  timedelta(minutes=timespan)
                and time_diff >= timedelta(minutes=0))
        
        return (self.last_sent_date is None or self.last_sent_date < datetime.date(datetime_now)) \
            and is_in_timespan(datetime_now.time(), self.send_time, self.timespan) \
            and self.calendar.is_workday(datetime_now.date())
    
    def get_remaining_days(self, datetime_now: datetime):
        return self.calendar.days_remain(datetime_now.date())
    
    def set_today_sent(self, datetime_now: datetime):
        self.last_sent_date = datetime.date(datetime_now)
