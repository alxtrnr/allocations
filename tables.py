import pandas as pd


def staff_table():
    data = []
    rmn = list(input('RMNs: ').split())  # [['Victor'], ['Nicola'], ['Gary'], ['Ravin']]
    rmn = [[x] for x in rmn]
    hca = list(input('HCAs: ').split())  # [['Victor'], ['Nicola'], ['Gary'], ['Ravin']]
    hca = [[x] for x in hca]
    # hca = [['Mo'], ['Coventry'], ['Elijah'], ['Jude'], ['Trevor'], ['Cedric'], ['Sheila'], ['Dennis'], ['Harry'], ['Bobby'],
    # ['Justine'], ['Adam']]
    team_dict = dict(zip(['RMNs' for n in range(len(rmn))], [[name for name in rmn]]))
    team_dict.update(dict(zip(['HCAs' for n in range(len(hca))], [[name for name in hca]])))

    # for v in team_dict.values():  # could be used to count and/or iterate hours and/or half hours?
    #     for i in v:
    #         i.append(int('11'))

    team_df = pd.DataFrame(team_dict.items())
    team_df.columns = 'Role', 'Name'
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    data.append(team_df)
    data.append(team_dict)
    observations_table(data)


def observations_table(data):
    """

    :param data: team_df, team_dict
    :return:
    """
    pn = int(input('How many patients on 1:1 eyesight: '))
    one2one_eyesight = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    # one2one_eyesight = [['CD', 11], ['ROM', 3], ['HD', 9],
    #                     ['LCD', 10]]  # for tests otherwise use comment out and use the two lines above
    observations_dict = dict(zip([x[0] for x in one2one_eyesight], [['eyes', x[1]] for x in one2one_eyesight]))

    pn = int(input('How many patients on 1:1 armslength: '))
    one2one_armslength = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    # one2one_armslength = [['LG', 8]]  # for tests otherwise use comment out and use the two lines above
    observations_dict.update(
        dict(zip([x[0] for x in one2one_armslength], [['arms', x[1]] for x in one2one_armslength])))

    pn = int(input('How many patients in isolation: '))
    one2one_isolation = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    # one2one_isolation = [['PP', 14]]  # for tests otherwise use comment out and use the two lines above
    observations_dict.update(
        dict(zip([x[0] for x in one2one_isolation], [['iso', x[1]] for x in one2one_isolation])))

    pn = int(input('How many patients in seclusion: '))
    seclusion_room = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    # seclusion_room = [['ZZ', 114]]  # for tests otherwise use comment out and use the two lines above
    observations_dict.update(dict(zip([x[0] for x in seclusion_room], [['sec', x[1]] for x in seclusion_room])))

    pn = int(input('How many patients on two2one: '))
    two2ones = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    # two2ones = [['KK', 23]]  # for tests otherwise use comment out and use the two lines above
    observations_dict.update(dict(zip([x[0] for x in two2ones], [['2:1', x[1]] for x in two2ones])))

    observations_df = pd.DataFrame(observations_dict.items())
    observations_df.columns = 'Patient Initials', 'Level & Room No.'

    obs_columns = []
    for index, row in observations_df.iterrows():
        obs_columns.append([row['Patient Initials'], row['Level & Room No.'][0], row['Level & Room No.'][1]])

    obs_allocations_df = pd.DataFrame(obs_columns)
    obs_allocations_df.columns = 'Patient Initials', 'Observation Level', 'Room Number'

    data.append(observations_df)
    data.append(observations_dict)
    data.append(obs_allocations_df)
    obs_allocations(data)


def obs_allocations(data):
    """

    :param data: [team_df, team_dict, observations_df, observations_dict, obs_allocations_df]
    :return:
    """
    hours_dict = {
        'time': [['08:00'], ['09:00'], ['10:00'], ['11:00'], ['12:00'], ['13:00'], ['14:00'], ['15:00'], ['16:00'],
                 ['17:00'], ['18:00'], ['19:00']]
    }

    # generates list of staff name. It works. Don't touch!
    staff_list = []
    for name in data[1]['HCAs']:  # HCAs first. TODO: include RMNs if HCA under number.
        staff_list.append(*name)  # * operator precludes using list comprehension

    p_dict = dict()
    for k, v in data[3].items():
        p_dict[k] = v[0]

    # updates hours_dict.values by appending a staff name (consecutively taken from staff_list) to each value in the
    # dictionary (an hour from 0800... to 1900hrs). The process repeats corresponding to patient_num
    patient_num = len(p_dict)
    obs_hours_to_cover = patient_num * 12
    num_of_staff_on_obs = len(staff_list)
    num_of_staff_list_copies = obs_hours_to_cover // num_of_staff_on_obs

    # Careful edits! Populates each_hour_list in the hours dictionary with staff allocated to Px on that hour.
    y = staff_list.copy() * num_of_staff_list_copies
    count = 1
    while count <= patient_num:
        staff_list_iter = iter(y)
        for hour in hours_dict.values():
            for each_hour_list in hour:
                each_hour_list.append(next(staff_list_iter))
        y.insert(0, y.pop())
        count += 1

    hour_and_staff_allocated = [v for k, v in hours_dict.items()]

    col_labels = []
    for initials, obs_level_and_room_no in data[3].items():
        col_labels.append(f'{initials} {obs_level_and_room_no[0]} {str(obs_level_and_room_no[1])}')

    allocations_df = pd.DataFrame()
    h_list_sans_hour = [x[1:] for x in
                        hour]  # removes index 0 (08:00...) from the hour list leaving just names allocated.

    for h_list in hour_and_staff_allocated:
        for h in h_list:
            allocations_df = pd.DataFrame(h_list_sans_hour)
    allocations_df.columns = [x for x in col_labels]
    allocations_df.index = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00',
                            '17:00', '18:00', '19:00']
    print()
    data.append(allocations_df)
    task_table(data)


def task_table(data):
    """

    :param data: [team_df, team_dict, observations_df, observations_dict, obs_allocations_df, allocations_df]
    :return:
    """
    tasks = ['Nurse in Charge', 'e-census', 'Observation Sheets', 'Security', 'Medication', 'Medication Stock',
             'Drug Charts Audit',
             'Clinical Room Checks', 'Clinical Room Cleaning', 'AED/Grab Bags', 'Floor Nurse', 'Fridge Temperature',
             'Store Room', 'Laundry Room', 'Communal Areas Cleaning', 'Environmental Checks', 'Validating Pink Notes',
             'Handover', 'Floater', 'Breakfast', 'Lunch', 'Dinner']

    print()
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    name = [[''] for i in range(len(tasks))]
    task_table_dict = dict(zip(tasks, name))

    for k, v in task_table_dict.items():
        x = k
        print()
        print('\n' * 50)
        print(data[5])
        print()
        print(data[0])
        print()
        task_table_dict[k] = input(f'allocate {k}: ').split()

    task_df = pd.DataFrame(task_table_dict.items())
    task_df.columns = ['Task', 'Name']
    data.append(task_df)
    display(data)


def display(data):
    """

    :param data: [team_df, team_dict, observations_df, observations_dict, obs_allocations_df, allocations_df, task_df]
    :return:
    """
    print(data[0])
    print()
    print(data[4])
    print()
    print(data[5])
    print()
    print(data[6])
    print()


staff_table()
