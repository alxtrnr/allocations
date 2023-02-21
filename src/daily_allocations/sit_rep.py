from daily_allocations import staffing_matrix
from sqlalchemy import Column, Integer, String, Boolean, Time, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import shift_hours

Base = declarative_base()


class StaffTable(Base):
    __tablename__ = 'staff_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    assigned = Column(Boolean, default=False)
    start_obs = Column(Time)
    end_obs = Column(Time)
    shift_duration = Column(Float, default=12.5)
    break_duration = Column(Float, default=1.5)


class PatientTable(Base):
    __tablename__ = 'patient_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    observation_level = Column(String)
    room_number = Column(String)


# Connect to the database
engine = create_engine('sqlite:///example.db', echo=False)

# Reflect the schema of the database into SQLAlchemy classes
Base.metadata.create_all(engine)

# Create a session to access the data
Session = sessionmaker(bind=engine)
session = Session()
generals = 12

# Queries
queries = {
    'q_staff_on_obs':     session.query(StaffTable).filter_by(assigned=True),
    'q_generals':         session.query(PatientTable).filter(
        PatientTable.observation_level.in_(['60m', '30m', '15m'])).all(),
    'q_one_to_one':       session.query(PatientTable).filter_by(observation_level='1:1'),
    'q_two_to_one':       session.query(PatientTable).filter_by(observation_level='2:1'),
    'q_sec':              session.query(PatientTable).filter_by(observation_level='Seclusion'),
    'q_lts':              session.query(PatientTable).filter_by(observation_level='LTS'),
    'q_patients_on_ward': session.query(PatientTable).count(),
    'q_number_on_60s':    session.query(PatientTable).filter(PatientTable.observation_level == '60m').count(),
    'q_number_on_30s':    session.query(PatientTable).filter(PatientTable.observation_level == '30m').count(),
    'q_number_on_15s':    session.query(PatientTable).filter(PatientTable.observation_level == '15m').count(),
    'q_number_on_1to1':   session.query(PatientTable).filter(PatientTable.observation_level == '1:1').count(),
    'q_number_on_2to1':   session.query(PatientTable).filter(PatientTable.observation_level == '2:1').count(),
    'q_number_in_SEC':    session.query(PatientTable).filter(PatientTable.observation_level == 'Seclusion').count(),
    'q_number_in_LTS':    session.query(PatientTable).filter(PatientTable.observation_level == 'LTS').count()
}

# Input data
input_data = {
    'STAFF_ON_OBS':    [[staff.name, str(staff.start_obs), str(staff.end_obs)] for staff in queries['q_staff_on_obs']],
    'GENERALS':        [[patient.room_number, patient.name, patient.observation_level] for patient in
                        queries['q_generals']],
    'ONE_TO_ONE':      [[patient.room_number, patient.name, patient.observation_level] for patient in
                        queries['q_one_to_one']],
    'TWO_TO_ONE':      [[patient.room_number, patient.name, patient.observation_level] for patient in
                        queries['q_two_to_one']],
    'SEC':             [[patient.room_number, patient.name, patient.observation_level] for patient in queries['q_sec']],
    'LTS':             [[patient.room_number, patient.name, patient.observation_level] for patient in queries['q_lts']],
    'SHIFT_HOURS':     shift_hours.ld_hours(),
    'total_obs_hours': queries['q_number_on_1to1'] * 12 + queries['q_number_on_2to1'] * 24 + queries['q_number_in_SEC']
                       * 12 + queries['q_number_in_LTS'] * 12 + generals
}


def send_data():
    return input_data


# Data Frames
dict_df_obs = {
    'df_staff_on_obs': pd.DataFrame(input_data['STAFF_ON_OBS'], columns=['Name', 'Start', 'End'], index=None),
    'df_generals':   pd.DataFrame(input_data['GENERALS'], columns=['Room', 'Name', 'Obs Level']),
    'df_one_to_one': pd.DataFrame(input_data['ONE_TO_ONE'], columns=['Room', 'Name', 'Obs Level']),
    'df_two_to_one': pd.DataFrame(input_data['TWO_TO_ONE'], columns=['Room', 'Name', 'Obs Level']),
    'df_sec':        pd.DataFrame(input_data['SEC'], columns=['Room', 'Name', 'Obs Level']),
    'df_lts':        pd.DataFrame(input_data['LTS'], columns=['Room', 'Name', 'Obs Level']),
}


def summary():
    print(f"\nNo. of Patients on Ward: {queries['q_patients_on_ward']}\n")
    print(f"Number on 60m observations: {queries['q_number_on_60s']}")
    print(f"Number on 30m observations: {queries['q_number_on_30s']}")
    print(f"Number on 15m observations: {queries['q_number_on_15s']}")
    print(f"Number on 1:1: {queries['q_number_on_1to1']}")
    print(f"Number on 2:1: {queries['q_number_on_2to1']}")
    print(f"Number in seclusion: {queries['q_number_in_SEC']}")
    print(f"Number in LTS: {queries['q_number_in_LTS']}\n")
    print(f"Total enhanced observation hours: {input_data['total_obs_hours'] - generals}")
    print(f"Total observation hours: {input_data['total_obs_hours']}")
    staffing_matrix.calculate_staff_numbers(input_data['total_obs_hours'], queries['q_patients_on_ward'])
    print(f"Minimum staff number to cover all obs: Not Sure!!!")

    print('\nOBSERVATIONS')
    for key, query in list(dict_df_obs.items())[1:]:
        if not query.empty:
            print(f'{key}:')
            print(f'{query.to_string(index=False)}\n')
        else:
            pass

    print('\nFOR ALLOCATION')
    print(dict_df_obs['df_staff_on_obs'])


session.close()




# if __name__ == '__main__':
#     send_data()
