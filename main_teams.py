import json

from request_logic import get_db_edits
from teams import teams_data_from_edits, find_userdata_from_edit, which_team

if __name__ == '__main__':
    user_teams = {}
    edits = get_db_edits()
    teams_data = teams_data_from_edits(edits)

    for edit in edits:
        user_data = find_userdata_from_edit(edit, teams_data)
        user = edit.user
        if user not in user_teams:
            team = which_team(user_data, teams_data)
            user_teams[user] = team

    print(json.dumps(user_teams))
