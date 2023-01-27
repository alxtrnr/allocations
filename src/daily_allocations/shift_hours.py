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
    from datetime import datetime

    st = input("Enter start time in 24h format (HH:MM): ")
    et = input("Enter end time in 24h format (HH:MM): ")

    # convert input to datetime objects
    st = datetime.strptime(st, "%H:%M")
    et = datetime.strptime(et, "%H:%M")

    # calculate and round the duration to hours and minutes
    d = et - st
    total_seconds = d.total_seconds()
    hours, remainder = divmod(int(total_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)

    # format datetime objects to only include hours and minutes
    st_formatted = st.strftime("%H:%M")
    et_formatted = et.strftime("%H:%M")

    # print values
    print("Start time:", st_formatted)
    print("End time:", et_formatted)
    print("Duration: {} hours {} minutes".format(hours, minutes))

    # mid_times = []
    # hour = int(input('Start time: '))
    # minute = [0, 30]
    # even_odd = 1
    #
    # for i in range(16):
    #     if even_odd % 2 != 0:
    #         choice = 0
    #     else:
    #         choice = 1
    #
    #     t = datetime(year=NOW.year, month=NOW.month, day=NOW.day, hour=hour, minute=minute[choice],
    #                  microsecond=NOW.microsecond)
    #     mid_times.append(t.strftime('%H:%M'))
    #     even_odd += 1
    #
    #     if even_odd % 2 != 0:
    #         hour += 1
    #     if hour > 23:
    #         hour -= 24


custom_hours()
