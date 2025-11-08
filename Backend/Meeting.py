
from datetime import date, time


class Meeting():

    def __init__(self, meeting_id, organiser, participants, startdate, enddate, startime, endtime, meeting_type):
        self.meeting_id = meeting_id
        self.organiser = organiser
        self.participants = participants
        self.starttime = startime
        self.endtime = endtime
        self.startdate = startdate
        self.enddate = enddate
        self.meeting_type = meeting_type

    def __repr__(self):
        return f'Meeting - {self.meeting_id} Organised By - {self.organiser}, Date - {self.startdate} - {self.enddate}, Time - {self.starttime} - {self.endtime}, Type - {self.meeting_type}'
    
    def to_dict(self):
        return {
            "id": self.meeting_id,
            "organizer": self.organiser,
            "participants": self.participants,
            "start_date": self.startdate.isoformat() if isinstance(self.startdate, date) else self.startdate,
            "end_date": self.enddate.isoformat() if isinstance(self.enddate, date) else self.enddate,
            "start_time": self.starttime.strftime("%H:%M:%S") if isinstance(self.starttime, time) else self.starttime,
            "end_time": self.endtime.strftime("%H:%M:%S") if isinstance(self.endtime, time) else self.endtime,
            "meeting_type": str(self.meeting_type)
        }