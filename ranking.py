from teams import get_team_scores, teams_data_from_edits
from request_logic import get_db_edits

try:
        from matplotlib import animation, pyplot as plt
except:
        matplotlib = None

def show_ranking_grupal(data):
        if not matplotlib:
                raise ImportError("no matplotlib")

        #Se puede ahorrar si simplemente se llama a la funcion despues de usar get_team_scores en main
        scores = get_team_scores(data)
        base = [0,0,0]
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize = (12, 6))
        plt.title("Puntaje total de los equipos")

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel('Equipos', fontweight ='bold') 
        ax.set_ylabel('Contribuciones', fontweight ='bold')

        artists = []
        colors = ['cyan', 'magenta', 'springgreen']

        while base != list(scores.values()):
                if base[0] != scores["RoseTree"]:
                        base[0] = base[0] + 1
                if base[1] != scores["TopoSort"]:
                        base[1] = base[1] + 1
                if base[2] != scores["FloodMax"]:
                        base[2] = base[2] + 1

                container = ax.bar(list(scores.keys()), base, color=colors)        
                artists.append(container)

        ax.bar_label(artists[len(artists) - 1])
        ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=35, repeat=False)

        plt.show()


def show_ranking_individual(data):
        if not matplotlib:
                raise ImportError("no matplotlib")

        # Capaz conviene hacer un refactoring de esta parte e incluirla en teams.py como otra funcion
        contributors = list()
        for team, members, in data.items():
                for contributor in members.items():
                        contributors.append(contributor)
        contributors.sort(key=lambda tup: tup[1])
        ###############################################################################################

        nombres = [x[0] for x in contributors]
        puntajes = [x[1] for x in contributors]
        base = [0] * len(puntajes)
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize = (12, 6))
        plt.title("Ranking individual de contribuciones")

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.xaxis.set_visible(False)

        artists = []

        while base[len(base)-1] != puntajes[len(base)-1]:
                for i in range (len(puntajes)):
                        if base[i] < puntajes[i]:
                                base[i] =  base[i] + 1
                container = ax.barh(nombres, base, color='cyan')
                artists.append(container)

        ax.bar_label(artists[len(artists)-1])
        ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=35, repeat=False)

        plt.show()

def flatten_users(teams):
    # transform user tuple into user string
    nteams = {}
    for team, td in teams.items():
        ntd = dict()
        for usertuple, count in td.items():
            uname, uid = usertuple
            userstr = f"{uname}#{uid}"
            ntd[userstr] = count
        nteams[team] = ntd
    return nteams


if __name__ == "__main__":
    sample_teams_data = {
        "RoseTree": {"Fron": 8, "Facu": 12,},
        "TopoSort": {"Sasha": 15, "Dani": 12, "Daeron": 5,},
        "FloodMax": {"Pau": 16, "Lau": 9,},
    }

    edits = get_db_edits()
    teams = teams_data_from_edits(edits)

    # to avoid random numpy error downstream
    teams = flatten_users(teams)

    show_ranking_grupal(teams)
    show_ranking_individual(teams)
