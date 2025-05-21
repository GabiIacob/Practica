from datetime import datetime,timedelta
current_time=datetime.now()
one_day_ago= current_time- timedelta(days=1)
next_day=current_time+ timedelta(days=1)
print (current_time)
print (one_day_ago)
print(next_day)