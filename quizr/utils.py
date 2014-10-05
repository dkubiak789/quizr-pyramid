import csv


ANSWER_IDS = ['A', 'B', 'C', 'D', 'E']


def get_questions(filename):
    """
    Reads data from CSV file.
    """
    with open(filename, 'rb') as csvfile:
        line = csv.reader(csvfile, delimiter=';')
        return [[unicode(cell, 'utf-8') for cell in row] for row in line]