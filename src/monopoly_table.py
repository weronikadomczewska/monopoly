import matplotlib.pyplot as plt
import random
import subprocess
import os

#TODO: dopisz do readme konieczność zainstalowania numpy
#TODO: ustaw kolory wierszy tak, aby zgadzały się z kolorami pionków graczy

#statystyki każdego gracza od 0 do 3 w kolejności posiadane pieniądze, posiadłości, pobyty w więzieniu
#w przypadku bankruta wszystkie statystyki sa zerowane

#dane
def statistics(data):
    
    #rangi
    #szukam najwięcej ECTS
    max_ects = max(data,key=lambda x:x[0])
    if len(max_ects) == 3:
        max_ects.append("geniusz!")
    else:
        max_ects[3] += "\n geniusz!"

    #szukam najwięcej przedmiotów
    max_p = max(data,key=lambda x:x[1])
    if len(max_p) == 3:
        max_p.append("pracoholik")
    else:
        max_p[3] += "\n pracoholik"

    #szukam najwięcej napraw
    max_np= max(data,key=lambda x:x[2])
    if len(max_np) == 3:
        max_np.append("(nie)złota rączka!")
    else:
        max_np[3] += "\n (nie)złota rączka!"

    for p in data:
        if len(p) < 4:
            p.append("")

    #zamieniam zera na "bankrut!"
    for i in range(len(data)):
        cnt=0
        for j in range(len(data[i])):
            if data[i][j] == '0':
                cnt += 1
        if cnt == 3:
            data[i] = ['bankrut', 'bankrut', 'bankrut', 'bankrut']


    #wykres
    fig, ax = plt.subplots(figsize=(12, 5)) 
    ax.set_axis_off()

    columns = ("ECTS'y", "wartość zaliczonych przedmiotów", "naprawy komputera", "ranga")
    rows = ["Gracz " + str(i+1) for i in range(len(data))]
    # print(rows)

    #kolory graczy
    player_colors = ["yellow", "green", "lightblue", "red"]

    table = ax.table( 
        cellText=data, 
        rowLabels=rows,  
        colLabels=columns, 
        rowColours=player_colors,  
        colColours=["lightblue"]* len(columns), 
        cellLoc='center',
        colWidths=[0.25, 0.25, 0.25, 0.25], 
        loc='upper left',
        
    )
        
    ax.set_title('Koniec gry!', fontsize=30)
    table.scale(1, 4)
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    plt.tight_layout()

    # zapis do pliku - odkomentuj!
    plt.savefig(fname="res/table.png")
    # plt.show()


#test
# data = [

#     ['255', '18', '10'],
#     ['10', '0', '15'],
#     ['0', '0', '0'],
#     ['100', '15', '23']

# ]

# statistics(data)

