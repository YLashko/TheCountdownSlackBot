from datetime import date, timedelta
import holidays

class Calendar:
    '''To keep track of holidays and calculate the remaining workdays'''
    def __init__(self, country: str = 'PL', include_today: bool = False):
        self.calculated_workdays: dict[int, list[bool]] = {}
        self.calculated_days_remain: dict[int, list[int]] = {}
        self.holidays = holidays.country_holidays(country)
        self.include_today = include_today

    def calculate_year(self, year: int) -> None:
        '''"Compile" a calendar for a specific year'''
        self.calculated_workdays[year] = []
        self.calculated_days_remain[year] = []
        date_iter = date(year, 1, 1)
        workdays_counter = 0

        while date_iter.year == year:
            is_holiday = date_iter.strftime("%Y-%m-%d") in self.holidays \
                      or date_iter.weekday() in (5, 6)
            
            if not self.include_today and not is_holiday:
                workdays_counter += 1

            self.calculated_workdays[year].append(not is_holiday)
            self.calculated_days_remain[year].append(workdays_counter)
            date_iter += timedelta(days=1)

            if self.include_today and not is_holiday:
                workdays_counter += 1
        
        self.calculated_days_remain[year] = [
            workdays_counter - days_remain
            for days_remain in self.calculated_days_remain[year]
        ]

    def is_workday(self, date_: date) -> bool:
        days_since_new_year = (date_ - date(date_.year, 1, 1)).days
        if date_.year not in self.calculated_workdays.keys():
            self.calculate_year(date_.year)
        return self.calculated_workdays[date_.year][days_since_new_year]
        
    def days_remain(self, date_: date) -> int:
        days_since_new_year = (date_ - date(date_.year, 1, 1)).days
        if date_.year not in self.calculated_days_remain.keys():
            self.calculate_year(date_.year)
        return self.calculated_days_remain[date_.year][days_since_new_year]
