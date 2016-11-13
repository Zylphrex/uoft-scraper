import meeting


class Section:

    @staticmethod
    def exists(browser, count):
        return bool(browser.find_elements_by_xpath('//*[@id="u245_line' + str(count) + '"]'))

    @staticmethod
    def create(browser, count):
        if not Section.exists(browser, count):
            return None

        return Section(browser, count)

    def __init__(self, browser, count):
        self._activity = browser.find_element_by_xpath('//*[@id="u245_line' + str(count) + '"]').text
        self._instructor = browser.find_element_by_xpath('//*[@id="u263_line' + str(count) + '"]').text
        self._class_size = browser.find_element_by_xpath('//*[@id="u281_line' + str(count) + '"]').text
        self._current_enrolment = browser.find_element_by_xpath('//*[@id="u290_line' + str(count) + '"]').text

        times = browser.find_element_by_xpath('//*[@id="u254_line' + str(count) + '"]').text
        locations = browser.find_element_by_xpath('//*[@id="u272_line' + str(count) + '"]').text
        if times != '':
            times = times.split('\n')
            days = [time.split(' ')[0] for time in times]
            times = [time.split(' ')[1] for time in times]
        else:
            days = []
            times = []
        if locations != '':
            locations = locations.split('\n')
        else:
            locations = []
        self._meetings = [meeting.Meeting(day, time, location) for day, time, location in zip(days, times, locations)]

    def to_dict(self):
        return {
            "activity": self._activity,
            "instructor": self._instructor,
            "class size": self._class_size,
            "current_enrolment": self._current_enrolment,
            "meetings": [meeting.to_dict() for meeting in self._meetings]
        }
