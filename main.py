def options():
    print('''
1: add staff
2: add patient observations
''')
    conduit()


def conduit():
    choice = int(input('type the choice number you require: '))
    if choice == 1:
        add_staff()
    elif choice == 2:
        one_to_ones_eyesight()


def add_staff():
    sn = int(input('How many staff on duty? '))
    team = [input('Enter staff name and designation: ').split() for x in range(sn)]
    collector(team)
    one_to_ones_eyesight()


def one_to_ones_eyesight():
    pn = int(input('How many patients on 1:1 eyesight: '))
    one2one_eyesight = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    collector(one2one_eyesight)
    one_to_ones_armslength()



def one_to_ones_armslength():
    pn = int(input('How many patients on 1:1 arms length: '))
    one2one_armslength = [input('Enter patient initials and room number: ').split() for x in range(pn)]
    collector(one2one_armslength)



def collector(*args):
    my_list = []
    my_list.append(args)
    print(my_list)

# print(o)
# #
#
# def one_to_ones_isolation():
#     pn = int(input('How many patients on 1:1 isolation: '))
#     one2one_isolation = [input('Enter patient initials and room number: ').split() for x in range(pn)]
#     seclusion()
#     return one2one_isolation
#
#
# def seclusion():
#     pn = int(input('How many patients in seclusion: '))
#     seclusion_room = [input('Enter patient initials and room number: ').split() for x in range(pn)]
#     two_to_ones()
#     return seclusion_room
#
#
# def two_to_ones():
#     pn = int(input('How many patients on 2:1 observations: '))
#     two2ones = [input('Enter patient initials, obs level and room number: ').split() for x in range(pn)]
#     return two2ones


options()

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
