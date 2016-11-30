from meeting import Meeting
from extract import extract


class Section:

    @staticmethod
    def exists(soup, count):
        return bool(soup.find_all(id='u245_line' + str(count)))

    @staticmethod
    def create(soup, count):
        if not Section.exists(soup, count):
            return None

        return Section(soup, count)

    def __init__(self, soup, count):
        self._activity = extract(soup, 'u245_line' + str(count))
        # soup.find('//*[@id="u245_line' + str(count) + '"]').text
        self._instructor = extract(soup, 'u263_line' + str(count))
        # soup.find('//*[@id="u263_line' + str(count) + '"]').text
        self._class_size = extract(soup, 'u281_line' + str(count))
        # soup.find('//*[@id="u281_line' + str(count) + '"]').text
        self._current_enrolment = extract(soup, 'u290_line' + str(count))
        # soup.find('//*[@id="u290_line' + str(count) + '"]').text
        self._option_to_waitlist = 'yes' if soup.find(id='u308_line' + str(count)) else 'no'
        self._delivery_mode = extract(soup, 'u314_line' + str(count))
        # soup.find('//*[@id="u314_line' + str(count) + '"]').text

        times = extract(soup, 'u254_line' + str(count))
        # soup.find('//*[@id="u254_line' + str(count) + '"]').text
        locations = extract(soup, 'u272_line' + str(count))
        # soup.find('//*[@id="u272_line' + str(count) + '"]').text
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
        self._meetings = [Meeting(day, time, location) for day, time, location in zip(days, times, locations)]

    def to_dict(self):
        return {
            "activity": self._activity,
            "instructor": self._instructor,
            "class size": self._class_size,
            "current enrolment": self._current_enrolment,
            "meetings": [meeting.to_dict() for meeting in self._meetings],
            "option to waitlist": self._option_to_waitlist,
            "delivery mode": self._delivery_mode
        }
