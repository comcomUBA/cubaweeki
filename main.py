import json
import datetime

from pprint import pprint

from teams import teams_data_from_edits
from request_logic import get_db_edits
from ranking import get_team_scores, flatten_users

if __name__ == '__main__':
    edits = []

    for edit in get_db_edits():
        ts = int(datetime.datetime.fromisoformat(edit.timestamp).timestamp())
        edits.append({
            "userid": edit.userid,
            "username": edit.user,
            "timestamp": ts
        })

    print(json.dumps(edits))
