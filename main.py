from pprint import pprint
from request_logic import get_recent_edits
from teams import find_userdata_from_edit, which_team, assign_team, get_team_scores, add_score

data = {
    "Rosetree":{},
    "TopoSort": {},
    "FloodMax": {},
}

if __name__ == '__main__':
    while True:
        edits = list(get_recent_edits(None))

        for edit in edits[0] if edits and edits[0] else []:
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
