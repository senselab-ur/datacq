#!/usr/bin/python

"""
@generate new CSV file everyday with current timestamps
ex: 04262016-135453.csv
"""

import timestamps

new_file = None

def generate_filename():
    filename = timestamps.generate()+'.csv'
    return filename

if __name__ == '__main__':
    filename = generate_filename()
    if filename != None:
        f = None
        try:
            f = open(filename, 'a')
        except Exception as err:
            print err
        finally:
            f.close()
        print "new file generated", filename
