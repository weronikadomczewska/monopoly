
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
        self.cards = [
            'Zająłeś drugie miejsce w konkursie piękności wydziału informatyki. Otrzymujesz 10 ECTSów.',
            'Stworzyłeś mema, który spodobał się pozostałym studentom, a nawet wykładowcy. Pobierz po 5 ECTSów od każdego gracza.',
            'Jak wiadomo, grzyby najszybciej rosną po deszczu. Ze względu na globalne ocieplenie nie otrzymujesz żadnego grzyba, a wręcz przeciwnie. Otrzymujesz 10 ECTSów.',
            'Trafiło ci się najłatwiejsze zadanie domowe. Otrzymujesz 5 ECTSów.',
            'W ostatniej chwili zdążyłeś na autobus. Rzuć kostką jeszcze raz.',
            'Dźwiękowcy z Hollywood proszą cię o pomoc. Otrzymujesz 50 ECTSów, jeśli posiadasz pole „Analiza matematyczna”.',
            'Dzięki indyjskim poradnikom na YT udało Ci się napisać względnie działający program. Otrzymujesz 10 ECTSów.',
            'Grając w Starcrafta II napotkałeś na kolosa. Otrzymujesz kolokwium, które możesz postawić na swoim dowolnym polu. (o ile posiadasz jakiekolwiek pole, na którym można je postawić)', # jeśli będzie to bardziej wygodne do napisania to pole może być losowe
            'Kupiłeś procesor AMD, dzięki któremu możesz się uczyć w ciepłej atmosferze. To dobrze wpływa na twoje wyniki w nauce.  Otrzymujesz 10 ECTSów.',
            'W poszukiwaniu inteligencji udajesz się na pole „Artificial Intelligence for Games”. Jeśli przejdziesz przez start, otrzymujesz 30 ECTSów.',
            'Nareszcie zdałeś egzamin na prawo jazdy. Przesuń pionek o 15 pól do przodu.',
            'Wydało się, że nie masz szacunku do logiki. Arnold Schwarzenegger rzuca Tobą o ścianę, a profesor odejmuje Ci 30 ECTSów.',
            'Dostałeś zadanie napisania systemu operacyjnego w Malbolge. Nie podołałeś, przez co tracisz 45 ECTSów.',
            'Przez przypadek wszedłeś do budynku wydziału matematyki. Cofnij się o 3 pola.',
            'Grzybobranie! Każdy gracz traci 10 ECTSów.',
            'Twój mikrofon wydaje dziwne dźwięki, przez co nie możesz zaprezentować swojego rozwiązania na ćwiczeniach. Tracisz 5 ECTSów.',
            'Podczas rozwiązywania quizu natrafiasz na błąd "invalidsesskey”, przez który nie możesz przesłać rozwiązania. Tracisz 10 ECTSów.',
            'Przez problemy z Internetem nie możesz zaprezentować swojego rozwiązania na ćwiczeniach. Tracisz 10 ECTSów.',
            'Zgubiłeś się w budynku uczelni. Idź na losowe pole.',
            'Zapominasz wyłączyć mikrofon na wykładzie, gdy niecenzuralne słowo wymyka się ukradkiem z twoich ust. Tracisz 5 ECTSów.',
            'Obudził się w tobie wewnętrzny humanista. Idź na losowe pole brązowe. Jeśli przejdziesz przez start, otrzymujesz 30 ECTSów.',
            'Zaspałeś na zajęcia. Tracisz 10 ECTSów.',
            'Indukcyjnie udowodniono, że nie ma dla ciebie miejsca na tej uczelni. Tracisz 15 ECTSów.',
            'Ukąsił cię jadowity python. Tracisz 10 ECTSów na zakup surowicy.',
            'Przez nierozsądne użycie funkcji remove() twój program okazuje się mieć niespodziewanie dużą złożoność algorytmiczną i zawiesza ci komputer. Tracisz 10 ECTSów.',
            'Nie wyłączywszy wcześniej udostępniania ekranu wpisujesz niefortunnie „LaTeX insert” w Google. Tracisz 10 ECTSów.',
            'Dostałeś na logice zadanie ze zbiorem for(int i = 0; i < 10; i++) {cout<<”w zbiorze „;}. Gubisz się, przez co tracisz 10 ECTSów. ',
            'Oszukiwałeś na quizie. Zawiedziony tobą BBe odejmuje ci 15 ECTSów.',
            'Wysyłasz na SKOS zdjęcie pracy domowej wykonane ziemniakiem, w złym oświetleniu i w jakości 10p.  Nikt nie może się doczytać twojego rozwiązania, przez co tracisz 10 ECTSów.',
            'Jako jedyny dostałeś najtrudniejsze zadanie z whitebooka w ramach zadania domowego. Oddajesz po 5 ECTSów każdemu graczowi.',
            'Wielokrotne ścinki sprawiają, że przestajesz dogadywać się ze swoim komputerem. Postanawiasz zatem udać się na pole „Komunikacja człowiek-komputer”. Jeśli przejdziesz przez start, otrzymujesz 30 ECTSów.',
            'Przez przypadek wpisałeś w konsolę linuxa "sudo rm -rf /". Idziesz na pole naprawy komputera.'       
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

            elif self.fields[p.position].owner == p and self.fields[p.position].upgradeLevel < 3:
                if random() < 0.20:
                    self.fields[p.position].upgradeLevel += 1