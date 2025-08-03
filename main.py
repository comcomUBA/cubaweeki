from pprint import pprint
from request_logic import get_recent_edits, do_fetch_run, get_db_edits
from teams import find_userdata_from_edit, which_team, assign_team, get_team_scores, add_score
from ranking import show_ranking_grupal, show_ranking_individual

from time import sleep

data = {
    "Rosetree": {},
    "TopoSort": {},
    "FloodMax": {},
}

if __name__ == '__main__':
    edits = get_db_edits()

    for edit in edits:
        user_data = find_userdata_from_edit(edit, data)

        if which_team(user_data, data):
            #ya tenia contribuciones
            updated_score = add_score(edit, data)
            data[which_team(user_data, data)][user_data] = updated_score
        else:
            #primera vez
            assign_team(user_data, data)

    pprint(data)
    print(get_team_scores(data))
