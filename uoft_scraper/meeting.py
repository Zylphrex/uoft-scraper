class Meeting:

    def __init__(self, day, time, location):
        self._day = day
        self._time = time
        self._location = location

    def to_dict(self):
        return {
            "day": self._day,
            "time": self._time,
            "location": self._location
        }
