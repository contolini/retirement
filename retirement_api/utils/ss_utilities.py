import os
# import sys
import json
import datetime

today = datetime.datetime.now().date()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# sys.path.append(BASE_DIR)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

datafile  = "%s/data/unique_retirement_ages_%s.json" % (BASE_DIR, today.year)
# if not os.path.isfile(datafile):
#     datafile  = "%s/data/unique_retirement_ages_2015.json" % BASE_DIR

# this datafile specifies years that have unique retirement age values
# since this may change, it is maintained in an external file

with open(datafile, 'r') as f:
    age_map = json.loads(f.read())
    for year in age_map:
        age_map[year] = tuple(age_map[year])

def yob_test(yob=None):
    """
    tests to make sure suppied birth year is valid;
    returns valid birth year as a string or None
    """
    if not yob:
        return None
    try:
        birth_year = int(yob)
    except:
        print "birth year should be a number"
        return None
    else:
        b_string = str(birth_year)
        if birth_year > today.year:
            print "can't work with birth dates in the future"
            return None
        elif len(b_string) != 4:
            print "please supply a 4-digit birth year"
            return None
        else:
            return b_string

def get_retirement_age(birth_year):
    """ 
    given a worker's birth year, 
    returns full retirement age in years and months;
    returns None if the supplied year isn't valid
    """
    b_string = yob_test(birth_year)
    if b_string:
        yob = int(birth_year)
        if b_string in age_map.keys():
            return age_map[b_string]        
        elif yob <= 1937:
            return (65, 0)
        elif yob >= 1943 and yob <= 1954:
            return (66, 0)
        elif yob >= 1960:
            return (67, 0)
    else:
        return None

def get_delay_bonus(birth_year):
    """
    given a worker's year of birth,
    returns the annual bonus for delaying retirement 
    past full retirement age
    """
    b_string = yob_test(birth_year)
    if b_string:
        yob = int(birth_year)
        if yob in [1933, 1934]:
            return 5.5
        elif yob in [1935, 1936]:
            return 6.0
        elif yob in [1937, 1938]:
            return 6.5
        elif yob in [1939, 1940]:
            return 7.0
        elif yob in [1941, 1942]:
            return 7.5
        elif yob >= 1943:
            return 8.0
        else:
            return None
