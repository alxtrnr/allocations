def add_staff():
    data = []

    # sn = int(input('How many staff on duty? '))
    # team = [input('Enter staff name and designation: ').split() for x in range(sn)]
    team = [['Abdullah', 'HCA'], ['Brighton', 'HCA'], ['Emmanuel', 'HCA'], ['Jade', 'HCA'], ['Tina', 'HCA'],
            ['Anthony', 'HCA'], ['Ismalia', 'HCA'], ['Babatunde', 'HCA'], ['Chuck', 'HCA'], ['Becky', 'HCA'],
            ['Joseph', 'RMN'], ['Alex', 'RMN'], ['Walter', 'RMN']]
    team_dict = dict(zip([x[0] for x in team], [x[1] for x in team]))
    data.append(team_dict)
    one_to_ones_eyesight(data)


def one_to_ones_eyesight(data):
    # pn = int(input('How many patients on 1:1 eyesight: '))
    # one2one_eyesight = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    one2one_eyesight = [['DK', 11], ['JS', 3], ['SGM', 9], ['SJ', 10]]
    eyesight_dict = dict(zip([x[0] for x in one2one_eyesight], [x[1] for x in one2one_eyesight]))
    data.append(eyesight_dict)
    one_to_ones_armslength(data)


def one_to_ones_armslength(data):
    # pn = int(input('How many patients on 1:1 arms length: '))
    # one2one_armslength = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    one2one_armslength = [['JH', 8]]
    armslength_dict = dict(zip([x[0] for x in one2one_armslength], [x[1] for x in one2one_armslength]))
    data.append(armslength_dict)
    one_to_ones_isolation(data)


def one_to_ones_isolation(data):
    # pn = int(input('How many patients on 1:1 isolation: '))
    # one2one_isolation = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    one2one_isolation = [['PP', 14]]
    isolation_dict = dict(zip([x[0] for x in one2one_isolation], [x[1] for x in one2one_isolation]))
    data.append(isolation_dict)
    seclusion(data)


def seclusion(data):
    pn = int(input('How many patients in seclusion: '))
    seclusion_room = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    seclusion_dict = dict(zip([x[0] for x in seclusion_room], [x[1] for x in seclusion_room]))
    data.append(seclusion_dict)
    two_to_ones(data)


def two_to_ones(data):
    pn = int(input('How many patients on 2:1 observations: '))
    two2ones = [input('Enter patient initials, obs level and room number: ').split() for x in range(pn)]
    two2ones_dict = dict(zip([x[0] for x in two2ones], [x[1] for x in two2ones]))
    data.append(two2ones_dict)
    display(data)


def display(data):
    '''
    data is a list of dictionaries
    '''
    print(data)


add_staff()

#
# obs_list = []
# patient_observations = dict()
# data = input('Enter initials, observation level and room no. separated by ":" ').split(':')
#
# # Displaying the dictionary
# for key, value in patient_observations.items():
#     print(f'{key}, {value[0]}, {value[1]}')
#
# tasks = ['security', 'medication', 'floor nurse', 'medication stock', 'drug charts audit', 'clinical room checks',
#          'clinical room cleaning', 'AED/Grab Bags', 'Fridge Temperature', 'Store Room', 'Laundry Room',
#          'Communal Areas Cleaning', 'Environmental Checks', 'Validating Pink Notes', 'Handover']
#
# hour = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']
# headers = ['TASKS', 'NAME', 'TIME', 'Intermittent Observations', 'FLOAT', 'BREAK 30m', 'BREAK 60m']
#
# d = {
#     '08:00': None,
#     '09:00': None,
#     '10:00': None,
#     '11:00': None,
#     '12:00': None,
#     '13:00': None,
#     '14:00': None,
#     '15:00': None,
#     '16:00': None,
#     '17:00': None,
#     '18:00': None,
#     '19:00': None
# }
