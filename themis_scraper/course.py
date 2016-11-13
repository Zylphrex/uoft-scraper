from selenium import webdriver
import session


def check_total():
    """
    returns the total number of courses
    """

    count_xpath = '//*[@id="courseSearchResults_info"]'
    result = session.at_xpath(count_xpath).text().split(' ')
    if result[-1] == 'results':
        return int(result[-2])
    elif result[-1] == 'found':
        return 0
    else:
        return None

def gen_course_xpath(i):
    """
    generates the xpath to the i-th course
    """

    return '//*[@id="courseSearchResults"]/tbody/tr[' + str(i) + ']/td[2]/a'

def extract_bounds():
    """
    extracts the lower and upper bounds on the course counts on this page
    """

    count_xpath = '//*[@id="courseSearchResults_info"]'
    result = session.at_xpath(count_xpath).text().split(' ')[-4].split('-')
    return int(result[0]), int(result[1])

def format(text):
    return text.split('\n')[-1]

def find_optional_element(browser, xpath):
    elements = browser.find_elements_by_xpath(xpath)
    if elements:
        return format(elements[0].text)
    else:
        return 'None'

def course_from_page(browser):
    title_xpath = '//*[@id="u19"]/h2/span'
    title = browser.find_element_by_xpath(title_xpath).text.split(' ')
    code = title[0][:-1]
    name = ' '.join(title[1:])

    division = format(browser.find_element_by_xpath('//*[@id="u23"]').text)
    description = format(browser.find_element_by_xpath('//*[@id="u32"]').text)
    department = format(browser.find_element_by_xpath('//*[@id="u41"]').text)

    prerequisite = find_optional_element(browser, '//*[@id="u50"]')
    corequisite = find_optional_element(browser, '//*[@id="u59"]')
    exclusion = find_optional_element(browser, '//*[@id="u68"]')
    preparation = find_optional_element(browser, '//*[@id="u77"]')

    level = format(browser.find_element_by_xpath('//*[@id="u86"]').text)
    term = format(browser.find_element_by_xpath('//*[@id="u158"]').text)

    return Course(code, name, division, description, department, prerequisite, corequisite, exclusion, preparation, level, term)

def create_course(url_end):
    """
    creates a single course object found at the url specified by url_end
    """
    url = 'http://coursefinder.utoronto.ca/course-search/search/' + url_end
    browser = webdriver.PhantomJS("./phantomjs")
    browser.get(url)
    course = course_from_page(browser)
    browser.quit()
    return course

def create_courses():
    """
    generates a list of all courses on this page
    """

    count = 0
    total = check_total()
    if total is None:
        return None

    courses = []

    cur = 0
    low, high = extract_bounds()

    while count < total:
        # there is still another course, maybe its on the next page
        course_xpath = gen_course_xpath(cur + 1)
        url = session.at_xpath(course_xpath).get_attr('href')
        courses.append(create_course(url))

        cur += 1
        count += 1

        if cur + low == high + 1:
            if high < total: # need to move to next page
                xpath = '//*[@id="courseSearchResults_next"]'
                node = session.at_xpath(xpath)
                while True: # spam next button until it works
                    try:
                        node.click()
                        break
                    except:
                        pass
            low, high = extract_bounds()
            cur = 0

    return courses


class Course:

    def __init__(self, code, name, division, description, department, prerequisite, corequisite, exclusion, preparation, level, term):
        self._code = code
        self._name = name
        self._division = division
        self._description = description
        self._department = department
        self._prerequisite = prerequisite
        self._corequisite = corequisite
        self._exclusion = exclusion
        self._preparation = preparation
        self._level = level
        self._term = term

        print('\n'.join([code, name, division, description, department, prerequisite, corequisite, exclusion, preparation, level, term]))
        print('=' * 80)


    def to_dict(self):
        return {
            "code": self._code,
            "name": self._name,
            "division": self._division,
            "description": self._description,
            "department": self._department,
            "prerequisite": self._prerequisite,
            "corequisite": self._corequisite,
            "exclusion": self._exclusion,
            "preparation": self._preparation,
            "level": self._level,
            "term": self._term
        }
