import datetime

date_1 = datetime.date.today()
date_2 = datetime.datetime.strptime('2023-04-22', "%Y-%m-%d").date()

print(date_1, date_2)
print(date_1 == date_2)
