import datetime

from daily_allocations import staffing_matrix
from daily_allocations.sit_rep import summary

from datetime import timedelta

import pandas as pd
from daily_allocations import shift_hours
from sqlalchemy import Column, Integer, String, Boolean, Time, Float
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
    start_obs = Column(Time)
    end_obs = Column(Time)
    shift_duration = Column(Float, default=0)
    break_duration = Column(Float, default=0)


class PatientTable(Base):
    __tablename__ = 'patient_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    observation_level = Column(String)
    room_number = Column(String)


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
    5. Situation Report
    6. Exit
    """)

    if choice == '1':
        staff_menu()
    elif choice == '2':
        patient_menu()
    elif choice == '3':
        allocations_menu()
    elif choice == '4':
        sm, sm_df = staffing_matrix.matrix()
        print('\nBase Staffing Matrix\n')
        print(sm_df)
        main_menu()
    elif choice == '5':
        summary()
        main_menu()
    elif choice == '6':
        quit()


def patient_menu():
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

    if len(selected_staff) == 1:
        staff = selected_staff[0]
        staff.assigned = True
        allocate_for = input(f'allocate {staff.name} for: long day(1), nights(2), custom hours(3)\n')
        if allocate_for == '1':
            staff.start_obs = (lambda x: datetime.datetime.strptime(x, '%H:%M').time())('08:00')
            staff.end_obs = (lambda x: datetime.datetime.strptime(x, '%H:%M').time())('20:00')
            staff.shift_duration = (datetime.datetime.combine(datetime.date.today(), staff.end_obs) -
                                    datetime.datetime.combine(datetime.date.today(), staff.start_obs)).seconds / 3600

        elif allocate_for == '2':
            staff.start_obs = (lambda x: datetime.datetime.strptime(x, '%H:%M').time())('20:00')
            staff.end_obs = (lambda x: datetime.datetime.strptime(x, '%H:%M').time())('08:00')
            staff.shift_duration = (datetime.datetime.combine(datetime.date.today(), staff.end_obs) -
                                    datetime.datetime.combine(datetime.date.today(), staff.start_obs)).seconds / 3600

        elif allocate_for == '3':
            staff.start_obs = input(f"Enter {staff.name}\'s start time in 24h format (HH:MM): ")
            staff.end_obs = input(f"Enter {staff.name}\'s end time in 24h format (HH:MM): ")
            staff.shift_duration = (datetime.datetime.combine(datetime.date.today(), staff.end_obs) -
                                    datetime.datetime.combine(datetime.date.today(), staff.start_obs)).seconds / 3600

        print(f'{staff.name} ({staff.role}) has been assigned for observations from {staff.start_obs} to '
              f'{staff.end_obs}')
    else:
        for staff in all_rows:
            if staff in selected_staff:
                staff.assigned = True
            else:
                staff.assigned = False
                staff.start_obs = None
                staff.end_obs = None

        allocate_for = input(f'allocate for: long day(1), nights(2), custom hours(3)\n')
        print('\nAssigned for observations:')
        assigned_query = session.query(StaffTable).filter_by(assigned=True)
        for n, staff in enumerate(assigned_query):
            if allocate_for == '1':
                staff.start_obs = (lambda x: datetime.datetime.strptime(x, '%H:%M').time())('08:00')
                staff.end_obs = (lambda x: datetime.datetime.strptime(x, '%H:%M').time())('20:00')
            elif allocate_for == '2':
                staff.start_obs = (lambda x: datetime.datetime.strptime(x, '%H:%M').time())('20:00')
                staff.end_obs = (lambda x: datetime.datetime.strptime(x, '%H:%M').time())('08:00')
            elif allocate_for == '3':

                staff.start_obs = (lambda x: datetime.datetime.strptime(x, '%H:%M').time())('23:00')
                staff.end_obs = (lambda x: datetime.datetime.strptime(x, '%H:%M').time())(input("23:56"))
            print(f'{n + 1}. {staff.name} ({staff.role}) from {staff.start_obs} to {staff.end_obs}')
    session.commit()
    main_menu()
    return assigned_query


def staff_team_df():
    query = session.query(StaffTable)
    all_rows = query.all()
    data = [[row.id, row.name, row.role, row.assigned, row.start_obs, row.end_obs, row.shift_duration,
             row.break_duration] for row in all_rows]
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Role', 'Assigned', 'Obs Start', 'Obs End', 'Obs Duration',
                                     'Break Duration'])
    all_staff = df.set_index('ID').sort_values(by='Role')
    return all_staff


def patients_df():
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


if __name__ == '__main__':
    main_menu()
