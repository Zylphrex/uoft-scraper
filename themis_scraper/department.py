import time
import session
import course


from constants import ARTS_DEPT
from constants import APSC_DEPT
from constants import SCAR_DEPT
from constants import UTM_DEPT


# each department is found in a element with id in the form of
# u###_line# where the first 3 numbers are found below, and the second
# number corresponds to its position on the page
_id_mapping = {
    ARTS_DEPT: 274,
    APSC_DEPT: 498,
    SCAR_DEPT: 644,
    UTM_DEPT: 790
}

_count_mapping = {
    ARTS_DEPT: 74,
    APSC_DEPT: 11,
    SCAR_DEPT: 18,
    UTM_DEPT: 22
}

# time to wait for webpage to load
SLEEP = 0.1

# maximum number of attempts it will try to load a page
MAX_ATTEMPTS = 100


def refine_division_base_xpath(base, division):
    """
    refine the base xpath for this division to focus on extracting the
    deparments from the html
    """
    return base + '//*[@id="' + division + 'List"]'

def gen_department_xpath(base, division, i):
    """
    generates a xpath to extract the department using the base xpath
    """

    return base + '//*[@id="u' + str(_id_mapping[division]) + '_line' + str(i) + '"]'

def create_department(base, division, i):
    """
    extracts the i-th department from the specified division, this function
    will try to extract the courses MAX_ATTEMPTS times at intervals of SLEEP
    seconds, and if it still fails after that, it will give up and return a
    department with no courses

    SLEEP and MAX_ATTEMPTS will be set at a value that will generally be considered safe
    """

    xpath = gen_department_xpath(base, division, i)
    node = session.at_xpath(xpath)
    name = node.text()
    node.click()

    # TODO: change to empty list later
    courses = []
    attempts = 0

    # if it didn't load correctly, try until it is
    while (not courses and attempts < MAX_ATTEMPTS):
        time.sleep(SLEEP)
        try:
            courses = course.create_courses()
        except IndexError:
            pass
        attempts += 1

    # return session to home page
    session.home()

    return Department(name, courses)

def create_departments(base, division):
    """
    generates a list of all departments in the division
    """
    base = refine_division_base_xpath(base, division)

    departments = []

    for i in range(_count_mapping[division]):
    # for i in range(0, 1): # TODO revert to above
        departments.append(create_department(base, division, i))

    return departments


class Department:

    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def to_dict(self):
        return {
            "name": self._name,
            "courses": [course.to_dict() for course in self._courses]
        }
