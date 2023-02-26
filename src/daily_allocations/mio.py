from daily_allocations.sit_rep import input_data
import pandas as pd
from pulp import *
from tabulate import tabulate

# define the input data model
sit_rep = input_data

staff = [{'name': name, 'start_time': int(start_time[:2]), 'end_time': int(end_time[:2])} for name, start_time, end_time
         in sit_rep['STAFF_ON_OBS']]

patients = [patient[1] for patient in sit_rep['ONE_TO_ONE']] + [patient[1] for patient in sit_rep['TWO_TO_ONE']]
patients.append('Generals')

two2one = [patient[1] for patient in sit_rep['TWO_TO_ONE']]  # list of patients that need two staff members
three2one = []  # list of patients that need three staff members

# define the observation hours
times = [n for n in range(1, 13)]
start_hour = times[0]
end_hour = times[-1]


def add_patient_constraints(problem, staff, patients, two2one, three2one, times, x):
    # Constraints: each patient has staff assigned at all times
    for j in patients:
        for k in times:
            # if the patient needs two staff members and is in two2one list, then assign two staff members to it
            if j in two2one:
                problem += lpSum([x[(i, j, k)] for i in staff]) == 2
            # if the patient needs three staff members and is in three2one list, then assign three staff members to it
            elif j in three2one:
                problem += lpSum([x[(i, j, k)] for i in staff]) == 3
            else:
                problem += lpSum([x[(i, j, k)] for i in staff]) == 1


def add_staff_constraints(problem, staff, patients, times, x):
    # Constraint: each staff member can be assigned to only one patient at a time within their availability window
    for s in staff:
        for k in times:
            problem += lpSum([x[(s['name'], j, k)] for j in patients]) <= 1
            problem += lpSum([x[(s['name'], j, k)] for j in patients]) <= k - s['start_time']
            problem += lpSum([x[(s['name'], j, k)] for j in patients]) <= s['end_time'] - k + 1


def add_consecutive_constraints(problem, staff, patients, times, x):
    # Constraint: staff members assigned to a patient for two consecutive times cannot be assigned to any
    # patient for the next hour
    for i in staff:
        for j in patients:
            for k in range(start_hour + 2, end_hour - 2):
                problem += (1 - x[(i, j, k)] - x[(i, j, k - 1)] - x[(i, j, k - 2)]) >= 0
                # problem += (1 - x[(i, j, k)] - x[(i, j, k-1)] - x[(i, j, k-2)]) >= 0
                problem += lpSum([x[(i, j, k)] for j in patients]) + lpSum([x[(i, j, k + 1)] for j in patients]) + \
                           lpSum([x[(i, j, k + 2)] for j in patients]) <= 2 - z[(i, j, k + 2)]


def add_break_constraints(problem, staff, patients, times, x):
    # Constraint: staff members are not assigned to a patient during their break time
    for i in staff:
        i_start = start_hour
        i_end = end_hour
        for j in patients:
            for k in range(start_hour + 2, end_hour - 1):
                if k >= i_start and k + 1 <= i_end:
                    if i in b:
                        problem += x[(i, j, k)] <= 1 - b[i, k]
                    else:
                        problem += x[(i, j, k)] <= 1


def add_min_break_constraints(problem, staff, patients, times, x, b):
    # Constraint: staff members have at least 90 minutes of break time
    for s in [s['name'] for s in staff]:
        s_dict = next((item for item in staff if item['name'] == s), None)
        if s_dict['end_time'] - s_dict['start_time'] < 12:
            min_break_time = 0.5  # 30 minutes
        else:
            min_break_time = 1.5  # 90 minutes

        for k in range(start_hour + 4, end_hour - 2):
            if k >= s_dict['start_time'] and k + 2 <= s_dict['end_time']:
                problem += lpSum([b[(s, t)] for t in range(k, k + 2)]) >= min_break_time - lpSum(
                    [x[(s, j, t)] for j in patients for t in range(k, k + 2)])

        # Constraint: staff members must have zero break time after their end time
        if s_dict['end_time'] < end_hour:
            problem += lpSum([b[(s, t)] for t in range(s_dict['end_time'], end_hour)]) == 0


def print_results(staff, patients, times, x):
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
    for i in staff:
        for j in patients:
            for k in times:
                if x[(i['name'], j, k)].varValue == 1:
                    print(f"{i['name']} allocated to {j} at {st[k]}")

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


# Binary variables to indicate whether a staff member is assigned to a patient at a specific time
x = LpVariable.dicts('x', [(s['name'], j, k) for s in staff for j in patients for k in times], cat='Binary')

# Binary variables to indicate whether a staff member is on break at a specific time
b = LpVariable.dicts('b', [(s['name'], k) for s in staff for k in times], cat='Binary')

# Binary variables to indicate whether a staff member is assigned to a patient at time k+2
z = LpVariable.dicts('z', [(s['name'], j, k + 2) for s in staff for j in patients for k in
                           range(start_hour + 2, end_hour - 2)], cat='Binary')

# Define the problem
problem = LpProblem("StaffAssignmentProblem", LpMinimize)

# Objective function: minimize the number of unassigned patients
problem += lpSum([1 - lpSum([x[(s['name'], j, k)] for j in patients]) for s in staff for k in times])

# Add patient constraints
add_patient_constraints(problem, [s['name'] for s in staff], patients, two2one, three2one, times, x)

# Add staff constraints with availability times
add_staff_constraints(problem, staff, patients, times, x)

# Add consecutive assignment constraints
add_consecutive_constraints(problem, [s['name'] for s in staff], patients, times, x)

# Add break constraints
add_break_constraints(problem, [s['name'] for s in staff], patients, times, x)

# Add minimum break time constraints
add_min_break_constraints(problem, staff, patients, times, x, b)

# set the logPath and keepFiles parameters to create a log of the MIP formulation
status = problem.solve(PULP_CBC_CMD(msg=False, logPath="log.txt", keepFiles=True))
problem.writeLP('allocations.lp')

# print the results
print(f"\nSolution Status: {LpStatus[status]}")
print_results(staff, patients, times, x)
