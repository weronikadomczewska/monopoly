import matplotlib.pyplot as plt
import random
import subprocess
import numpy as np

#TODO: dopisz do readme konieczność zainstalowania numpy
#TODO: ustaw kolory słupków tak, aby zgadzały się z kolorami pionków graczy

#statystyki każdego gracza od 0 do 3 w kolejności posiadane pieniądze, posiadłości, pobyty w więzieniu
#jeżeli jest mniej niż 4 graczy - wszystko jest ustawione na None; w przypadku bankruta wszystkie statystyki sa zerowane

#wykres jest grupowany po turach

#dane testowe dla sześciu tur
stats = {}

for i in range(4):
    money = []
    possessions = []
    prison = 0
    money.append(random.choice([None, 0, 10, 20, 30, 40, 50]))
    if money[0] == None:
        money = [None, None, None, None, None, None]
        possessions = [None, None, None, None, None, None]
        prison = None
    elif money[0] == 0:
        money = [0,0,0,0,0,0]
        possessions = [0,0,0,0,0,0]
        prison = random.choice([0, 10, 20, 30])
    else:
        for k in range(5):
            money.append(random.choice([10,20,30,40,50]))
        for j in range(6):
            possessions.append(random.choice([5, 10, 15, 20, 25]))
        prison = random.choice([0, 10, 20])

    stats[i] = (money, possessions, prison)


#usuwam dane niestniejących graczy (None)
good_stats = {}
cnt = 0
for i in range(4):
    if stats[i][2] == None:
        continue
    else:
        good_stats[cnt] = stats[i]
        cnt += 1

# print(stats)
# print()
# print(good_stats)

#rozdzielam dane
players_money = []
players_possessions = []
players_prison = []

for i in range(len(good_stats)-1):
    players_money.append(good_stats[i][0])
    players_possessions.append(good_stats[i][1])
    players_prison.append(good_stats[i][2])

# print(players_money)
print(players_possessions)
# print(players_prison)

#wykres
#ilość tur przyjęta do testów; dzielę wykres po turach
groups=6
#rozmieszczenie grup kolumn na wykresie
# x = [i for i in range(groups)]
x=np.arange(groups)
bar_width = 0.15

# plt.axis("off")
plt.xticks([])
plt.yticks([])

for i in range(len(good_stats)-1):
    print(players_money[i])
    plt.bar(x,players_money[i], bar_width, color="green")
    
plt.xticks(x,[y+1 for y in range(groups)])

for i in range(len(good_stats)-1):
    print(players_possessions[i])
    plt.bar(x+bar_width,players_possessions[i], width=bar_width, color="pink")

plt.title("Koniec gry!", fontsize=15)
plt.xlabel("Numer tury")
plt.legend(["Zebrane ECTS-y", "Zaliczone przedmioty"])
plt.box(False)




# subprocess.run(["touch", "plot.png"])
# plt.savefig(fname="plot.png")
# plt.gca().axes.get_yaxis().set_visible(False)
plt.show()
