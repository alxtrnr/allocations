import pandas as pd
from tabulate import tabulate
from pulp import *


def print_results(staff, patients, times, x, problem):
    ask = input('Allocating for long day or night shift d/N: ')
    if ask == 'd':
        st = {1: '08:00',
              2: '09:00',
              3: '10:00',
              4: '11:00',
              5: '12:00',
              6: '13:00',
              7: '14:00',
              8: '15:00',
              9: '16:00',
              10: '17:00',
              11: '18:00',
              12: '19:00'
              }
    else:
        st = {1: '20:00',
              2: '21:00',
              3: '22:00',
              4: '23:00',
              5: '00:00',
              6: '01:00',
              7: '02:00',
              8: '03:00',
              9: '04:00',
              10: '05:00',
              11: '06:00',
              12: '07:00'
              }

    # Print the solution
    print(f"Unassigned staff hours: {int(value(problem.objective))}")

    # Create a table to display the results
    pd.set_option('display.max_columns', None)

    # Define the start time for the schedule
    start_time = 8

    if ask == 'd':
        hours = [f"{hour:02}:00" for hour in range(8, 20)]
    else:
        hours = [f"{hour:02}:00" for hour in range(20, 24)] + [f"{hour:02}:00" for hour in range(0, 8)]
        start_time = 20

    # Create a new index for the results table using the hours list
    results = pd.DataFrame(columns=patients, index=hours)

    # Fill in the results table with staff assignments
    for j in patients:
        for k in times:
            assigned_staff = [i['name'] for i in staff if x[(i['name'], j, k)].varValue == 1]
            if ask == 'd':
                hour = k + start_time - 1
            else:
                hour = (k + start_time - 1) % 24
            results.loc[f"{hour:02}:00"][j] = ', '.join(assigned_staff)

    # Convert the table to a list of lists
    table = results.reset_index().values.tolist()

    # Display the table using tabulate
    print('\nAllocations')
    print(tabulate(table, headers=[''] + patients, tablefmt="fancy_grid"))

    # Display break times and patient assignments for each staff
    df = pd.DataFrame(columns=[s['name'] for s in staff], index=times)
    for i in staff:
        total_assigned = 0
        for k in times:
            assigned_patient = None
            for j in patients:
                if x[(i['name'], j, k)].varValue == 1:
                    assigned_patient = j
                    total_assigned += 1
                    break
            if assigned_patient:
                df.at[k, i['name']] = assigned_patient
            else:
                df.at[k, i['name']] = "Off Obs"
        df.at['TOTALS', i['name']] = total_assigned

    # change the row labels
    if ask == 'd':
        df.index = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00',
                    '19:00', 'TOTALS']
    else:
        df.index = ['20:00', '21:00', '22:00', '23:00', '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00',
                    '07:00', 'TOTALS']

    print("\nBreak times and patient assignments for each staff:")
    print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
