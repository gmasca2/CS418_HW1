import re

prof_name_list = []
prof_courses_list = []
prof_dict = {}

with open('class.txt', 'r') as class_file:
    line = class_file.readline()
    while line:
        prof_name_list.append(line.split('  - ')[0].title())    # populating name list
        courses = line.split('  - ')[1].split('|')
        courses[-1] = courses[-1].strip()  # To remove \n from last element of list
        for index, element in enumerate(courses):
            courses[index] = element.capitalize()
        prof_courses_list.append(courses)   # populating course list
        line = class_file.readline()

# processing various name patterns
for index, item in enumerate(prof_name_list):
    if re.findall('^\w+$', item):
        prof_name_list[index] = item
    # last_name, first_name
    elif re.findall('\w*,\s*\w*', item):
        prof_name_list[index] = item.split(',')[0]
    # first_name.last_name
    elif re.findall('[a-zA-Z]+\.[a-zA-Z]+', item):
        prof_name_list[index] = item.split('.')[1]
    # first_name last_name
    elif re.findall('^[a-zA-Z]+\s+[a-zA-Z]+$', item):
        prof_name_list[index] = item.split(' ')[1]
    # first_name middle_name last_name
    elif re.findall('^[a-zA-Z\.]+\s+[a-zA-Z\.]+\s[a-zA-Z]+$', item):
        prof_name_list[index] = item.split(' ')[2]
    else:
        print(item)
        print('Name format not encountered in test input class.txt, hence not handled')

# initializing dictionary key values
for item in set(prof_name_list):
    prof_dict[item] = []

# populating the dictionary, since last_name is assumed unique, same last names will just have their course_lists
# extended
for index, item in enumerate(prof_name_list):
    prof_dict[item].extend(prof_courses_list[index])

# sorting course lists for each prof, alphabetically
for name, course_list in prof_dict.items():
    course_list.sort()
    prof_dict[name] = course_list

# writing cleaned output to file
with open('cleaned.txt', 'w') as cleaned_file:
    for key in sorted(list(set(prof_name_list))):
        cleaned_file.write(key + ' - ' + '|'.join(prof_dict[key]) + '\n')



