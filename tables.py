import pandas as pd


def staff_on_duty():
    rmn = list(input('RMNs: ').split())
    hca = list(input('HCAs: ').split())

    team_dict = dict(zip(['RMNs' for n in range(len(rmn))], [[name for name in rmn]]))
    team_dict.update(dict(zip(['HCAs' for n in range(len(hca))], [[name for name in hca]])))

    team_df = pd.DataFrame(team_dict.items())
    team_df.columns = 'Role', 'Name'

    task_table(team_df)


def task_table(team_df):
    tasks = ['nurse in charge', 'security', 'medication', 'floor nurse', 'medication stock', 'drug charts audit', 'clinical room checks',
             'clinical room cleaning', 'AED/Grab Bags', 'Fridge Temperature', 'Store Room', 'Laundry Room',
             'Communal Areas Cleaning', 'Environmental Checks', 'Validating Pink Notes', 'Handover']

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
        print(team_df)
        print()
        task_table_dict[k] = input(f'allocate {k}: ').split()

    df = pd.DataFrame(task_table_dict.items())
    df.columns = ['Task', 'Name']

    print()
    print(df)


staff_on_duty()
