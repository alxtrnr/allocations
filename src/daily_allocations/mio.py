from daily_allocations.sit_rep import input_data
import pandas as pd
from pulp import *

# define the input data model
sit_rep = input_data


# Define the problem
problem = LpProblem("StaffAssignmentProblem", LpMinimize)

# Define the variables
staff = [name[0] for name in sit_rep['STAFF_ON_OBS']]  # staff members
machines = ['Generals', 'Mo', 'Callum', 'Ben']  # machines
times = range(8, 21)  # times

# Binary variables to indicate whether a staff member is assigned to a machine at a specific time
x = LpVariable.dicts('x', [(i, j, k) for i in staff for j in machines for k in times], cat='Binary')

# Objective function: minimize the difference in number of assignments among staff
problem += lpSum([x[(i, j, k)] for i in staff for j in machines for k in times]) / (len(staff) * len(machines))

# Constraints: each machine has staff assigned at all times between 08:00 and 20:00
for j in machines:
    for k in times:
        problem += lpSum([x[(i, j, k)] for i in staff]) == 1

# Constraints: staff cannot be assigned to more than one machine at the same time
for i in staff:
    for k in times:
        problem += lpSum([x[(i, j, k)] for j in machines]) <= 1

# Constraint: staff cannot be assigned to the same machine for more than two consecutive hours
for i in staff:
    for j in machines:
        for k in range(8, 19):
            problem += x[(i, j, k)] + x[(i, j, k+1)] + x[(i, j, k+2)] <= 2

# Constraint: each staff member can be assigned to only one machine at a time
for i in staff:
    for k in times:
        problem += lpSum([x[(i, j, k)] for j in machines]) <= 1

# Solve the problem
status = problem.solve()

# Create a table to display the results
results = pd.DataFrame(index=times, columns=machines)
for j in machines:
    for k in times:
        assigned_staff = [i for i in staff if x[(i, j, k)].varValue == 1]
        if assigned_staff:
            results.loc[k, j] = str(assigned_staff)[1:-1]
        else:
            results.loc[k, j] = ''

# Print the solution as a table
print(results)


