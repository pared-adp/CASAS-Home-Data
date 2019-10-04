"""
cb: Bryton LeValley
demonstration of separating rooms for home project
might be an easier way, but I made the output files easily readable by postgres
"""


#pip install pathlib in terminal this is for mac compatability Just in case
from pathlib import Path
import csv

# !!!!change this if file is located somewhere else
data_path = "data/data.txt"

data_length = 3

i = 0

# this is the list for bedroom sensors note: not complete
Bedroom_list = ('M047','M045','M046','M048','M049','M050','M044','M043')

bedroom_out = ''
everything_else = ''
i = 0# used to break early for testing

with open(Path(data_path), 'r') as infile:
    file_reader = csv.reader(infile, delimiter='\t')

    for row in file_reader:
        row_string = ''
        i = i + 1

        # steps through each line in original file
        for x in range(len(row)):

            # checks if not Null and adds each row to a new row string while replacing the tab separator with commas
            if row[x] != '':
                row_string += row[x]
                row_string += ','

        # add an extra comma if there is no notes in the row
        # this makes the files work better with the pandas functions
        if len(row) < data_length:
            for x in range(len(row),data_length):
                row_string += ','

        # puts the row into bed_room if in the bedroom list
        # eventually every room will have a list
        if row[1] in Bedroom_list:
            bedroom_out = bedroom_out + '\n' + row_string
        # puts everything else into another file
        else:
            everything_else = everything_else + '\n' + row_string
        print(f'{i} = {row[1]}')

        # breaks at 100000 rows for demo purposes
        if i > 100000:
            break

#writes csv bedroom
with open('bedroom.csv', 'w+') as file:
    file.write(bedroom_out)

with open('everything_else.csv', 'w+') as file:
    file.write(everything_else)

"""
notes about the output file:
the comma at the end means there is another item at the end. it is just a empty string
"""