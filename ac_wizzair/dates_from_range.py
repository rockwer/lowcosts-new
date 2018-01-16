from datetime import timedelta, datetime
import calendar
from time import sleep

def get_dates_range(dateFrom, dateTo):
    dateFrom_raw = datetime.strptime(dateFrom[0:10], '%Y-%m-%d')
    dateTo_raw = datetime.strptime(dateTo[0:10], '%Y-%m-%d')
    dates_list_raw = []
    for n in range(int((dateTo_raw - dateFrom_raw).days) + 1):
        dates_list_raw.append(dateFrom_raw + timedelta(n))
    dates_list_datetime_format = []
    # print(dates_list_raw)
    previous_date = datetime.now()
    # print(previous_date)
    last_days = []
    is_in_list = False
    for d in dates_list_raw:
        if d.month == previous_date.month and is_in_list == False:
            dates_list_datetime_format.append(d)
            last_day = calendar.monthrange(d.year, d.month)
            last_days.append(last_day[:][1])
            is_in_list = True
        elif d.month != previous_date.month:
            dates_list_datetime_format.append(d)
            previous_date = d
            # print(previous_date)
            last_day = calendar.monthrange(d.year, d.month)
            last_days.append(last_day[:][1])
    # print(dates_list_datetime_format)
    # print(last_days)
    new_dates_list_to = []
    index = 0
    for y in last_days:
        new_datee = str(dates_list_datetime_format[index].year) + "-" + str('%02d' % dates_list_datetime_format[index].month) + "-" + str(y)
        new_dates_list_to.append(new_datee)
        index += 1
    new_dates_list_from = []
    # print(new_dates_list_from)
    # print(new_dates_list_to)
    for ds in dates_list_datetime_format:
        new_dates_list_from.append(ds.strftime("%Y-%m-%d"))
    # print(new_dates_list_from)
    dates_dic = {}
    dates_dic["dates_from"], dates_dic["dates_to"] = new_dates_list_from, new_dates_list_to
    return dates_dic


# dateFrom = "2018-01-16T00:00:00"
# dateTo = "2018-02-26T00:00:00"
#
# dates_range = get_dates_range(dateFrom, dateTo)
# # print(dates_range)
# request_index = 0
# while request_index < len(dates_range['dates_from']):
#     # print(request_index)
#     date_from = dates_range['dates_from'][request_index]
#     date_to = dates_range['dates_to'][request_index]
#     request_index += 1
#     sleep(1)
#     # print(date_from)
#     # print(date_to)