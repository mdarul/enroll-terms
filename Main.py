import os
import csv
import argparse

'''
TO DO
- dodać możliwość wyboru katalogu z plikami i terminu, obsługa błędów wyżej wymienionych (EDIT - już tylko obsługa błędów)
- traktowanie terminu bez 'A' lub 'B' jako 'AB' (EDIT - zrobione, przetestować)
- dodać możliwość wyboru dokładności (maksymalna liczba studentów którym może kolidować) (EDIT - done)

(poniższe trzeba doczytać by zrobić)
- własne wyjątki
- dekoratory
- loggery
- wrzucić na gita
- możliwość zainstalowania jako pakiet za pomocą pip'a
'''


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="directory with enroll .csv files")
    parser.add_argument("group", type=str, help='term of the group in format "day week_type time_start - time_end "')
    parser.add_argument("subject", type=str, help="name of the subject (the same as file name)")
    args = parser.parse_args()
    path = args.path
    group = args.group
    subject = args.subject
    return path, group, subject


def init_dict():
    days = ['poniedziałek ', 'wtorek ', 'środa ', 'czwartek ', 'piątek ']
    letters = ['A ', 'B ']
    hours = ['8:00 - 9:30', '9:35 - 11:05', '11:15 - 12:45', '12:50 - 14:20', '14:40 - 16:10', '16:15 - 17:45', '17:50 - 19:20', '19:30 - 21:00']
    terms = []
    for day in days:
        for letter in letters:
            for hour in hours:
                terms.append(day + letter + hour)
    output_dict = dict(())
    for term in terms:

        tmp = dict({term: 0})
        output_dict.update(tmp)
    return output_dict


def is_refactorable(term):
    tmp = term.split(" ")
    if tmp[1] != 'A' and tmp[1] != 'B':
        return 1
    else:
        return 0


def refactor_term(term):
    tmp = term.split(" ")
    term_A = str(tmp[0]) + ' A' + " ".join(tmp[1:])
    term_B = str(tmp[0]) + ' B' + " ".join(tmp[1:])
    return term_A, term_B


def fill_terms(terms, album_numbers, path):
    file_list = os.listdir(path)
    for file in file_list:
        with open(path+file, 'r') as csv_file:
            file_content = csv.reader(csv_file, delimiter=';')
            flag = False
            for line in file_content:
                if line and flag:
                    term = line[0]
                    flag = False
                if not line:
                    flag = True
                if line:
                    if line[0] in album_numbers:
                        if term in terms:
                            terms[term] += 1
                        if is_refactorable(term):
                            term_A, term_B = refactor_term(term)
                            if term_A in terms:
                                terms[term_A] += 1
                            else:
                                pass
                            if term_B in terms:
                                terms[term_B] += 1
                            else:
                                pass
    return terms


def get_students(path, group, subject):
    group_term = group
    group_ids = []
    with open(path + subject, newline='') as csv_file:
        file_content = csv.reader(csv_file, delimiter=";")
        flag = False
        for line in file_content:
            if flag and not line:
                break
            if flag and line:
                group_ids.append(line[0])
            if line:
                if line[0] == group_term:
                    flag = True
    return group_ids


path, group, subject = parser()
terms = init_dict()
album_numbers = get_students(path, group, subject)
terms = fill_terms(terms, album_numbers, path)
wspolczynnik_litosci = 300
for term in terms:
    if terms[term] < wspolczynnik_litosci:
        print(term, terms[term])


'''
wtorek 16:15 A ->   poniedziałek 17:50 (1), 19:30 (0)
                    wtorek 14:40 (3), 16:15 (1), 17:50 (3), 19:30 (0)
                    środa 11:15 (3), 17:50 (0), 19:20 (0)
                    czwartek 14:40 (0), 16:15 (2), 19:30 (0)
                    piątek 8:00 (3), 9:35 (3), 12:50 (2), 14:40 (3), 16:15 (2)

wtorek 17:50 A ->   poniedziałek 11:15 (2), 17:50 (3), 19:30 (0)
                    wtorek 17:50 (0), 19:30 (0)
                    środa 11:15 (1), 17:50 (2), 19:20 (0)
                    czwartek 11:15 (3), 16:15 (2), 19:30 (0)
                    piątek 8:00 (1), 9:35 (3), 12:50 (3), 14:40 (1), 16:15 (2)

środa 8:00 A ->     poniedziałek 11:15 (3), 17:50 (2), 19:30 (0)
                    wtorek 14:40 (3), 17:50 (2), 19:30 (0)
                    środa 8:00 (3), 11:15 (1), 17:50 (0), 19:30 (0)
                    czwartek 11:15 (3), 12:50 (3), 14:40 (2), 16:15 (2), 19:30 (0)
                    piątek 8:00 (3), 12:50 (3), 14:40 (1), 16:15 (1)

środa 17:50 A ->    poniedziałek 19:30 (0)
                    wtorek 16:15 (2), 17:50 (1), 19:30 (0)
                    środa 17:50 (0), 19:30 (0)
                    czwartek 12:50 (2), 14:40 (3), 16:15 (1), 19:30 (0)
                    piątek 8:00 (3), 14:40 (2)
'''