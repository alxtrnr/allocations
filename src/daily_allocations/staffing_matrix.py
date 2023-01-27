import pandas as pd


def matrix(obs_hours, patients_on_ward):
    staffing_matrix = [[1, 1, 2, 1, 1],
                       [2, 2, 2, 1, 2],
                       [3, 2, 2, 1, 2],
                       [4, 2, 2, 1, 2],
                       [5, 2, 2, 1, 2],
                       [6, 2, 2, 1, 2],
                       [7, 2, 2, 1, 2],
                       [8, 2, 2, 2, 1],
                       [9, 2, 2, 2, 1],
                       [10, 2.5, 2, 2, 1],
                       [11, 2.5, 2, 2, 2],
                       [12, 2.5, 3, 2, 2],
                       [13, 2.5, 3, 2, 2],
                       [14, 2.5, 3, 2, 2],
                       [15, 2.5, 4, 2, 2],
                       [16, 2.5, 4, 2, 2]]

    extra_staff_needed = 0
    if obs_hours > 24 and patients_on_ward >= 11:
        difference = obs_hours - 24
        extra_staff_needed = difference / 12
        for hca in staffing_matrix:
            hca[2] += extra_staff_needed  # days
            hca[4] += extra_staff_needed  # nights
    elif obs_hours > 12 and patients_on_ward < 11:
        difference = obs_hours - 12
        extra_staff_needed = difference / 12
        for hca in staffing_matrix:
            hca[2] += extra_staff_needed  # days
            hca[4] += extra_staff_needed  # nights

    print(f'Staff above matrix to cover enhanced observations: {extra_staff_needed}')

    matrix_df = pd.DataFrame(staffing_matrix,
                             columns=['Number of Patients', 'Day RMN', 'Day SW', 'Night RMN', 'Night SW'])

    number_of_patients, day_rmn, day_sw, night_rmn, night_sw = staffing_matrix[patients_on_ward]
    print(f'\nDay RMN: {day_rmn}\nDay HCA: {day_sw}\nNight RMN: {night_rmn}\nNight HCA: {night_sw}')

    return matrix_df.set_index('Number of Patients')
