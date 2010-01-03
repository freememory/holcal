from datetime import date
from calendar import Calendar

class HolidayCalendar:
    """Abstract class representing a holiday calendar.
    
    Do not instantiate."""
    def is_weekend(self, d):
        raise NotImplementedError("Not implemented here")
    
    def is_business_day(self, d):
        raise NotImplementedError("Not implemented here")
    
    def is_holiday(self, d):
        raise NotImplementedError("Not implemented here")
    
class BasicHolidayCalendar(HolidayCalendar):
    """Basic Holiday Calendar expects a file in the following format(example):
    
    R 12-25 # Xmas
    R 1-1 # New Years
    R 7-4 # 4th of July
    W SU # Weekends
    H 2009-3-14 # Pi day!
    H 2009-10-24 # Avogadro
    E 2012-12-25 #The end of the world...Xmas is cancelled
    ...
    
    R indicates a recurring holiday, that occurs every year on the same day, and is in the form MM-DD
    W indicates weekend days, and is a string of characters in [MTWRFSU]
    E is an exception to a recurring holiday, and is in the format YYYY-MM-DD.
    H is a holiday, and like an exception, must be in the format YYYY-MM-DD
    
    The # is a comment, and causes the parser to ignore the rest of the line. There are no block comments."""
    days = ['M', 'T', 'W', 'R', 'F', 'S', 'U']
    def __init__(self, filename):
        self.holidays = []
        self.weekend_days = ''
        self.recurring_holidays = []
        self.recurring_exceptions = []
        self.__initialize_from_file(filename)
        
    def is_weekend(self, d):
        day = self.__class__.days[d.weekday()]
        return -1 != self.weekend_days.find(day)
    
    def is_holiday(self, d):
        recurrences = [date(d.year, int(r.split('-')[0]), int(r.split('-')[1])) for r in self.recurring_holidays]
        exception = d in exceptions
        holiday = d in recurrences or d in self.holidays
        return holiday and not exception
     
    def is_business_day(self, d):
        return not self.is_weekend(d) and not self.is_holiday(d)
 
    def __initialize_from_file(self, filename):
        actions = {'E': lambda l: self.__register_exception(l),
                   'R': lambda l: self.__register_recurrence(l),
                   'H': lambda l: self.__register_holiday(l),
                   'W': lambda l: self.__register_weekend(l)}
        
        with open(filename) as calfile:
            for line in calfile:
                if line[0] in actions.keys():
                    action = actions[line[0]]
                    action(self.__clean_entry(line[1:]))
                    
    def __clean_entry(self, line):
        line = line.strip()
        com = line.find('#')
        if com != -1:
            line = line[:com]
        return line
    
    def __full_date_entry(self, datestr):
        split = datestr.split('-')
        if len(split) != 3:
            raise Exception('Date entry should be full (YYYY-MM-DD), but is improperly formatted.')
        
        y,m,d = [int(split[0]), int(split[1]), int(split[2])]
        d = date(y,m,d)
        
        return d
    
    def __register_exception(self, exstr):
        self.recurring_exceptions.append(self.__full_date_entry(exstr))
    
    def __register_holiday(self, holstr):
        self.holidays.append(self.__full_date_entry(holstr))
     
    def __register_recurrence(self, recstr):
        if len(recstr.split('-')) != 2:
            raise Exception('Recurring Holiday entry should be in MM-DD format, but is improperly formatted.')
        
        self.recurring_holidays.append(recstr)
    
    def __register_weekend(self, wkendstr):
        for day in wkendstr:
            if day not in self.__class__.days:
                raise Exception('Weekend day not recognized.')
        
        self.weekend_days = wkendstr
    
    