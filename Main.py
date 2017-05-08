# -*- coding: utf-8 -*-
import os
import csv
import argparse


class ParserCollisionsExceptions(Exception):
    """Cant be lower than 0"""
    pass


def parser_decorator(function):
    def communiacte():
        print("Parsing arguments...")
        return function()
    return communiacte


@parser_decorator
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="directory with enroll .csv files")
    parser.add_argument("group", type=str, help='term of the group in format "day week_type time_start - time_end "')
    parser.add_argument("subject", type=str, help="name of the subject (the same as file name)")
    parser.add_argument("max_collisions", type=int, help="max number of students with collisions")
    args = parser.parse_args()
    path = args.path
    group = args.group
    subject = args.subject
    try:
        max_collisions = args.max_collisions
        if max_collisions < 0:
            raise ParserCollisionsExceptions
    except ParserCollisionsExceptions:
        print("ParserCollisionsExceptions:")
        print("Number of possible collisions can't be lower than 0!")
        print()
    return path, group, subject, max_collisions


# creates a dictionary which keys are all available terms for classes, and values are default (0)
def init_dict():
    days = ['poniedzia³ek ', 'wtorek ', 'œroda ', 'czwartek ', 'pi¹tek ']
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


# checks, wheter the term has neither A nor B (so it occurs every week, in other words - it is AB)
def is_refactorable(term):
    tmp = term.split(" ")
    if tmp[1] != 'A' and tmp[1] != 'B':
        return 1
    else:
        return 0


# if term is AB, treat it as both A and B
def refactor_term(term):
    tmp = term.split(" ")
    term_A = str(tmp[0]) + ' A' + " ".join(tmp[1:])
    term_B = str(tmp[0]) + ' B' + " ".join(tmp[1:])
    return term_A, term_B


# get all .csv files from given path
def get_files(path):
    l = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            l.append(file)
    return l


# analises all files - everytime it finds a student that is given group (album_numbers list), 
# it increments the dictionary's value (the key is the group in which he/she has been found)
def fill_terms(terms, album_numbers, path):
    file_list = get_files(path)
    for file in file_list:
        with open(path+file, 'r') as csv_file:
            file_content = csv.reader(csv_file, delimiter=';')
            # flag tells if the following line is group name (if true)
            flag = False
            for line in file_content:
                if line and flag:
                    term = line[0]
                    flag = False
                # if current line is empty, then following line will be group name (or file end, but it won't change anything)
                if not line:
                    flag = True
                if line:
                    # if student (student's album number) is in album_numbers list, increment value in dict
                    if line[0] in album_numbers:
                        # if term is either A or B
                        if term in terms:
                            terms[term] += 1
                        # if term is AB, split it into term A and term B
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


# get all students from given group
def get_students(path, group, subject):
    group_term = group
    group_ids = []
    with open(path + subject, newline='') as csv_file:
        file_content = csv.reader(csv_file, delimiter=";")
        # if we find our group, we set flag True. Once we finish 
        # analising it (line is empty, all people from group were added), we break the operation
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


def print_results():
    pass


path, group, subject, max_collisions = parser()
terms = init_dict()
album_numbers = get_students(path, group, subject)
terms = fill_terms(terms, album_numbers, path)
for term in terms:
    if terms[term] < max_collisions:
        print(term, terms[term])

'''
wtorek 16:15 A ->   poniedzia³ek 17:50 (1), 19:30 (0)
                    wtorek 14:40 (3), 16:15 (1), 17:50 (3), 19:30 (0)
                    œroda 11:15 (3), 17:50 (0), 19:20 (0)
                    czwartek 14:40 (0), 16:15 (2), 19:30 (0)
                    pi¹tek 8:00 (3), 9:35 (3), 12:50 (2), 14:40 (3), 16:15 (2)
wtorek 17:50 A ->   poniedzia³ek 11:15 (2), 17:50 (3), 19:30 (0)
                    wtorek 17:50 (0), 19:30 (0)
                    œroda 11:15 (1), 17:50 (2), 19:20 (0)
                    czwartek 11:15 (3), 16:15 (2), 19:30 (0)
                    pi¹tek 8:00 (1), 9:35 (3), 12:50 (3), 14:40 (1), 16:15 (2)
œroda 8:00 A ->     poniedzia³ek 11:15 (3), 17:50 (2), 19:30 (0)
                    wtorek 14:40 (3), 17:50 (2), 19:30 (0)
                    œroda 8:00 (3), 11:15 (1), 17:50 (0), 19:30 (0)
                    czwartek 11:15 (3), 12:50 (3), 14:40 (2), 16:15 (2), 19:30 (0)
                    pi¹tek 8:00 (3), 12:50 (3), 14:40 (1), 16:15 (1)
œroda 17:50 A ->    poniedzia³ek 19:30 (0)
                    wtorek 16:15 (2), 17:50 (1), 19:30 (0)
                    œroda 17:50 (0), 19:30 (0)
                    czwartek 12:50 (2), 14:40 (3), 16:15 (1), 19:30 (0)
                    pi¹tek 8:00 (3), 14:40 (2)
'''
