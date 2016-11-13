import json
import requests
import time

from bs4 import BeautifulSoup


from course import Course


ARTS_DEPT = 'Faculty of Arts and Science'
APSC_DEPT = 'Faculty of Applied Science and Engineering'
SCAR_DEPT = 'University of Toronto Scarborough'
UTM_DEPT = 'University of Toronto Mississauga'

_depts = [ARTS_DEPT, APSC_DEPT, SCAR_DEPT, UTM_DEPT]

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


def validate(uid):
    parts = uid.split('_')
    if len(parts) != 2:
        return False

    part1 = parts[0][1:]
    part2 = parts[1][4:]

    if not part1.isdigit() or not part2.isdigit():
        return False

    part1 = int(part1)
    part2 = int(part2)

    for id_key in _id_mapping:
        if part1 == _id_mapping[id_key]:
            for count_key in _count_mapping:
                if part2 < _count_mapping[count_key]:
                    return True

    return False

def extract_links(soup):
    inputs = soup.find_all('input')
    links = []

    for elem in inputs:
        if 'data-for' in elem.attrs and validate(elem['data-for']):
            data = elem['value']
            data = data.split('searchForCourseByDept(')[1].split(');')[0]
            index = 0
            while True:
                index = data.find("'", index)
                if index == -1:
                    break
                if index == 0 or index == len(data) - 1:
                    data = data[:index] + '"' + data[index + 1:]
                elif data[index - 1] == ' ' or data[index + 1] == ',' or data[index - 1] == ',':
                    data = data[:index] + '"' + data[index + 1:]
                index += 1

            data = json.loads('[' + data + ']')
            links.append((data[2].strip(), data[4].strip()))

    return links

def formulate_department_url(link):
    return 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/course/browseSearch?deptId=' + link[0] + '%20&divId=' + link[1]

def formulate_course_url(link):
    return 'http://coursefinder.utoronto.ca/course-search/search/courseSearch/coursedetails/' + link

def gen_course_links(soup):
    links = extract_links(soup)
    course_links = []

    for l in links: # TODO
        dept_link = formulate_department_url(l)
        response = session.get(dept_link, cookies=homepage.cookies)
        data = json.loads(response.text.strip())['aaData']
        for course in data:
            course_link = formulate_course_url(course[1].split('/')[-2].split("'")[0])
            course_links.append(course_link)

    return course_links




if __name__ == '__main__':
    site_url = 'http://coursefinder.utoronto.ca/'
    session = requests.Session()
    homepage = session.get(site_url)

    soup = BeautifulSoup(homepage.text, 'lxml')

    course_links = gen_course_links(soup)

    courses = []

    for course_link in course_links[:10]:
        time.sleep(.5)
        print(course_link)
        course = Course(course_link)
        courses.append(course.to_dict())

    file = open('data.js', 'w')
    file.write(json.dumps(courses, indent=4))
    file.close()
