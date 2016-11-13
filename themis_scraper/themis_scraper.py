import json
import session
import division


if __name__ == '__main__':
    session.set_up()

    url='http://coursefinder.utoronto.ca/'

    session.start_session(url)

    divisions = division.create_divisions()

    data =  {"divisions": [division.to_dict() for division in divisions]}

    file = open('data.js', 'w')
    file.write(json.dumps(data, indent=4))
    file.close()
