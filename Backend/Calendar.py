from Meeting import Meeting
from collections import defaultdict
from datetime import date, timedelta
from MeetingType import MeetingType
import calendar

all_meetings = defaultdict(lambda : [])

class Calendar:
    
    def __init__(self):
        self.meetings = defaultdict(lambda : [])

    def add_meeting(self, meeting):

        organiser = meeting.organiser

        # self.meetings[organiser].append(meeting)
        all_meetings[organiser].append(meeting)

        for participant in meeting.participants :
            # self.meetings[participant].append(meeting)
            all_meetings[participant].append(meeting)


    def get_meetings(self, user, startdate = date.min, enddate = date.max) :

        user_meetings = all_meetings[user]
        # user_meetings = self.meetings[user]

        occurrences = []
        seen = set()  # to deduplicate (meeting_id, occurrence_date)

        def add_occurrence(orig_meeting, occ_date):
            key = (orig_meeting.meeting_id, occ_date)
            if key in seen:
                return
            seen.add(key)
            # create a single-instance Meeting representing this occurrence
            occ = Meeting(orig_meeting.meeting_id,
                          orig_meeting.organiser,
                          orig_meeting.participants,
                          occ_date,
                          occ_date,
                          orig_meeting.starttime,
                          orig_meeting.endtime,
                          MeetingType.SINGLE_INSTANCE)
            occurrences.append(occ)

        for meeting in user_meetings :
            # Ignore meetings that end before the requested range or start after it
            overall_start = meeting.startdate
            overall_end = meeting.enddate
            if overall_end < startdate or overall_start > enddate:
                continue

            if meeting.meeting_type == MeetingType.SINGLE_INSTANCE:
                if meeting.startdate >= startdate and meeting.startdate <= enddate:
                    add_occurrence(meeting, meeting.startdate)

            elif meeting.meeting_type == MeetingType.DAILY:
                s = max(overall_start, startdate)
                e = min(overall_end, enddate)
                cur = s
                while cur <= e:
                    add_occurrence(meeting, cur)
                    cur += timedelta(days=1)

            elif meeting.meeting_type == MeetingType.WEEKLY:
                # find first occurrence on or after startdate
                first = overall_start
                if first < startdate:
                    days_diff = (startdate - overall_start).days
                    weeks_offset = days_diff // 7
                    first = overall_start + timedelta(weeks=weeks_offset)
                    if first < startdate:
                        first += timedelta(weeks=1)
                cur = first
                last = min(overall_end, enddate)
                while cur <= last:
                    add_occurrence(meeting, cur)
                    cur += timedelta(weeks=1)

            elif meeting.meeting_type == MeetingType.MONTHLY:
                # helper to add months
                def add_month(d):
                    y = d.year + (d.month // 12)
                    m = d.month % 12 + 1
                    day = d.day
                    last_day = calendar.monthrange(y, m)[1]
                    day = min(day, last_day)
                    return date(y, m, day)

                # start from the meeting's startdate or the first month >= startdate
                cur = overall_start
                while cur < startdate:
                    cur = add_month(cur)
                    # guard against infinite loop
                    if cur.year > enddate.year + 10:
                        break
                last = min(overall_end, enddate)
                while cur <= last:
                    add_occurrence(meeting, cur)
                    cur = add_month(cur)

            else:
                # unknown type: treat as single instance if any overlap
                s = max(overall_start, startdate)
                if s <= min(overall_end, enddate):
                    add_occurrence(meeting, s)

        # print occurrences
        for meet in occurrences : 
            print(f"User {user} Calendar - {meet}")

        return occurrences