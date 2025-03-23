
from main import *

users_playing = []
data = {
    "Rosetree":{},
    "TopoSort": {},
    "FloodMax": {},
}

def assign_team(user):
    """
    Determines the team with the least members and assigns the user to that team.
    """
    # Find the team with the least members
    least_populated_team = min(data, key=lambda team: len(data[team]))
    data[least_populated_team][user] = 1
    return least_populated_team

def which_team(user):
    """
    Determines which team a user belongs to.
    """
    for key in data:
        if user in data[key].keys():
            return key
    return False
    
def find_userdata_from_edit(edit):
    """
    Finds the user data tuple (user, userid, score) from the team data.
    If the user is not found, initializes a new tuple with a score of 0.
    """
    user = edit['user']
    userid = edit['userid']
    
    # Search for the user in the team data
    for team, members in data.items():
        for member in members:
            if member[0] == user and member[1] == userid:
                return member

    # If user is not found, return a new tuple with score 0
    return (user, userid)

def add_score(edit):
    """
    Finds the user's current score from the team data and increments it by 1.
    """
    user = edit['user']
    userid = edit['userid']

    # Search for the user in the team data
    for team, members in data.items():
        for member, score in members.items():
            if member[0] == user and member[1] == userid:
                # Increment the user's score by 1
                return score + 1

    # If user is not found, return an initial score of 1
    return 1

def get_team_scores():
    """
    Calculates the total score for each team by summing up the scores of all players in the team.
    Returns a dictionary with team names as keys and their total scores as values.
    """
    team_scores = {}
    for team, members in data.items():
        # Sum up the scores of all members in the team
        total_score = sum(members.values())
        team_scores[team] = total_score
    return team_scores

def main():
    while True:
        edits = list(get_recent_edits(None))

        for edit in edits[0] if edits and edits[0] else []:
            user_data = find_userdata_from_edit(edit)

            if which_team(user_data):
                #ya tenia contribuciones
                updated_score = add_score(edit)
                data[which_team(user_data)][user_data] = updated_score
            else:
                #primera vez
                assign_team(user_data)
        pprint(data)
        print(get_team_scores())
        
        sleep(10)

main()