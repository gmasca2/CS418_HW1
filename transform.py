from bs4 import BeautifulSoup
from datetime import datetime
import requests
import csv

url = 'https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions'
superbowl_page = requests.get(url).text

bs_object = BeautifulSoup(superbowl_page, 'lxml')

row_list = []
winning_team = []
win_count = []
losing_team = []
loss_count = []
venue = []
venue_count = []
complete_list = []

my_file = open('transformed.csv', 'w')

for data in range(1, 12, 2):
    label = bs_object.find_all('table')[1].contents[3].contents[0].contents[data].get_text().strip()
    row_list.append(label if label != 'Date/Season' else 'Year')
print(row_list)
complete_list.append(row_list)

for i in range(2, 118, 2):
    row_list = []
    for j in range(1, 12, 2):
        text = bs_object.find_all('table')[1].contents[3].contents[i].contents[j].get_text('$').strip()
        if j == 7 and ('OT' in text):   # Handling overtime cases, to be printed as '<score> OT'
            score = text.split(' ')[0]
            text = score + ' OT'
        else:
            d = text.index('$')
            text = text[0:d]
        if j == 3:
            datetime_obj = datetime.strptime(text, '%B %d, %Y')
            text = datetime_obj.year
        elif j == 5:
            winning_team.append(text)
            win_count.append(winning_team.count(text))
            text = text + " 0" + str(winning_team.count(text))
        elif j == 7:
            text = text.replace(u'\xa0', u'')
        elif j == 9:
            losing_team.append(text)
            loss_count.append(losing_team.count(text))
            text = text + " 0" + str(losing_team.count(text))
        elif j == 11:
            venue.append(text)
            venue_count.append(venue.count(text))
            text = text + " 0" + str(venue.count(text))
        row_list.append(text)
    if 'To be determined' in row_list[4]:   # Not including games which haven't been played
        continue
    print(row_list)
    complete_list.append(row_list)
with open('transformed.csv', 'a', newline='') as f1:
    the_writer = csv.writer(f1)
    for item_list in complete_list:
        the_writer.writerow(item_list)
my_file.close()

# Needs following modifications:
# Combine header row with general data row with a common for loop
# Conform to transform.csv norms stipulated in Piazza posts by TAs
