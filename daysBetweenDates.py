def daysBetweenDates(year1, month1, day1, year2, month2, day2):
    """Returns the number of days between year1/month1/day1
       and year2/month2/day2. Assumes inputs are valid dates
       in Gregorian calendar."""
    assert not dateIsBefore(year2, month2, day2,year1, month1, day1)
    
    days = 0
    while dateIsBefore(year1, month1, day1, year2, month2, day2):
        year1, month1, day1 = nextDay(year1, month1, day1)
        days += 1
    return days


def nextDay(year, month, day):
  '''This is for the simple case when there are 30 days in every months'''
  if day<30:
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


