from datetime import datetime, timedelta


def create_shift_list(start_time, end_time):
    """
    Given start_time and end_time in string format of 'HH:MM', returns a list of
    half-hourly time stamps between the two times.

    Example:
    >> create_shift_list('08:00', '20:00')
    ['08:00', '08:30', '09:00', ..., '19:30', '20:00']

    Args:
    - start_time (str): start time in string format of 'HH:MM'
    - end_time (str): end time in string format of 'HH:MM'

    Returns:
    - list of half-hourly time stamps between start_time and end_time
    """
    start_time = datetime.strptime(start_time, "%H:%M")
    end_time = datetime.strptime(end_time, "%H:%M")

    # Add 1 day to end_time if start_time is after end_time
    if start_time > end_time:
        end_time = end_time + timedelta(days=1)

    duration = end_time - start_time
    total_minutes = int(duration.total_seconds() / 60)
    half_hours = total_minutes // 30
    shift_hours = []
    current_time = start_time

    for i in range(half_hours + 1):
        shift_hours.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=30)
        if current_time > end_time:
            break
    return shift_hours


def get_and_show_shift_hours(start_time, end_time):
    shift_hours = create_shift_list(start_time, end_time)
    print("Start time:", start_time)
    print("End time:", end_time)

    start_time = datetime.strptime(start_time, "%H:%M")
    end_time = datetime.strptime(end_time, "%H:%M")

    # Add 1 day to end_time if start_time is after end_time
    if start_time > end_time:
        end_time = end_time + timedelta(days=1)

    duration = end_time - start_time
    total_seconds = duration.total_seconds()
    hours, remainder = divmod(int(total_seconds), 3600)
    minutes, _ = divmod(remainder, 60)
    print("Duration: {} hours {} minutes".format(hours, minutes))
    print("Shift hours:", shift_hours)


def ld_hours():
    st = '08:00'
    et = '20:00'
    return create_shift_list(st, et)


def n_hours():
    st = '20:00'
    et = '08:00'
    return create_shift_list(st, et)


def custom_hours():
    st = input("Enter start time in 24h format (HH:MM): ")
    et = input("Enter end time in 24h format (HH:MM): ")
    return create_shift_list(st, et)

