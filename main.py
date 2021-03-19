from colorama import Fore

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
    one2one_eyesight = [['CD', 11], ['ROM', 3], ['HD', 9], ['LCD', 10]]
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
    one2one_armslength = [['LG', 8]]
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
    # pn = int(input('How many patients in seclusion: '))
    # seclusion_room = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    seclusion_room = [['ZZ', 114]]
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
    # pn = int(input('How many patients on 2:1 observations: '))
    # two2ones = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    two2ones = [['KK', 23]]
    two2ones_dict = dict(zip([x[0] for x in two2ones], [x[1] for x in two2ones]))
    data.append(two2ones_dict)
    intermittent_observations(data)


def intermittent_observations(data):
    intermittent = 11
    data.append(intermittent)
    calculate_hours(data)


def calculate_hours(data):
    """

    :param data:
    :return:
    """
    # print()
    # print(f'Data: {data}')
    # print()

    hca_hours = 9.5 * len(data[0])
    print(f'No. of HCA on shift: {len(data[0])}')
    print(f'HCA hours: {hca_hours}\n')

    rmn_hours = 9.5 * len(data[1])
    print(f'No. of RMN on shift: {len(data[1])}')
    print(f'RMN hours: {rmn_hours}\n')

    eyesight_hours = 11 * len(data[2])
    print(f'No. of patents on 1:1 eyesight: {len(data[2])}')
    print(f'Eyesight hours: {eyesight_hours}')

    armslength_hours = 11 * len(data[3])
    print(f'No. of patents on 1:1 armslength: {len(data[3])}')
    print(f'Armslength hours: {armslength_hours}')

    isolation_hours = 11 * len(data[4])
    print(f'No. of patents in isolation: {len(data[4])}')
    print(f'Isolation hours: {isolation_hours}')

    seclusion_hours = 11 * len(data[5])
    print(f'No. of patents in seclusion: {len(data[5])}')
    print(f'Seclusion Hours: {seclusion_hours}\n')

    two2one_hours = 11 * len(data[6])
    print(f'No. of patents on two2one: {len(data[6])}\n')

    total_one2one_hours = eyesight_hours + armslength_hours + isolation_hours + seclusion_hours
    total_observation_hours = total_one2one_hours + two2one_hours + data[7]

    print(Fore.LIGHTGREEN_EX + f'Total one2one hours: {total_one2one_hours}', Fore.RESET)
    print(Fore.LIGHTGREEN_EX + f'Total two2one hours: {two2one_hours}', Fore.RESET)
    print(Fore.LIGHTGREEN_EX + f'Total intermittent hours: {data[7]}')
    print(Fore.LIGHTGREEN_EX + f'Total observation hours to cover: {total_observation_hours}')

    no_of_obs_per_hca = total_observation_hours / len(data[0])
    print(Fore.LIGHTGREEN_EX + f'Number of observations per HCA: {no_of_obs_per_hca}', Fore.RESET)











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
