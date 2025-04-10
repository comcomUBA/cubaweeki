from matplotlib import animation, pyplot as plt
from teams import get_team_scores


data = {"Rosetree": {"Fron": 8, "Facu": 12,},
        "TopoSort": {"Sasha": 15, "Dani": 12, "Daeron": 5,},
        "FloodMax": {"Pau": 16, "Lau": 9,},
        }

def show_ranking_grupal(data):
        scores = get_team_scores(data) #Se puede ahorrar si simplemente se llama a la funcion despues de usar get_team_scores en main
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
                if base[0] != scores["Rosetree"]:
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

#show_ranking_grupal(data)
show_ranking_individual(data)

