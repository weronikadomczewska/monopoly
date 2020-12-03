
from field import Field
from random import randint, random

''' klasa reprezentująca rozgrywkę '''
class Game:
    ''' 
    konstruktor gry

    '''
    def __init__(self):
        self.initializeFields()
        self.initializeCards()
        self.players = []
    
    '''
    funkcja inicjalizująca planszę, tworzy wszystkie pola i dodaje je do listy self.fields
    '''
    def initializeFields(self):
        self.fields = []
        # TODO(Bartosz P.): dodać prawdziwe pola
        for i in range(36):
            # color = (255, 56, 152)
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            # isSpecial = False if random() > 0.25 else True
            if i == 0:
                self.fields.append(Field(color=color, isSpecial=True, imagePath="res/start.png"))
            elif i == 9:
                self.fields.append(Field(color=color, isSpecial=True, imagePath="res/jail.png"))
            elif i == 18:
                self.fields.append(Field(color=color, isSpecial=True, imagePath="res/tram.png"))
            elif i == 27:
                self.fields.append(Field(color=color, isSpecial=True, imagePath="res/gotojail.png"))
            else:
                self.fields.append(Field(color=color))



    '''
    funkcja inicjalizująca karty, dodaje je do list self.positiveCards i self.negativeCards
    '''
    def initializeCards(self):
        self.positiveCards = [
            ("+10", lambda _ : print("karta +10")),  # tymczasowe karty do testowania
            ("+100", lambda _ : print("karta +100")) # TODO(Bartosz P.): zamienić je na prawdziwe
        ]

        self.negativeCards = [
            ("-10", lambda _ : print("karta -10")),  # tymczasowe karty do testowania
            ("-100", lambda _ : print("karta -100")) # TODO(Bartosz P.): zamienić je na prawdziwe
        ]

    '''
    funkcja dodająca gracza do gry

    Argumenty:
        player (Player): gracz, którego dodajemy
    '''
    def addPlayer(self, player):

        if len(self.players) < 4:
            self.players.append(player)
        else:
            raise Exception("Game:addPlayer: coś jest nie tak, próbowano dodać za dużo graczy!")
    
    # funkcja do testowania interfejsu
    def takeAction(self):
        for p in self.players:
            p.position += randint(1, 12)
            if p.position > 35:
                p.position %= 36

            if self.fields[p.position].owner == None and not self.fields[p.position].isSpecial:
                if random() < 0.05:
                    self.fields[p.position].owner = p
                    p.ownedFields.append(self.fields[p.position])