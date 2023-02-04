from daily_allocations import staffing_matrix
from datetime import timedelta

import pandas as pd
from daily_allocations import shift_hours
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create an engine to carry on with the table. This is the SQLite engine. If echo is True, the log is visible:
engine = create_engine('sqlite:///allocations_db/test1.db', echo=False)

# Construct a sessionmaker object and bind it to the engine
Session = sessionmaker(bind=engine)
session = Session()

# declarative_base() is a factory function that constructs a base class for declarative class definitions.
Base = declarative_base()


# Defining declarative classes. They are assigned to the Base variable.
class StaffTable(Base):
    __tablename__ = 'staff_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    assigned = Column(Boolean, default=False)


class PatientTable(Base):
    __tablename__ = 'patient_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    observation_level = Column(String)
    room_number = Column(String)


class StaffOnObsTable(Base):
    __tablename__ = 'staff_on_obs_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    start_time = Column(String)
    end_time = Column(String)


# Create all the tables in the database which are defined by Base's subclasses
Base.metadata.create_all(engine)

OBS_LEVEL_DICT = {
    1: '60m',
    2: '15m',
    3: '30m',
    4: '1:1',
    5: '2:1',
    6: 'Seclusion',
    7: 'LTS'
}
TIME_STAMP = timedelta(minutes=30)
FULL_DURATION = TIME_STAMP * 25
MID_DURATION = TIME_STAMP * 15
FULL_BREAK_DURATION = TIME_STAMP * 3
MID_BREAK_DURATION = TIME_STAMP * 1


def main_menu():
    choice = input("""
    1. Staff Team
    2. Patient Group
    3. Allocate
    4. Staffing Matrix
    5. Working Data
    6. Exit
    """)

    if choice == '1':
        staff_menu()
    elif choice == '2':
        patient_menu()
    elif choice == '3':
        allocations_menu()
    elif choice == '4':
        staffing_matrix.matrix()
        main_menu()
    elif choice == '5':
        decision_variables_dashboard()
    elif choice == '6':
        quit()


def patient_menu():
    """
    This function displays the patient menu.
    It takes no arguments.
    It returns nothing.
    :return:
    """
    print("""
    1. Show patients' details 
    2. Add patient(s) details
    3. Modify patient(s) details
    4. Return to main menu
""")
    choice = int(input('Make selection: '))
    if choice == 1:
        print(patients_df())
        patient_menu()
    elif choice == 2:
        create_patient()
    elif choice == 3:
        update_patient()
    elif choice == 4:
        main_menu()


def staff_menu():
    """
    This function displays the staff menu, and allows the user to select an option.
    The options are:
        1. Show staff details
        2. Add staff
        3. Update staff
        4. Return to main menu
    The function will then call the appropriate function for the selected option.
    :return:
    """
    print("""
    1. Show staff details
    2. Add staff
    3. Update staff
    4. Return to main menu
""")
    choice = int(input('Make selection: '))
    if choice == 1:
        print(staff_team_df())
        staff_menu()
    elif choice == 2:
        create_staff()
    elif choice == 3:
        update_or_delete_staff()
    elif choice == 4:
        main_menu()


def allocations_menu():
    print("""
    1. Observation levels
    2. Assign staff
    3. Under development
    4. Return to main menu
""")
    choice = int(input('Make selection: '))
    if choice == 1:
        print(observations_df())
        allocations_menu()
    elif choice == 2:
        assign_staff_to_obs()
    elif choice == 3:
        print('under development')
        allocations_menu()
    elif choice == 4:
        main_menu()


def display_obs_levels_key():
    return """OBSERVATION LEVEL
    1: 60m
    2: 15m
    3: 30m
    4: 1:1
    5: 2:1
    6: Seclusion
    7: LTS
    """


def create_patient():
    print(display_obs_levels_key())

    # add patients to the table with session.add()
    session.add(PatientTable(room_number=int(input('Room Number: ')), name=input('Name: '),
                             observation_level=OBS_LEVEL_DICT[int(input('Observation Level: '))]))
    add_more_patients = input('add patient y/N: ')
    if add_more_patients == 'y':
        create_patient()

    # tell the Session to save the changes to the database and commit the transaction
    session.commit()
    patient_menu()


def update_patient():
    print(patients_df())
    patient_id_to_modify = int(input('enter ID of patient to modify: '))
    patient_to_modify = session.query(PatientTable).filter_by(id=patient_id_to_modify).first()
    print(f"{patient_to_modify.name} will be modified")
    print("""
    1. Room number
    2. Name
    3: Observation Level
    4. Delete Patient
    5. Return to main patient menu
    """)

    item_to_modify = int(input())
    if item_to_modify == 1:
        patient_to_modify.room_number = int(input('Room Number: '))
    elif item_to_modify == 2:
        patient_to_modify.name = input('Patient Name: ')
    elif item_to_modify == 3:
        print(display_obs_levels_key())
        patient_to_modify.observation_level = OBS_LEVEL_DICT[int(input('Observation Level: '))]
    elif item_to_modify == 4:
        session.delete(patient_to_modify)
    elif item_to_modify == 5:
        patient_menu()
    session.commit()
    patient_menu()


def delete_patient():
    """
This is a function that deletes a patient from the staff_table in a database using the SQLAlchemy library.

The function begins by printing the current state of the staff_table using the patient_table() function.

It then prompts the user to enter the ID of the patient they would like to delete. This ID is stored in the
patient_id_to_delete variable as an integer.

The function then uses the session.query() method to retrieve the patient with the specified ID from the staff_table.
This patient is stored in the patient_to_delete variable.

The function then prints the name of the patient that will be deleted.

Next, the function uses the session.delete() method to delete the patient from the staff_table.

The function then prompts the user to enter 'y' if they would like to delete more patients. If the user enters 'y', the
function calls itself again to delete more patients. If the user enters anything else, or if the user doesn't enter any
input, the function moves on to the next step.

Finally, the function uses the session.commit() method to save the changes to the database and commit the transaction.
It then calls the patient_menu() function.
    """
    print(patients_df())

    patient_id_to_delete = int(input('enter ID of patient to delete: '))
    patient_to_delete = session.query(StaffTable).get(patient_id_to_delete)

    print(f"Name: {patient_to_delete.patient_name} will be deleted")

    # delete patient from the table with session.delete()
    session.delete(patient_to_delete)

    delete_more_patients = input('delete more patients y/N: ')
    if delete_more_patients == 'y':
        delete_patient()

    # tell the Session to save the changes to the database and commit the transaction
    session.commit()
    patient_menu()


def create_staff():
    # add staff to the table with session.add()
    session.add(StaffTable(name=input('Staff Name: '), role=input('Staff Role: ')))
    add_more_staff = input('add staff y/N: ')
    if add_more_staff == 'y':
        create_staff()
    # tell the Session to save the changes to the database and commit the transaction
    session.commit()
    staff_menu()


def update_or_delete_staff():
    print(staff_team_df())
    staff_id_to_update = int(input('enter ID of staff to update: '))
    staff_to_update = session.query(StaffTable).filter_by(id=staff_id_to_update).first()
    print(f"{staff_to_update.name} will be updated")
    print("""
    1. Update Name
    2. Update Role 
    3. Delete Staff
    4. Staff Menu
    5. Main Menu
    """)
    update_menu_selection = int(input())

    # update name
    if update_menu_selection == 1:
        staff_to_update.name = input('Name: ')
    # update role
    elif update_menu_selection == 2:
        staff_to_update.role = input('Role: ')
    # delete staff
    elif update_menu_selection == 3:
        check = input(f"Delete: {staff_to_update.name} y/N: ")
        if check == 'y':
            session.delete(staff_to_update)
        else:
            update_or_delete_staff()
    # menus
    elif update_menu_selection == 4:
        staff_menu()
    elif update_menu_selection == 5:
        main_menu()

    session.commit()
    update_or_delete_staff()


def assign_staff_to_obs():
    query = session.query(StaffTable)
    all_rows = query.all()
    print('\n', staff_team_df())

    select_staff = [staff_id for staff_id in input('\nID of staff to assign on obs: ').split()]
    selected_staff = [session.query(StaffTable).get(staff_id) for staff_id in select_staff]

    for staff in all_rows:
        if staff in selected_staff:
            staff.assigned = True
        else:
            staff.assigned = False
    session.commit()

    print('\nAssigned to undertake observations:')
    assigned_query = session.query(StaffTable).filter_by(assigned=True)
    for n, staff in enumerate(assigned_query):
        print(f'{n + 1}. {staff.name} ({staff.role})')
    print('\n', staff_team_df())
    main_menu()
    return assigned_query


def staff_team_df():
    """
This function creates a pandas DataFrame from the StaffTable object of an SQLAlchemy session.
The DataFrame contains the staff's name, role, hours, and ID, and is sorted by role.
The function returns the DataFrame.
"""
    query = session.query(StaffTable)
    all_rows = query.all()
    data = [[row.id, row.name, row.role, row.assigned] for row in all_rows]
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Role', 'Assigned on obs'])
    all_staff = df.set_index('ID').sort_values(by='Role')
    return all_staff


def patients_df():
    """
    Here's what the function is doing
1.    The function starts by creating a query from the PatientTable class in the session.
2.    The query is then executed to retrieve all the rows from the table.
3.    The retrieved rows are then stored in a list and converted into a DataFrame.
4.    The DataFrame is then set to be indexed by Room Num and sorted by Room Num.
5.    Finally, the DataFrame is returned.
    """
    query = session.query(PatientTable)
    all_rows = query.all()
    data = [[row.id, row.name, row.observation_level, row.room_number] for row in all_rows]
    df = pd.DataFrame(data, columns=['id', 'Patient Name', 'Observation Level', 'Room Num'])
    patients = df.set_index('id').sort_values(by='Room Num')
    return patients


def observations_df():
    # Select patients according to observation level
    obs_query_60m = session.query(PatientTable).filter(PatientTable.observation_level == '60m')
    obs_query_30m = session.query(PatientTable).filter(PatientTable.observation_level == '30m')
    obs_query_15m = session.query(PatientTable).filter(PatientTable.observation_level == '15m')
    one_2_one_obs_query = session.query(PatientTable).filter(PatientTable.observation_level == '1:1')
    two_2_one_obs_query = session.query(PatientTable).filter(PatientTable.observation_level == '2:1')
    seclusion_obs_query = session.query(PatientTable).filter(PatientTable.observation_level == 'Seclusion')
    lts_obs_query = session.query(PatientTable).filter(PatientTable.observation_level == 'LTS')

    # Pull out patient details from each respective row.
    obs_60m = [[patient.name, patient.observation_level, patient.room_number] for patient in obs_query_60m]
    obs_30m = [[patient.name, patient.observation_level, patient.room_number] for patient in obs_query_30m]
    obs_15m = [[patient.name, patient.observation_level, patient.room_number] for patient in obs_query_15m]
    obs_one_2_one = [[patient.name, patient.observation_level, patient.room_number] for patient in one_2_one_obs_query]
    obs_two_2_one = [[patient.name, patient.observation_level, patient.room_number] for patient in two_2_one_obs_query]
    obs_seclusion = [[patient.name, patient.observation_level, patient.room_number] for patient in seclusion_obs_query]
    obs_lts = [[patient.name, patient.observation_level, patient.room_number] for patient in lts_obs_query]
    data = obs_60m + obs_30m + obs_15m + obs_one_2_one + obs_two_2_one + obs_seclusion + obs_lts
    df = pd.DataFrame(data, columns=['Name', 'Observation Level', 'Room No.'])
    # df.set_index('Room No.', inplace=True)
    df.sort_values(by='Room No.', ascending=True, inplace=True)

    print(df)

    main_menu()


def decision_variables_dashboard():
    totals = {
        'patients_on_ward': session.query(PatientTable).count(),
        'number_on_60s':    session.query(PatientTable).filter(PatientTable.observation_level == '60m').count(),
        'number_on_30s':    session.query(PatientTable).filter(PatientTable.observation_level == '30m').count(),
        'number_on_15s':    session.query(PatientTable).filter(PatientTable.observation_level == '15m').count(),
        'number_on_1:1':    session.query(PatientTable).filter(PatientTable.observation_level == '1:1').count(),
        'number_on_2:1':    session.query(PatientTable).filter(PatientTable.observation_level == '2:1').count(),
        'number_in_SEC':    session.query(PatientTable).filter(PatientTable.observation_level == 'Seclusion').count(),
        'number_in_LTS':    session.query(PatientTable).filter(PatientTable.observation_level == 'LTS').count(),
        'assigned_staff':   session.query(StaffTable).filter_by(assigned=True)
    }

    generals = 12
    total_obs_hours = totals['number_on_1:1'] * 12 + totals['number_on_2:1'] * 24 + totals['number_in_SEC'] * 12 + \
                      totals['number_in_LTS'] * 12 + generals

    print(f"\nNumber of Patients on Ward: {totals['patients_on_ward']}")
    print(f"Number on 60m observations: {totals['number_on_60s']}")
    print(f"Number on 30m observations: {totals['number_on_30s']}")
    print(f"Number on 15m observations: {totals['number_on_15s']}")
    print(f"Number on 1:1: {totals['number_on_1:1']}")
    print(f"Number on 2:1: {totals['number_on_2:1']}")
    print(f"Number in seclusion: {totals['number_in_SEC']}")
    print(f"Number in LTS: {totals['number_in_LTS']}\n")
    print(f'Total enhanced observation hours: {total_obs_hours - generals}')
    staffing_matrix.calculate_staff_numbers(total_obs_hours, totals['patients_on_ward'])
    print('\nStaff selected to complete observations')
    for n, staff in enumerate(totals['assigned_staff']):
        print(f'{n + 1}. {staff.name} ({staff.role})')

    main_menu()

    return tc


if __name__ == '__main__':
    main_menu()
