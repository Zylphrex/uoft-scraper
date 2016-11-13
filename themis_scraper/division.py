import session
import department

from constants import ARTS_DEPT
from constants import APSC_DEPT
from constants import SCAR_DEPT
from constants import UTM_DEPT

########################################
# variables go here
# id of div for each division
_divisions = [ARTS_DEPT, APSC_DEPT, SCAR_DEPT, UTM_DEPT]
########################################


def gen_division_base_xpath(division):
    """
    generates the base xpath for each division, this xpath can then be used to
    create other xpaths that can extract other info about the division
    """
    return '//*[@id="' + division + '"]'

def gen_division_name_xpath(base):
    """
    generates a xpath to extract the name of the division using the base xpath
    """
    return base + '//h4//span'

def create_division(division):
    """
    creates a single division with the id as specified by division
    """

    base = gen_division_base_xpath(division)

    name = session.at_xpath(gen_division_name_xpath(base)).text()

    print("extracting division:", name)

    departments = department.create_departments(base, division)

    print("finished extracting division:", name)
    return Division(name, departments)

def create_divisions():
    """
    creates all the divisions, one for each id specified by _divisions above
    """

    divisions = []

    for division in _divisions:
    # for division in _divisions[:1]: # TODO revert to above
        divisions.append(create_division(division))

    return divisions

class Division:

    def __init__(self, name, departments):
        self._name = name
        self._departments = departments

    def to_dict(self):
        return {
            "name": self._name,
            "departments": [department.to_dict() for department in self._departments]
        }
