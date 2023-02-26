import datetime

from daily_allocations import staffing_matrix
from daily_allocations.sit_rep import summary
from daily_allocations import shift_hours

from datetime import timedelta
import pandas as pd

from sqlalchemy import Column, Integer, String, Boolean, Time, Float
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create an engine to carry on with the table. This is the SQLite engine. If echo is True, the log is visible:
# engine = create_engine('sqlite:///allocations_db/test1.db', echo=False)
engine = create_engine('sqlite:///example.db')

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

    # Set staff assigned. Single instance.
    if len(selected_staff) == 1:
        staff = selected_staff[0]
        staff.assigned = True
    # Set staff assigned. Reset staff values if not assigned. Group instance.
    else:
        for staff in all_rows:
            if staff in selected_staff:
                staff.assigned = True
            else:
                staff.assigned = False
                staff.start_obs = None
                staff.end_obs = None
                staff.shift_duration = 0
                staff.break_duration = 0

    # Set start and end times of observation span
    start, stop = 'time', 'time'
    allocate_for = input(f'allocate for: long day(1), nights(2), custom hours(3)\n')
    ds = {'08:00': '00:00',
          '09:00': '01:00',
          '10:00': '02:00',
          '11:00': '03:00',
          '12:00': '04:00',
          '13:00': '05:00',
          '14:00': '06:00',
          '15:00': '07:00',
          '16:00': '08:00',
          '17:00': '09:00',
          '18:00': '10:00',
          '19:00': '11:00',
          '20:00': '12:00'
          }
    ns = {'20:00': '00:00',
          '21:00': '01:00',
          '22:00': '02:00',
          '23:00': '03:00',
          '00:00': '04:00',
          '01:00': '05:00',
          '02:00': '06:00',
          '03:00': '07:00',
          '04:00': '08:00',
          '05:00': '09:00',
          '06:00': '10:00',
          '07:00': '11:00',
          '08:00': '12:00'
          }
    for staff in selected_staff:
        if allocate_for == '1':
            start, stop = ds['08:00'], ds['20:00']
        elif allocate_for == '2':
            start, stop = ns['20:00'], ns['08:00']

        elif allocate_for == '3':
            ask = input('Days or Nights: d/N')
            st = input(f"Enter {staff.name}\'s start time in 24h format (HH:MM): ")
            et = input(f"Enter {staff.name}\'s end time in 24h format (HH:MM): ")
            if ask == 'd':
                start, stop = ds[st], ds[et]
            else:
                start, stop = ns[st], ns[et]

        #  Convert strings to datetime objects to calculate obs duration
        staff.start_obs = (lambda start_str: datetime.datetime.strptime(start_str, '%H:%M').time())(start)
        staff.end_obs = (lambda end_str: datetime.datetime.strptime(end_str, '%H:%M').time())(stop)
        staff.shift_duration = (datetime.datetime.combine(datetime.date.today(), staff.end_obs) -
                                datetime.datetime.combine(datetime.date.today(), staff.start_obs)).seconds / 3600

        # Display confirmation of staff assigned to obs
        print(f'{staff.name} ({staff.role}) has been assigned for observations')

        # Use obs duration to calculate break duration
        if staff.shift_duration > 8:
            staff.break_duration = staff.shift_duration * 0.125
        elif staff.shift_duration == 8:
            staff.break_duration = staff.shift_duration * 0.0625
        else:
            staff.break_duration = 0

    session.commit()
    main_menu()


def staff_team_df():
    query = session.query(StaffTable)
    all_rows = query.all()
    data = [[row.id, row.name, row.role, row.assigned, row.start_obs, row.end_obs, row.shift_duration,
             row.break_duration] for row in all_rows]
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Role', 'Assigned', 'ObsStart', 'ObsEnd', 'ObsHrs',
                                     'BreakHrs'])
    all_staff = df.set_index('ID').sort_values(by='ID')
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
