


def nextDay(year, month, day):
  '''This is for the simple case when there are 30 days in every months'''
  if day<30:
    return year,month,day+1
  else:
    if month<12:
      return year, month+1,1
    else:
      return year+1,1,1
