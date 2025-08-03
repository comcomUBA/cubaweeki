import json

from pprint import pprint
from teams import teams_data_from_edits
from request_logic import get_db_edits
from ranking import get_team_scores, flatten_users

if __name__ == '__main__':
    edits = get_db_edits()
    teams = teams_data_from_edits(edits)
    teams = flatten_users(teams)

    # pprint(teams)
    # print(get_team_scores(teams))
    print(json.dumps(teams))
