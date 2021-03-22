import pandas as pd


def staff_table():
    data = []
    rmn = [['Victor'], ['Nicola'], ['Gary']]  # list(input('RMNs: ').split())
    hca = [['Mo'], ['Coventry'], ['Elijah'], ['Jude'], ['Trevor'],
           ['Cedric'], ['Sheila'], ['Dennis'], ['Harry'], ['Bobby']]  # list(input('HCAs: ').split())
    team_dict = dict(zip(['RMNs' for n in range(len(rmn))], [[name for name in rmn]]))
    team_dict.update(dict(zip(['HCAs' for n in range(len(hca))], [[name for name in hca]])))

    for v in team_dict.values():
        for i in v:
            i.append(int('11'))

    team_df = pd.DataFrame(team_dict.items())
    team_df.columns = 'Role', 'Name'
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    data.append(team_df)
    data.append(team_dict)

    print()
    print(team_dict)
    print()
    # print(team_df)

    observations_table(data)


def observations_table(data):
    """

    :param data: team_df, team_dict
    :return:
    """
    # pn = int(input('How many patients on 1:1 eyesight: '))
    # one2one_eyesight = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    one2one_eyesight = [['CD', 11], ['ROM', 3], ['HD', 9],
                        ['LCD', 10]]  # for tests otherwise use comment out and use the two lines above
    observations_dict = dict(zip([x[0] for x in one2one_eyesight], [['eyesight', x[1]] for x in one2one_eyesight]))

    # pn = int(input('How many patients on 1:1 armslength: '))
    # one2one_armslength = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    one2one_armslength = [['LG', 8]]  # for tests otherwise use comment out and use the two lines above
    observations_dict.update(
        dict(zip([x[0] for x in one2one_armslength], [['armslength', x[1]] for x in one2one_armslength])))

    # pn = int(input('How many patients in isolation: '))
    # one2one_isolation = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    one2one_isolation = [['PP', 14]]  # for tests otherwise use comment out and use the two lines above
    observations_dict.update(
        dict(zip([x[0] for x in one2one_isolation], [['isolation', x[1]] for x in one2one_isolation])))

    # pn = int(input('How many patients in seclusion: '))
    # seclusion_room = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    seclusion_room = [['ZZ', 114]]  # for tests otherwise use comment out and use the two lines above
    observations_dict.update(dict(zip([x[0] for x in seclusion_room], [['seclusion', x[1]] for x in seclusion_room])))

    # pn = int(input('How many patients on two2one: '))
    # two2ones = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    two2ones = [['KK', 23]]  # for tests otherwise use comment out and use the two lines above
    observations_dict.update(dict(zip([x[0] for x in two2ones], [['two2one', x[1]] for x in two2ones])))

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

    day_shift_dict = {
        '': ['', '', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
             '18:00', '19:00']
    }
    day_shift_dict.update(data[3])
    print()
    print('day shift dict =', day_shift_dict)
    print()

    for k, v in day_shift_dict.items():
        if len(v) < 12:
            count = 0
            while count < 12:
                v.append(None)
                count += 1

    # for k, v in day_shift_dict.items():
    #     for i in v:
    #         if i is None:
    #             day_shift_dict[k] = data[1]['HCAs'][0][0]
    # print(day_shift_dict)

    allocations_df = pd.DataFrame(day_shift_dict,
                                  index=['Obs Level', 'Room No', '', '', '', '', '', '', '', '', '', '', '', ''])
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    print()
    print(allocations_df)
    data.append(allocations_df)
    print()

    allocations_df.iloc[2][1] = data[1]['HCAs'][0][0]
    for i in allocations_df['CD'][2:]:
        print(i)
    print(allocations_df)
    print()







    # task_table(data)
    # display(data)


def task_table(data):
    """

    :param data: [team_df, observations_df, observations_dict, obs_allocations_df, allocations_df]
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
        print(data[0])
        print()
        task_table_dict[k] = input(f'allocate {k}: ').split()

    task_df = pd.DataFrame(task_table_dict.items())
    task_df.columns = ['Task', 'Name']
    data.append(task_df)
    display(data)


def display(data):
    """

    :param data: team_df, observations_df, observations_dict, obs_allocations_df, allocations_df, task_df
    :return:
    """

    print()
    print(data[0])
    print()
    print(data[3])
    print()
    print(data[4])
    print()
    # print(data[5])


staff_table()
