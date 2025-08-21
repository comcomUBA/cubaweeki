import json
from collections import Counter, defaultdict

def main():
    """Aggregate team scores and output in the specified format."""
    # Load team assignments and edits
    with open('race/teams.json', 'r') as f:
        user_teams = json.load(f)
    
    with open('race/edits.json', 'r') as f:
        edits = json.load(f)
    
    # Group edits by team with actual timestamps
    team_edits = defaultdict(list)
    team_id_map = {}
    team_id = 1
    
    for edit in edits:
        username = edit['username']
        if username in user_teams:
            team = user_teams[username]
            
            # Assign team ID if not already assigned
            if team not in team_id_map:
                team_id_map[team] = team_id
                team_id += 1
            
            team_edits[team].append(edit['timestamp'])
    
    # Create output in the requested format
    team_data = []
    for team, timestamps in team_edits.items():
        for timestamp in timestamps:
            team_data.append({
                "teamid": team_id_map[team],
                "teamname": team,
                "timestamp": timestamp
            })
    
    # Save output
    with open('race/team_scores_from_users.json', 'w') as f:
        json.dump(team_data, f, indent=2, ensure_ascii=False)
    
    print(f'Team scores saved to race/team_scores_from_users.json')

if __name__ == '__main__':
    main()
