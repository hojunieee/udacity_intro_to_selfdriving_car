def daysBetweenDates(year1, month1, day1, year2, month2, day2):
    """Returns the number of days between year1/month1/day1
       and year2/month2/day2. Assumes inputs are valid dates
       in Gregorian calendar."""
    assert not dateIsBefore(year2, month2, day2,year1, month1, day1)
    assert year1>1582
    assert year2>1582
    
    days = 0
    while dateIsBefore(year1, month1, day1, year2, month2, day2):
        year1, month1, day1 = nextDay(year1, month1, day1)
        days += 1
    return days


def nextDay(year, month, day):
  '''This is for the simple case when there are 30 days in every months'''
  if day<daysInMonth(year,month):
    return year,month,day+1
  else:
    if month<12:
        return year, month+1,1
    else:
        return year+1,1,1

    
def dateIsBefore(Y1,M1,D1,Y2,M2,D2):
    if Y1<Y2:
        return True
    if Y1==Y2:
        if M1<M2:
            return True
        if M1==M2:
            return D1<D2
    return False


def daysInMonth(Y1,M1):
    if M1 in [1,3,5,7,8,10,12]:
        return 31
    if M1 in [4,6,9,11]:
        return 30
    if M1 == 2:
        if isLeapYear(Y1):
            return 29
        else:
            return 28    
    
def isLeapYear(Y1):
    return Y1 % 4 == 0 and (Y1 % 100 != 0 or Y1 % 400 == 0)
