
from field import Field
from random import randint, random, choice
from monopoly_table import statistics

''' klasa reprezentująca rozgrywkę '''

class Game:
    
    WAITINGFORDICE = 1
    WAITINGFORDECISION = 2
    WAITINGFORCARD = 3
    WAITINGFORUPGRADE = 4
    WAITINGFORPURCHASE = 5
    WAITINGFORREPURCHASE = 6
    WAITINGFORJAIL = 7
    WAITINGFORTRAM = 8
    KONIECGRY = 9

    ''' 
    konstruktor gry

    '''
    def __init__(self):
        self.initializeFields()
        self.initializeCards()
        self.players = []
        self.state = self.WAITINGFORDICE
        self.activePlayer = 0
    
    '''
    funkcja inicjalizująca planszę, tworzy wszystkie pola i dodaje je do listy self.fields
    '''
    #obsługa pola startowego
    def startField(self, player):
        player.money += 30

    #akcja na polu duży grzyb
    def bigMushroom(self, player):
        player.money -= 30

    #TODO
    #akcja na polu szansa
    def chanceField(self, player):
        card = choice(self.cards)
        self.card_effect(player, card[-2], card[-1])
        return card[0]

    #akcja na polu więzienie
    def prisonField(self, player):
        player.jailed = 2
        player.total_jailed += 1
    
    #TODO
    #akcja na polu specjalnym praktyka w Nokii (pole, którego nie można odkupić)
    def practiseField(self, player):
        if self.fields[player.position].owner == None:
            player.money -= 45
            self.fields[player.position].owner=player
            player.ownedFields.append(self.fields[player.position])
        else:
            player.money -= 30
            self.fields[player.position].owner.money += 30

    #akcja na polu tramwaj
    def tramField(self, player):
        self.state = self.WAITINGFORTRAM
        return False

    #akcja tramwaju
    def tram(self,position):
        if self.fields[position].owner!= self.players[self.activePlayer] and self.fields[position].owner!= None:
            self.state = self.WAITINGFORTRAM
            return 'Pole innego gracza. Nie można wejść na to pole!'
        else:
            self.go_to_field(position)


    #akcja na polu idź do więzienia
    def goToPrison(self, player):
        player.position = 9
        player.jailed = 3
        player.total_jailed += 1

    #akcja na polu mały grzyb
    def littleMushroom(self, player):
        player.money -= 15

    # self.players[self.activePlayer]
    def initializeFields(self):
        self.fields = []

        self.fields.append(Field(isSpecial=True,specialFunction=self.startField, imagePath="res/start.png")) #Start
        self.fields.append(Field(name="Współczesne stosunki międzynarodowe", color=(102, 51, 0), financial=(12, 4, 6, 18, 50, 10))) # 1.1 -financial cena,opłata bazowa,opłata 1 poziom,opłata 2 poziom,opłata 3 poziom,cena upgradu
        self.fields.append(Field(name="Szansa", isSpecial=True,specialFunction=self.chanceField , imagePath="res/noimage.png")) # Szansa
        self.fields.append(Field(name="Historia Filozofii", color=(102, 51, 0), financial=(12, 4, 12, 36, 90, 10))) # 1.2
        self.fields.append(Field(isSpecial=True,specialFunction=self.bigMushroom, imagePath="res/noimage.png")) # Grzyb duży
        self.fields.append(Field(name="Wstęp do informatyki", color=(204, 229, 255), financial=(20, 6, 18, 54, 110,10))) # 2.1
        self.fields.append(Field(name="Szansa", isSpecial=True,specialFunction=self.chanceField, imagePath="res/noimage.png")) # Szansa
        self.fields.append(Field(name="Wstęp do programowania w języku Python", color=(204, 229, 255), financial=(20, 6, 18, 54, 110,10))) # 2.2
        self.fields.append(Field(name="Wstęp do programowania w języku C", color=(204, 229, 255), financial=(24, 8, 20, 60, 120,10))) # 2.3
        self.fields.append(Field(isSpecial=True,specialFunction=self.prisonField, imagePath="res/jail.png")) # Więzienie
        self.fields.append(Field(name="Podstawy elektroniki, elektrotechniki i miernictwa", color=(153, 0, 153), financial=(28, 10, 30, 90, 150, 20)))   # 3.1
        self.fields.append(Field(name="Praktyka zawodowa w Nokii", isSpecial=True,specialFunction=self.practiseField,financial=(45,30,0,0,0,0), imagePath="res/noimage.png")) 
        self.fields.append(Field(name="Komunikacja człowiek-komputer", color=(153, 0, 153), financial=(28, 10, 30, 90, 150, 20))) # 3.2
        self.fields.append(Field(name="Systemy wbudowane", color=(153, 0, 153), financial=(32, 12, 36, 100, 180, 20))) # 3.3
        self.fields.append(Field(name="Rozwój systemu zapisów", color=(255, 128, 0), financial=(36, 14, 40, 110, 190, 20))) #4.1
        self.fields.append(Field(name="Szansa", isSpecial=True,specialFunction=self.chanceField, imagePath="res/noimage.png")) # Szansa
        self.fields.append(Field(name="Kurs: Praktyczne aspekty sieci komputerowych", color=(255, 128, 0), financial=(36, 14, 40, 110, 190, 20))) # 4.2
        self.fields.append(Field(name="Kurs: WWW", color=(225, 128, 0), financial=(40, 16, 44, 120, 200, 20))) # 4.3
        self.fields.append(Field(isSpecial=True,specialFunction=self.tramField, imagePath="res/tram.png")) # Tramwaj
        self.fields.append(Field(name="Podstawy grafiki komputerowej", color=(255, 0, 0), financial=(44, 18, 50, 140, 210, 30))) # 5.1
        self.fields.append(Field(name="Szansa", isSpecial=True,specialFunction=self.chanceField, imagePath="res/noimage.png")) # Szansa
        self.fields.append(Field(name="Kurs programowania gier w silniku Unity3D", color=(255, 0, 0), financial=(44, 18, 50, 140, 210, 30))) # 5.2
        self.fields.append(Field(name="Artificial Intelligence for Games", color=(255, 0, 0), financial=(48, 20, 60, 150, 220, 30))) # 5.3
        self.fields.append(Field(name="Kurs języka Java", color=(255, 255, 0), financial=(52, 22, 66, 160, 230, 30))) # 6.1
        self.fields.append(Field(name="Kurs języka Rust", color=(255, 255, 0), financial=(52, 22, 66, 160, 230, 30))) # 6.2
        self.fields.append(Field(name="Praktyka zawodowa w Comarch", isSpecial=True,specialFunction=self.practiseField,financial=(45,30,0,0,0,0)))
        self.fields.append(Field(name="Języki programowania", color=(255, 255, 0), financial=(56, 24, 72, 170, 240, 30))) # 6.3
        self.fields.append(Field(isSpecial=True,specialFunction=self.goToPrison, imagePath="res/gotojail.png")) # Idź do więzienia
        self.fields.append(Field(name="Analiza numeryczna", color=(0, 153, 0), financial=(60, 26, 78, 190, 255, 40))) # 7.1
        self.fields.append(Field(name="Matematyka dyskretna", color=(0, 153, 0), financial=(60, 26, 78, 190, 255, 40))) # 7.2
        self.fields.append(Field(name="Szansa", isSpecial=True,specialFunction=self.chanceField, imagePath="res/noimage.png")) # Szansa
        self.fields.append(Field(name="Algebra", color=(0, 153, 0), financial=(64, 30, 90, 200, 280, 40))) # 7.3
        self.fields.append(Field(name="Szansa", isSpecial=True,specialFunction=self.chanceField, imagePath="res/noimage.png")) # Szansa
        self.fields.append(Field(name="Analiza matematyczna", color=(3, 177, 252), financial=(70, 35, 100, 220, 300, 40))) # 8.1
        self.fields.append(Field(isSpecial=True,specialFunction=self.littleMushroom, imagePath="res/noimage.png")) # Grzyb mały
        self.fields.append(Field(name="Logika dla informatyków", color=(3, 177, 252), financial=(80, 40, 120, 280, 400, 40))) # 8.1

        ''' Testowy algorytm Karola, wraz z dodaniem prawdziwych pól przestanie być on potrzebny
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

    # add > zmiana poziomu pieniędzy gracza
    # get-from-all > otrzymujesz n pieniędzy od wszystkich graczy
    # all > wszyscy gracze dostają n pieniędzy
    # dice > dodatkowy rzut kostką
    # add-if > zmień poziom pieniędzy gracza przy spełnieniu jakiegoś warunku
    # travel > idź na wskazane pole
    # go > idź o n pól do przodu
    # new-house > postaw budynek w danym miejscu
    # go-to-jail > idź do więzienia

    def card_effect(self, player, card, value):

        if card == 'add':
            player.money += value

        elif card == 'get-from-all':
            for p in self.players:
                if not p.bankrupt:
                    p.money -= value
                    player.money += value

        elif card == 'all':
            for p in self.players:
                if not p.bankrupt:
                    p.money += value
        
        elif card == 'dice':
            self.state = self.WAITINGFORDICE

        elif card == 'add-if':
            for i in player.ownedFields:
                if i.name == "Analiza matematyczna":
                    player.money += value

        elif card == 'travel':
            player.position = value
        
        elif card == 'lost':
            value = randint(0, 35)
            player.position = value

        elif card == 'human':
            value = randint(1, 3)
            player.position = value

        elif card == 'go':
            self.go_to_field((player.position + value) % 36)
            
        elif card == 'go-to-jail':
            self.goToPrison(player)

    def initializeCards(self):
        self.cards = [
            ('Zająłeś drugie miejsce w konkursie piękności wydziału informatyki. Otrzymujesz 10 ECTSów.', 'add', 10),
            ('Stworzyłeś mema, który spodobał się pozostałym studentom, a nawet wykładowcy. Pobierz po 5 ECTSów od każdego gracza.', 'get-from-all', 5),
            ('Jak wiadomo, grzyby najszybciej rosną po deszczu. Ze względu na globalne ocieplenie nie otrzymujesz żadnego grzyba, a wręcz przeciwnie. Otrzymujesz 10 ECTSów.', 'add', 10),
            ('Trafiło ci się najłatwiejsze zadanie domowe. Otrzymujesz 5 ECTSów.', 'add', 5),
            ('W ostatniej chwili zdążyłeś na autobus. Rzuć kostką jeszcze raz.', 'dice', 0),
            ('Dźwiękowcy z Hollywood proszą cię o pomoc. Otrzymujesz 50 ECTSów, jeśli posiadasz pole „Analiza matematyczna”.', 'add-if', 50),
            ('Dzięki indyjskim poradnikom na YT udało ci się napisać względnie działający program. Otrzymujesz 10 ECTSów.', 'add', 10),
            ('Kupiłeś procesor AMD, dzięki któremu możesz się uczyć w gorącej atmosferze. To dobrze wpływa na twoje wyniki w nauce.  Otrzymujesz 10 ECTSów.', 'add', 10),
            ('W poszukiwaniu inteligencji udajesz się na pole „Artificial Intelligence for Games”. Jeśli przejdziesz przez start, otrzymujesz 30 ECTSów.', 'travel', 22),
            ('Nareszcie zdałeś egzamin na prawo jazdy. Przesuń pionek o 15 pól do przodu.', 'go', 15),
            ('Wydało się, że nie masz szacunku do logiki. Arnold Schwarzenegger rzuca tobą o ścianę, a profesor odejmuje ci 30 ECTSów.', 'add', -30),
            ('Dostałeś zadanie napisania systemu operacyjnego w Malbolge. Nie podołałeś, przez co tracisz 45 ECTSów.', 'add', -45),
            ('Przez przypadek wszedłeś do budynku wydziału matematyki. Cofnij się o 3 pola.', 'go', -3),
            ('Grzybobranie! Każdy gracz traci 10 ECTSów.', 'all', -10),
            ('Twój mikrofon wydaje dziwne dźwięki, przez co nie możesz zaprezentować swojego rozwiązania na ćwiczeniach. Tracisz 5 ECTSów.', 'add', -5),
            ('Podczas rozwiązywania quizu natrafiasz na błąd "invalidsesskey”, przez który nie możesz przesłać rozwiązania. Tracisz 10 ECTSów.', 'add', -10),
            ('Przez problemy z Internetem nie możesz zaprezentować swojego rozwiązania na ćwiczeniach. Tracisz 10 ECTSów.', 'add', -10),
            ('Zgubiłeś się w budynku uczelni. Idź na losowe pole.', 'lost', 0),
            ('Zapominasz wyłączyć mikrofon na wykładzie, gdy niecenzuralne słowo wymyka się ukradkiem z twoich ust. Tracisz 5 ECTSów.', 'add', -5),
            ('Obudził się w tobie wewnętrzny humanista. Idź na losowe pole brązowe. Jeśli przejdziesz przez start, otrzymujesz 30 ECTSów.', 'human', 0),
            ('Zaspałeś na zajęcia. Tracisz 10 ECTSów.', 'add', -10),
            ('Indukcyjnie udowodniono, że nie ma dla ciebie miejsca na tej uczelni. Tracisz 15 ECTSów.', 'add', -15),
            ('Ukąsił cię jadowity python. Tracisz 10 ECTSów na zakup surowicy.', 'add', -10),
            ('Przez nierozsądne użycie funkcji remove() twój program okazuje się mieć niespodziewanie dużą złożoność obliczeniową i zawiesza ci komputer. Tracisz 10 ECTSów.', 'add', -10),
            ('Nie wyłączywszy wcześniej udostępniania ekranu, wpisujesz niefortunnie „LaTeX insert” w Google. Tracisz 10 ECTSów.', 'add', -10),
            ('Dostałeś na logice zadanie ze zbiorem for(int i = 0; i < 10; i++) {cout<<"w zbiorze ";}. Gubisz się, przez co tracisz 10 ECTSów. ', 'add', -10),
            ('Oszukiwałeś na quizie. Zawiedziony tobą prowadzący odejmuje ci 15 ECTSów.', 'add', -15),
            ('Wysyłasz na SKOS zdjęcie pracy domowej wykonane ziemniakiem, w złym oświetleniu i w jakości 10p.  Nikt nie potrafi przeczytać twojego rozwiązania, przez co tracisz 10 ECTSów.', 'add', -10),
            ('Jako jedyny dostałeś najtrudniejsze zadanie z whitebooka w ramach zadania domowego. Oddajesz po 5 ECTSów każdemu graczowi.', 'get-from-all', -5),
            ('Wielokrotne ścinki sprawiły, że przestałeś dogadywać się ze swoim komputerem. Postanowiłeś zatem udać się na pole „Komunikacja człowiek-komputer”. Jeśli przejdziesz przez start, otrzymujesz 30 ECTSów.', 'travel' ,12),
            ('Przez przypadek wpisałeś w konsolę linuxa "sudo rm -rf /". Idziesz na pole naprawy komputera.', 'go-to-jail', 0)
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
    """# funkcja do testowania interfejsu
    def takeAction(self):
        for p in self.players:
            p.position += randint(1, 12)
            if p.position > 35:
                p.position %= 36

            if self.fields[p.position].owner == None and not self.fields[p.position].isSpecial:
                if random() < 0.05:
                    self.fields[p.position].owner = p
                    p.ownedFields.append(self.fields[p.position])

            elif self.fields[p.position].owner == p and self.fields[p.position].upgradeLevel < 3:
                if random() < 0.20:
                    self.fields[p.position].upgradeLevel += 1"""
    def game_over(self):
        tabela=[]
        for player in self.players:
            tabela.append([player.money,player.ownedFields,player.total_jailed])

        return statistics(tabela)


    def doktorat(self):
        z=0
        for pole in self.players[self.activePlayer].ownedFields:
            if pole.upgradeLevel==3:
                z+=1
        if z>=6:
            self.state = self.KONIECGRY
            return False



        # kliknięcie dla rzutu kością
    def zmiana_aktywnego_gracza(self):
        self.doktorat()
        self.activePlayer +=1
        self.activePlayer %=len(self.players)
        if self.players[self.activePlayer].bankrupt==True:
            self.zmiana_aktywnego_gracza()
        self.state = self.WAITINGFORDICE
        self.players[self.activePlayer].diceroll=0

    #Bankrut:
    def bankrut(self,player):
        player.bankrupt= True
        player.money = 0
        z=0
        for gracz in self.players:
            if gracz.bankrupt == True:
                z+=1
        for pole in player.ownedFields:
            pole.owner=None
            pole.upgradeLevel = 0
        player.ownedFields=[]
        if z==3:
            self.state = self.KONIECGRY
            return False



    def czy_wszyscy_gracze_jeszcze_graja(self):
        for i in self.players:
            if i.money < 0:
                self.bankrut(i)
                #raise Exception("Game:input dice:Bot: coś jest nie tak, Bankrutów jeszcze nie ma!")

    def go_to_field(self,pole):
        # rzut kością, przesunięcie gracza, odpalenie funkcji pola na które stanął
        p = self.players[self.activePlayer]
        pole_stare = p.position
        p.position = pole

        if p.isBot == True:
            if pole<pole_stare:
                if pole!=0:
                    self.startField(p)

            if self.fields[p.position].isSpecial == True:
                self.fields[p.position].specialFunction(p)
                self.zmiana_aktywnego_gracza()
            # nie zajęte pole
            elif self.fields[p.position].owner == None:
                if p.money >= self.fields[p.position].getPurchaseCost():
                    dec = p.botDecidePurchase(self.fields[p.position])  # argumenty???????
                    if (dec == True):
                        p.money -= self.fields[p.position].getPurchaseCost()
                        self.fields[p.position].owner = p
                    self.zmiana_aktywnego_gracza()
                    # wyświetlanie 'nie stać cię na zakup'
                else:
                    self.zmiana_aktywnego_gracza()

            elif self.fields[p.position].owner != p:
                # jakaś animacja albo zanznaczenie przekazania piniędzy?
                oplata = self.fields[p.position].getFeeValue()
                p.money -= oplata
                self.fields[p.position].owner.money += oplata
                if p.money < 0:
                    self.bankrut(p)
                   # raise Exception("Game:input dice:Bot: coś jest nie tak, Bankrutów jeszcze nie ma!")
                    # odkupowanie pola od gracza
                elif p.money < self.fields[p.position].getRepurchaseCost():
                    self.zmiana_aktywnego_gracza()
                else:
                    dec = p.botDecideRepurchase(self.fields[p.position])  # argumenty???????
                    if (dec == True):
                        p.money -= self.fields[p.position].getRepurchaseCost()
                        self.fields[p.position].upgradeLevel = 0
                        self.fields[p.position].owner = p
                    self.zmiana_aktywnego_gracza()
            # Upgrade pola
            elif self.fields[p.position].owner == p:
                if self.fields[p.position].upgradeLevel < 3:
                    if p.money >= self.fields[p.position].getUpgradeCost():
                        dec = p.botDecideUpgrade(self.fields[p.position])
                        if (dec == True):
                            p.money -= self.fields[p.position].getUpgradeCost()
                            self.fields[p.position].upgradeLevel += 1
                        self.zmiana_aktywnego_gracza()
                    else:
                        self.zmiana_aktywnego_gracza()
                else:
                    self.zmiana_aktywnego_gracza()
            #                 self.fields[p.position].owner = p
            #                 p.ownedFields.append(self.fields[p.position])
            else:
                raise Exception("Game:go to:Bot: coś jest nie tak, Gdzie ty jesteś na plansz?",
                                str(p.position))
            raise Exception("Game: go to:Bot: coś jest nie tak, Gdzie ty jesteś na plansz?",str(p.position))


        # -------------------------------------------------------------------------------------------------------------------

        else:  # Active Player is not a bot
            # przechodzenie przez start
            if pole<pole_stare:
                if pole!=0:
                    self.startField(p)

            if self.fields[p.position].isSpecial == True:
                self.state = self.WAITINGFORDECISION
                self.fields[p.position].specialFunction(p)
                self.czy_wszyscy_gracze_jeszcze_graja()
                p.diceroll = 0
                return False


            # nie zajęte pole
            elif self.fields[p.position].owner == None:
                if p.money >= self.fields[p.position].getPurchaseCost():
                    self.state = self.WAITINGFORPURCHASE
                    p.diceroll = 0
                    return False
                    # wyświetlanie 'nie stać cię na zakup'
                else:
                    self.zmiana_aktywnego_gracza()

            elif self.fields[p.position].owner != p:
                # jakaś animacja albo zanznaczenie przekazania piniędzy?
                oplata = self.fields[p.position].getFeeValue()
                p.money -= oplata
                self.fields[p.position].owner.money += oplata

                if p.money < 0:
                    self.bankrut(p)
                    #raise Exception("Game:input dice: coś jest nie tak, Bankrutów jeszcze nie ma!")
                    # odkupowanie pola od gracza

                elif p.money < self.fields[p.position].getRepurchaseCost():
                    self.zmiana_aktywnego_gracza()
                else:
                    self.state = self.WAITINGFORREPURCHASE
                    p.diceroll = 0
                    return False

            # Upgrade pola
            elif self.fields[p.position].owner == p:
                if self.fields[p.position].upgradeLevel < 3:
                    if p.money >= self.fields[p.position].getUpgradeCost():
                        self.state = self.WAITINGFORUPGRADE
                        p.diceroll = 0
                        return False
                    else:
                        self.zmiana_aktywnego_gracza()
                else:
                    self.zmiana_aktywnego_gracza()
            else:
                raise Exception("Game:go to: coś jest nie tak, Gdzie ty jesteś na plansz?",
                                str(p.position))
#--------------------------------------------------------------------------------------------------------------------------------
    def inputDice(self):
        # rzut kością,
        p=self.players[self.activePlayer]
        if p.isBot == True:
            if p.jailed > 0:
                p.jailed -= 1
                if p.money>30:
                    decision = p.botDecideJail()
                    if (decision == True):
                        p.money -= 30
                        p.jailed=0
                    else:
                        self.zmiana_aktywnego_gracza()
                        dice1 = randint(1, 3)
                        dice2 = randint(4, 6)
                        return (dice1, dice2, True)

                    # brake out
                else:
                    dice1 = randint(1, 6)
                    dice2 = randint(1, 6)
                    if dice1 != dice2:
                        self.zmiana_aktywnego_gracza()
                        return (dice1, dice2, True)
                    else:
                        p.jailed=0
                    # jak bot wyszedł kontynujemy program

            dice1 = randint(1, 6)
            dice2 = randint(1, 6)
            pole=p.position+dice1+dice2
            if pole>=36:
                pole=pole%36
            if dice1 == dice2:
                p.diceroll += 1
                if pole== 27:
                    self.goToPrison(p)
                    self.zmiana_aktywnego_gracza()
                    return (dice1, dice2, True)
                else:
                    # 3 dublety z rzędu
                    if p.diceroll == 3:
                        self.state = self.WAITINGFORDECISION
                        self.fields[27].specialFunction(self,p)
                        p.diceroll = 0
                        return (dice1, dice2, True)
                    else:
                        if pole<p.position:
                            p.money+=30
                        p.position=pole
                        self.state = self.WAITINGFORDICE
                        return (dice1, dice2, True)
            self.go_to_field(pole)
            return (dice1, dice2, True)

            #

#-------------------------------------------------------------------------------------------------------------------


        else: # Active Player is not a bot
            if p.jailed > 0:
                p.jailed-=1
                if p.money<30:
                    self.inputDecision('Break_out')
                    return False
                self.state = self.WAITINGFORJAIL
                return False

            dice1 = randint(1, 6)
            dice2 = randint(1, 6)
            pole = p.position + dice1 + dice2
            if pole >=36:
                pole = pole % 36
           # dublety
            if dice1 == dice2:
                p.diceroll+=1
                if p.position == 27:
                    self.goToPrison(p)
                    p.diceroll = 0
                    self.zmiana_aktywnego_gracza()
                    return (dice1,dice2)
                else:
                   # 3 dublety z rzędu
                    if p.diceroll == 3:
                        self.goToPrison(p)
                        p.diceroll = 0
                        self.zmiana_aktywnego_gracza()
                        return (dice1, dice2)
                    else:
                        self.state = self.WAITINGFORDICE
                        if pole<p.position:
                            p.money+=30
                        p.position=pole
                        return (dice1,dice2)
            else:
                self.go_to_field(pole)
                return (dice1, dice2)


    # kliknięcie do podjęcia decyzji (np. kupna pola)

    # kupowanie upgradów, podkupowanie pól graczom, wyjście z więzienia, akceptacja karty szansy itp. itd
    def inputDecision(self, decision):
        p=self.players[self.activePlayer]
        #zakup
        if decision== 'Buy':
            p.money -= self.fields[p.position].getPurchaseCost()
            self.fields[p.position].owner = p
            p.ownedFields.append(self.fields[p.position])
            self.zmiana_aktywnego_gracza()
        #upgrade
        elif decision == 'Upgrade':
            p.money -= self.fields[p.position].getUpgradeCost()
            self.fields[p.position].upgradeLevel +=1
            self.zmiana_aktywnego_gracza()

        #odkup
        elif decision == 'Repurchase':
            p.money -= self.fields[p.position].getRepurchaseCost()
            owner = self.fields[p.position].owner
            self.fields[p.position].upgradeLevel = 0
            self.fields[p.position].owner = p
            owner.ownedFields.remove(self.fields[p.position])
            p.ownedFields.append(self.fields[p.position])
            self.zmiana_aktywnego_gracza()

        #akceptacja
        elif decision == 'Yes':
            self.zmiana_aktywnego_gracza()
            self.czy_wszyscy_gracze_jeszcze_graja()

        #wyjście z więzienia
        elif decision == 'Bribe':
            p.money-= 30 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!kwota?
            p.jailed=0
            self.state = self.WAITINGFORDICE
        #brake out
        elif decision == 'Break_out':
            dice1 = randint(1, 6)
            dice2 = randint(1, 6)
            if dice1!=dice2:
                self.zmiana_aktywnego_gracza()
                return (dice1, dice2)
            self.state = self.WAITINGFORDICE
            p.jailed = 0
            return (dice1,dice2)



        else:
            raise Exception("Game:input decision: coś jest nie tak, Takiej decyzji jeszcze nie ma!")







        pass
