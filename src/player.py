import random

''' klasa reprezentująca pojedynczego gracza w grze '''
class Player:

    ''' 
    konstruktor gracza

    Argumenty:
        isBot (bool): czy tworzony gracz jest botem?
        color (tuple(int, int, int)): kolor reprezentujący tworzonego gracza (RGB)
        money (int): początkowa gotówka tworzonego gracza

    '''
    def __init__(self, isBot=False, color=(0, 0, 0), money=300):
        self.isBot = isBot
        self.color = color
        self.money = money
        self.diceroll = 0
        self.position = 0
        self.ownedFields = []

# przykłady stworzenia nowego gracza
#
# p1 = Player(isBot=True, color=(255, 0, 0), money=600) - tworzy gracza komputerowego o kolorze czerwonym, który posiada 600 pieniędzy
# p2 = Player(money=100) - tworzy gracza (niekomputerowego) o kolorze czarnym i gotówce 100
