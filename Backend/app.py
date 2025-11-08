from MeetingScheduler import MeetingScheduler
from Meeting import Meeting
from datetime import date, datetime, time
from MeetingType import MeetingType
from flask import Flask, request, jsonify
import random
from Calendar import all_meetings

server = Flask(__name__)

# to get meetings 
@server.route("/meetings/<string:range>", methods=['GET'])
def fetch_meeting(range):

    try : 
        # we get user name from header
        print(request.headers)
        user = request.headers.get("username")
        print("user", user)
        meetingScheduler = MeetingScheduler()
        meetings = meetingScheduler.fetch_meetings(user, period=range)
        print(meetings)
        meetings_json = [m.to_dict() for m in meetings]
        return jsonify( status =  "success" , meetings = meetings_json), 200
    
    except Exception as e :
        return {"error" : str(e)}, 500

@server.route("/meetings/", methods=['POST'])
def schedule_meeting():

    try : 
        # we get user name from header
        user = request.headers.get("username")

        data = request.get_json()
        participants = data.get("participants")
        start_date = data.get("start_date")
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = data.get("end_date")
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        start_time = data.get("start_time")
        start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        end_time = data.get("end_time")
        end_time = datetime.strptime(end_time, "%H:%M:%S").time()
        meeting_type = data.get("meeting_type")

        meeting_id = int(random.random())

        meeting = Meeting(meeting_id, user,participants, start_date, end_date, start_time, end_time, meeting_type )

        meetingScheduler = MeetingScheduler()
        meetingScheduler.schedule_meeting(meeting = meeting)
        meetings = meetingScheduler.fetch_meetings(user, period=range)
        print(meetings)
        meetings_json = [m.to_dict() for m in meetings]
        return jsonify( status =  "success" , meetings = meetings_json), 200
    
    except Exception as e :
        return {"error" : str(e)}, 500



def main():

    meeting1 = Meeting(1,"Alice", ["A", "B", "C"], date(2025,11,21), date(2025,11,21), time(14,30,0), time(15,0,0), MeetingType.SINGLE_INSTANCE)
    meeting2 = Meeting(2,"Bob", ["A", "B", "C"],   date(2025,11,21), date(2025,11,30), time(15,30,0), time(15,45,0), MeetingType.DAILY)
    meeting3 = Meeting(3,"Alice", ["A", "B", "C"], date(2025,11,11), date(2025,11,21),time(13,30,0), time(15,0,0), MeetingType.WEEKLY)
    meeting4 = Meeting(4,"Alice", ["A", "B", "C"], date(2025,11,10), date(2025,11,10),time(13,30,0), time(14,0,0), MeetingType.DAILY)


    meetingScheduler = MeetingScheduler()
    meetingScheduler.schedule_meeting(meeting = meeting1)
    meetingScheduler.schedule_meeting(meeting = meeting2)
    meetingScheduler.schedule_meeting(meeting = meeting3)
    meetingScheduler.schedule_meeting(meeting = meeting4)

#     meetings = meetingScheduler.fetch_meetings("Alice", period="week")


if __name__ == "__main__":
    main()
    print("all_meetings", all_meetings )
    server.run(debug=True, use_reloader=False)