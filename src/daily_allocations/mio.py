from daily_allocations.sit_rep import input_data
import pandas as pd
from pulp import *


def add_machine_constraints(problem, staff, machines, two2one, three2one, times, x):
    # Constraints: each machine has staff assigned at all times between 08:00 and 19:00
    for j in machines:
        for k in times:
            # if the machine needs two staff members and is in two2one list, then assign two staff members to it
            if j in two2one:
                problem += lpSum([x[(i, j, k)] for i in staff]) == 2
            # if the machine needs three staff members and is in three2one list, then assign three staff members to it
            elif j in three2one:
                problem += lpSum([x[(i, j, k)] for i in staff]) == 3
            else:
                problem += lpSum([x[(i, j, k)] for i in staff]) == 1


def add_staff_constraints(problem, staff, machines, times, x):
    # Constraint: each staff member can be assigned to only one machine at a time
    for i in staff:
        for k in times:
            problem += lpSum([x[(i, j, k)] for j in machines]) <= 1


def add_consecutive_constraints(problem, staff, machines, times, x):
    # Constraint: staff members assigned to a machine for two consecutive hours cannot be assigned to any
    # machine for the next hour
    for i in staff:
        for j in machines:
            for k in range(10, 17):
                problem += (1 - x[(i, j, k)] - x[(i, j, k-1)] - x[(i, j, k-2)]) >= 0
                problem += x[(i, j, k)] + x[(i, j, k+1)] + x[(i, j, k+2)] <= 2 - z[(i, j, k+2)]


def add_break_constraints(problem, staff, machines, times, x, b):
    # Constraint: staff members are not assigned to a machine during their break time
    for i in staff:
        for j in machines:
            for k in range(12, 18):
                problem += x[(i, j, k)] <= 1 - b[(i, k)]


def add_min_break_constraints(problem, staff, machines, times, x, b):
    # Constraint: staff members have at least 90 minutes of break time between 12:00 and 19:00
    for i in staff:
        for k in range(12, 18):
            problem += lpSum([b[(i, t)] for t in range(k, k+2)]) >= 1 - lpSum([x[(i, j, t)] for j in machines for t in range(k, k+2)])
        for k in range(13, 18):
            problem += lpSum([b[(i, t)] for t in range(k, k+2)]) >= 1 - lpSum([x[(i, j, t)] for j in machines for t in range(k, k+2)])
        problem += lpSum([b[(i, 18)] for i in staff]) == 0


# define the input data model
sit_rep = input_data

# Define the variables
staff = ['Peter', 'John', 'Billy', 'William', 'Jane', 'Brian']
machines = ['Generals', 'AT']

two2one = ['AT']  # list of machines that need two staff members
three2one = []  # list of machines that need three staff members
times = range(8, 20)  # list of the shifts hours

# Binary variables to indicate whether a staff member is assigned to a machine at a specific time
x = LpVariable.dicts('x', [(i, j, k) for i in staff for j in machines for k in times], cat='Binary')

# Binary variables to indicate whether a staff member is on break at a specific time
b = LpVariable.dicts('b', [(i, k) for i in staff for k in times], cat='Binary')

# Binary variables to indicate whether a staff member is assigned to a machine at time k+2
z = LpVariable.dicts('z', [(i, j, k+2) for i in staff for j in machines for k in range(10, 17)], cat='Binary')


# Define the problem
problem = LpProblem("StaffAssignmentProblem", LpMinimize)

# Objective function: minimize the number of unassigned machines
problem += lpSum([1 - lpSum([x[(i, j, k)] for i in staff]) for j in machines for k in times])

# Add machine constraints
add_machine_constraints(problem, staff, machines, two2one, three2one, times, x)

# Add staff constraints
add_staff_constraints(problem, staff, machines, times, x)

# Add consecutive assignment constraints
add_consecutive_constraints(problem, staff, machines, times, x)

# Add break constraints
add_break_constraints(problem, staff, machines, times, x, b)

# Add minimum break time constraints
add_min_break_constraints(problem, staff, machines, times, x, b)

# set the logPath and keepFiles parameters to create a log of the MIP formulation
status = problem.solve(PULP_CBC_CMD(msg=0, logPath="log.txt", keepFiles=True))
problem.writeLP('allocations.lp')

# Check if there is a feasible solution with the current number of staff members
while problem.status != 1:
    # If there is no feasible solution, print the minimum number of staff required for a feasible solution
    print(f"Not enough staff members available. Try adding more staff.")
    break

    # Add a constraint to ensure that the minimum number of staff members required is available
    staff.append(f"New Staff {len(staff) + 1}")
    problem += lpSum([1 for i in range(len(staff))]) == len(staff)
    # Re-solve the problem with the additional staff member(s)
    status = problem.solve()

# Print the solution
print(f"Total cost: {int(value(problem.objective))}")
for i in staff:
        for j in machines:
            for k in times:
                if x[(i, j, k)].varValue == 1:
                    print(f"{i} allocated to {j} at {k}:00")

# Create a table to display the results
pd.set_option('display.max_columns', None)
results = pd.DataFrame(columns=machines, index=times)

for j in machines:
    for k in times:
        assigned_staff = [i for i in staff if x[(i, j, k)].varValue == 1]
        results.loc[k][j] = ', '.join(assigned_staff)

# Display the results
print('\nAllocations')
print(results)

# Display break times and machine assignments for each staff
df = pd.DataFrame(columns=staff, index=times)

for i in staff:
    for k in times:
        assigned_machine = None
        for j in machines:
            if value(x[(i, j, k)]) == 1:
                assigned_machine = j
                break
        if assigned_machine:
            df.at[k, i] = assigned_machine
        else:
            df.at[k, i] = "Off Obs"

print("\nBreak times and machine assignments for each staff:")
print(df)
