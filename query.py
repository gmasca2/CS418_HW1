import sys
import re
import itertools

argument_list = sys.argv
similar_courses = set()


# function for calculating jaccard similarity of two list of words
def jaccard(list_1, list_2):
    set_union = set(list_1 + list_2)
    set_intersection = set([x for x in list_1 if x in list_2])
    jac = len(set_intersection) / len(set_union)
    return jac


def Q1(file):
    # getting list of courses as set
    set_of_courses = set()

    # course_dict stores courses as keys and flag as value. flag and dictionary itself is used for better handling of
    # jaccard comparison between courses in the same data structure. Lists and sets didn't work for me
    course_dict = {}
    jaccard_set_of_courses = set()
    with open(file, 'r') as cleaned_file:
        line = cleaned_file.readline()
        while line:
            courses = line.split(' - ')[1]
            for part in courses.split('|'):
                set_of_courses.add(part.strip())
            line = cleaned_file.readline()
    for course in set_of_courses:
        course_dict[course] = 0  # initializing course_dict, values imply: 1 -> skip, 0 -> don't skip

    for course in course_dict.keys():
        similar_course_group = set()
        if course_dict[course] == 1:
            continue
        else:
            similar_course_group.add(course)
            course_dict[course] = 1
            jaccard_set_of_courses.add(course)
        for other_course in course_dict.keys():
            if len(course.split()) == len(other_course.split()):
                if course_dict[other_course] == 1:  # will ensure the course is not compared with itself
                    continue
                jac = jaccard(course.split(), other_course.split())

                # for # of words in course name >= 4, jaccard >= 0.6 => good similarity
                # for # of words in course name = 3, jaccard between 0.3 and 0.6 => good similarity
                # for # of words in course name = 1 or 2, character based jaccard is calculated, with 0.801 threshold
                if (len(course.split()) >= 4 and jac >= 0.6) or (
                        len(course.split()) == 3 and 0.3 <= jac < 0.6) or \
                        ((len(course.split()) == 1 or len(course.split()) == 2) and jaccard(list(course), list(
                            other_course)) >= 0.801):
                    similar_course_group.add(other_course)
                    course_dict[other_course] = 1
        similar_courses.add(similar_course_group)
    print(similar_courses)
    return len(jaccard_set_of_courses)


def Q2(file, prof_name):
    if re.findall('^\w+$', prof_name):
        prof_last_name = prof_name.title()
    # last_name, first_name
    elif re.findall('\w*,\s*\w*', prof_name):
        prof_last_name = prof_name.split(',')[0].title()
    # first_name.last_name
    elif re.findall('[a-zA-Z]+\.[a-zA-Z]+', prof_name):
        prof_last_name = prof_name.split('.')[1].title()
    # first_name last_name
    elif re.findall('^[a-zA-Z]+\s+[a-zA-Z]+$', prof_name):
        prof_last_name = prof_name.split(' ')[1].title()
    # first_name middle_name last_name
    elif re.findall('^[a-zA-Z\.]+\s+[a-zA-Z\.]+\s[a-zA-Z]+$', prof_name):
        prof_last_name = prof_name.split(' ')[2].title()
    else:
        print(prof_name)
        print('Name format not encountered in test input class.txt, hence not handled')
    with open(file, 'r') as cleaned_file:
        line = cleaned_file.readline()
        while line:
            if line.split(' - ')[0] == prof_last_name:
                courses = line.split(' - ')[1].replace('|', ', ')
            line = cleaned_file.readline()
    return courses


def Q3(file):
    prof_dict = {}
    with open(file, 'r') as cleaned_file:
        line = cleaned_file.readline()
        while line:
            temp_list = line.split(' - ')[1].split('|')
            temp_list[-1] = temp_list[-1].strip()
            prof_dict[line.split(' - ')[0]] = temp_list
            line = cleaned_file.readline()
    for (k1, v1), (k2, v2) in itertools.combinations(prof_dict.items(), 2):
        if len(v1) >= 5 and len(v2) >= 5:
            print(k1, k2, jaccard(v1,v2))


print(f"# of unique courses = {Q1(argument_list[1])}")
print(f"The courses taught by Professor {argument_list[2]} are: ", Q2(argument_list[1], argument_list[2]))
print('No professors found with most aligned teaching interests')
