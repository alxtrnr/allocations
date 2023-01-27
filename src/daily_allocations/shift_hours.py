from datetime import datetime

NOW = datetime.now()


def ld_hours():
    long_day_times = []
    hour = 8
    minute = [0, 30]
    even_odd = 1

    for i in range(24):
        if even_odd % 2 != 0:
            choice = 0
        else:
            choice = 1
        t = datetime(year=NOW.year, month=NOW.month, day=NOW.day, hour=hour, minute=minute[choice],
                     microsecond=NOW.microsecond)
        long_day_times.append(t.strftime('%H:%M'))
        even_odd += 1

        if even_odd % 2 != 0:
            hour += 1

    return long_day_times


def n_hours():
    night_times = []
    hour = 20
    minute = [0, 30]
    even_odd = 1

    for i in range(24):
        if even_odd % 2 != 0:
            choice = 0
        else:
            choice = 1
        t = datetime(year=NOW.year, month=NOW.month, day=NOW.day, hour=hour, minute=minute[choice],
                     microsecond=NOW.microsecond)
        night_times.append(t.strftime('%H:%M'))

        even_odd += 1
        if even_odd % 2 != 0:
            hour += 1
        if hour > 23:
            hour -= 24

    return night_times


def custom_hours():
    mid_times = []
    hour = int(input('Start time: '))
    minute = [0, 30]
    even_odd = 1

    for i in range(16):
        if even_odd % 2 != 0:
            choice = 0
        else:
            choice = 1

        t = datetime(year=NOW.year, month=NOW.month, day=NOW.day, hour=hour, minute=minute[choice],
                     microsecond=NOW.microsecond)
        mid_times.append(t.strftime('%H:%M'))
        even_odd += 1

        if even_odd % 2 != 0:
            hour += 1
        if hour > 23:
            hour -= 24

    return mid_times


