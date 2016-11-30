import requests


from bs4 import BeautifulSoup


from section import Section
from extract import extract


class Course:

    def __init__(self, url):
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        self.set_course_data(soup)
        self.set_sections_data(soup)

    def set_course_data(self, soup):
        header = soup.find(id='u19').text.strip().split(' ')
        self._code = header[0][:-1]
        self._name = ' '.join(header[1:])

        self._division = extract(soup, 'u23')
        self._description = extract(soup, 'u32')
        self._department = extract(soup, 'u41')
        self._prerequisite = extract(soup, 'u50')
        self._corequisite = extract(soup, 'u59')
        self._exclusion = extract(soup, 'u68')
        self._preparation = extract(soup, 'u77')
        self._level = extract(soup, 'u86')
        self._term = extract(soup, 'u158')

    def set_sections_data(self, soup):
        self._sections = []
        count = 0
        while True:
            sect = Section.create(soup, count)
            if sect is not None:
                self._sections.append(sect)
                count += 1
            else:
                break

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
            "term": self._term,
            "sections": [section.to_dict() for section in self._sections]
        }
