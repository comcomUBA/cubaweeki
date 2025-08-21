def initial_teams_data():
    return {
        "RoseTree": {},
        "TopoSort": {},
        "FloodMax": {},
    }

def assign_team(user, teams):
    """
    Determines the team with the least members and assigns the user to that team.
    """
    # Find the team with the least members
    least_populated_team = min(teams, key=lambda team: len(teams[team]))
    teams[least_populated_team][user] = 1
    return least_populated_team

def which_team(user, teams):
    """
    Determines which team a user belongs to.
    """
    for key in teams:
        if user in teams[key].keys():
            return key
    return False
    
def find_userdata_from_edit(edit, teams):
    """
    Finds the user data tuple (user, userid, score) from the teams data.
    If the user is not found, initializes a new tuple with a score of 0.
    """

    user = edit.user
    userid = edit.userid

    # Search for the user in the team data
    for team, members in teams.items():
        for member in members:
            if member[0] == user and member[1] == userid:
                return member

    # If user is not found, return a new tuple with score 0
    return (user, userid)

def add_score(edit, teams):
    """
    Finds the user's current score from the teams data and increments it by 1.
    """
    user = edit.user
    userid = edit.userid

    # Search for the user in the teams data
    for team, members in teams.items():
        for member, score in members.items():
            if member[0] == user and member[1] == userid:
                # Increment the user's score by 1
                return score + 1

    # If user is not found, return an initial score of 1
    return 1

def get_team_scores(teams):
    """
    Calculates the total score for each team by summing up the scores of all players in the team.
    Returns a dictionary with team names as keys and their total scores as values.
    """
    team_scores = {}
    for team, members in teams.items():
        # Sum up the scores of all members in the team
        total_score = sum(members.values())
        team_scores[team] = total_score
    return team_scores

def teams_data_from_edits(edits):
    teams = initial_teams_data()

    for edit in edits:
        user_data = find_userdata_from_edit(edit, teams)
        team = which_team(user_data, teams)

        if not team:
            assign_team(user_data, teams)
        else:
            updated_score = add_score(edit, teams)
            teams[team][user_data] = updated_score

    return teams
