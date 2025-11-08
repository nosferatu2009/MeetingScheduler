from Meeting import Meeting
from collections import defaultdict
from datetime import date, timedelta
from Calendar import Calendar


class MeetingScheduler:

    def __init__(self):
        self.calendar = Calendar()

    def schedule_meeting(self, meeting):
        self.calendar.add_meeting(meeting)

    def fetch_meetings(self, user, startdate = date.min, enddate = date.max, period: str = None) :
        """Fetch meetings for a user. If `period` is provided it overrides startdate/enddate.
        Supported period values: 'today', 'week', 'month'.
        """
        if period:
            today = date.today()
            if period == 'today':
                startdate = today
                enddate = today
            elif period == 'week':
                startdate = today
                enddate = today + timedelta(days=6)
            else : 
                # compute end of current month
                y = today.year
                m = today.month
                if m == 12:
                    next_month = date(y+1, 1, 1)
                else:
                    next_month = date(y, m+1, 1)
                startdate = today
                enddate = next_month - timedelta(days=1)
            # else:
            #     raise ValueError("Unknown period. Use 'today', 'week' or 'month'.")

        return self.calendar.get_meetings(user, startdate, enddate)