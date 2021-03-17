def add_hca():
    data = []

    # hca_num = int(input('How many HCA on shift? '))
    # hca = [input('Enter HCA name: ') for x in range(hca_num)]
    # hca_dict = dict(zip([x for x in hca], ['HCA' for n in range(len(hca))]))
    hca = [['Mo'], ['Coventry'], ['Elijah'], ['Jude'], ['Trevor'],
           ['Cedric'], ['Sheila'], ['Dennis'], ['Harry'], ['Bobby']]
    hca_dict = dict(zip([x[0] for x in hca], ['HCA' for n in range(len(hca))]))
    data.append(hca_dict)
    add_rmn(data)


def add_rmn(data):
    # rmn_num = int(input('How many RMN on shift? '))
    # rmn = [input('Enter RMN name: ') for x in range(rmn_num)]
    # rmn_dict = dict(zip([x for x in rmn], ['RMN' for n in range(len(rmn))]))
    rmn = [['Victor'], ['Nicola'], ['Gary']]
    rmn_dict = dict(zip([x[0] for x in rmn], ['RMN' for n in range(len(rmn))]))
    data.append(rmn_dict)
    one_to_ones_eyesight(data)


def one_to_ones_eyesight(data):
    """
        :param data: [dictionaries]

        index   dictionary name
        0:      team_dict

        :return: data.append(eyesight_dict)
        """
    # pn = int(input('How many patients on 1:1 eyesight: '))
    # one2one_eyesight = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    one2one_eyesight = [['DK', 11], ['JS', 3], ['SGM', 9], ['SJ', 10]]
    eyesight_dict = dict(zip([x[0] for x in one2one_eyesight], [x[1] for x in one2one_eyesight]))
    data.append(eyesight_dict)
    one_to_ones_armslength(data)


def one_to_ones_armslength(data):
    """
        :param data: [dictionaries]

        index   dictionary name
        0:      team_dict
        1:      eyesight_dict

        :return: data
        """
    # pn = int(input('How many patients on 1:1 arms length: '))
    # one2one_armslength = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    one2one_armslength = [['JH', 8]]
    armslength_dict = dict(zip([x[0] for x in one2one_armslength], [x[1] for x in one2one_armslength]))
    data.append(armslength_dict)
    one_to_ones_isolation(data)


def one_to_ones_isolation(data):
    """
        :param data: [dictionaries]

        index   dictionary name
        0:      team_dict
        1:      eyesight_dict
        2:      armslength_dict

        :return: data
        """
    # pn = int(input('How many patients on 1:1 isolation: '))
    # one2one_isolation = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    one2one_isolation = [['PP', 14]]
    isolation_dict = dict(zip([x[0] for x in one2one_isolation], [x[1] for x in one2one_isolation]))
    data.append(isolation_dict)
    seclusion(data)


def seclusion(data):
    """
        :param data: [dictionaries]

        index   dictionary name
        0:      team_dict
        1:      eyesight_dict
        2:      armslength_dict
        3:      isolation_dict

        :return: data
        """
    pn = int(input('How many patients in seclusion: '))
    seclusion_room = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    seclusion_dict = dict(zip([x[0] for x in seclusion_room], [x[1] for x in seclusion_room]))
    data.append(seclusion_dict)
    two_to_ones(data)


def two_to_ones(data):
    """
        :param data: [dictionaries]

        index   dictionary name
        0:      team_dict
        1:      eyesight_dict
        2:      armslength_dict
        3:      isolation_dict
        4:      seclusion_dict

        :return: data
        """
    pn = int(input('How many patients on 2:1 observations: '))
    two2ones = [input('Enter patient initials, obs level and room number: ').split() for x in range(pn)]
    two2ones_dict = dict(zip([x[0] for x in two2ones], [x[1] for x in two2ones]))
    data.append(two2ones_dict)
    calculate_hours(data)


def calculate_hours(data):
    hca_hours = 9.5 * len(data[0])
    rmn_hours = 9.5 * len(data[1])
    eyesight_hours = 11 * len(data[2])
    armslength_hours = 11 * len(data[3])
    isolation_hours = 11 * len(data[4])
    seclusion_hours = 11 * len(data[5])
    two2one_hours = 11 * len(data[6])
    total_one2ones = len(data[2]) + len(data[3]) + len(data[4]) + len(data[5])
    total_one2one_hours = total_one2ones * 11
    hca_allocation = total_one2one_hours / len(data[0])
    print(hca_hours, rmn_hours, eyesight_hours, armslength_hours, isolation_hours, seclusion_hours, two2one_hours)
    print(total_one2ones)
    print(f'hca_allocation: {hca_allocation}')





def display(data):
    """
    :param data: [dictionaries]

    index   dictionary name
    0:      team_dict
    1:      eyesight_dict
    2:      armslength_dict
    3:      isolation_dict
    4:      seclusion_dict
    5:      two2ones_dict

    :return: data
    """
    for d in data:
        print(d)



add_hca()

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
