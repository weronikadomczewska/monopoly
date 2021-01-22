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
        self.jailed = 0
        self.position = 0
        self.ownedFields = []
        self.total_jailed = 0
        
        self.bankrupt = False

        self.riskLevel = random.random()
        self.aggressionLevel = random.random()
        
    def botDecidePurchase(self, field):
        return True if random.random() <= self.riskLevel else False

    def botDecideRepurchase(self, field):
        return True if random.random() <= self.aggressionLevel else False

    def botDecideUpgrade(self, field):
        risk = self.riskLevel
        ownedMoney = self.money
        costOfUpgrade = field.getUpgradeCost() # koszt ulepszenia pola
        percentOfBudget = costOfUpgrade / ownedMoney #jaki procent budżetu będzie poświęcony na zakup pola

        if percentOfBudget >= 0.75:
            if risk >= 0.95:
                return True
            else:
                return False

        elif 0.5 <= percentOfBudget < 0.75:
            if risk >= 0.5:
                return True
            else:
                return False

        elif 0.25 <= percentOfBudget < 0.5:
            if risk >= 0.3:
                return True
            else:
                return False
        else:
            return True

    #True - wykupuje się
    # False - rzuca dalej kośćmi        
    def botDecideJail(self, field):
        aggression = self.aggressionLevel
        ownedMoney = self.money

        if aggression >= 0.8:
            return True

        costOfBribe = 50 #koszt wykupienia się z więzienia
        percentOfBudget = costOfBribe / ownedMoney #procent budżetu, jaki stanowi wykupienie się z więzenia

        if 0 < percentOfBudget < 0.15:
            return True 
        elif 0.15 <= percentOfBudget < 0.3:
            if aggression >= 0.4:
                return True
            else:
                return False
        elif 0.3 <= percentOfBudget < 0.5:
            if aggression >= 0.6:
                return True
            else:
                return False
        elif 0.5 <= percentOfBudget < 0.7:
            if 0.6 < aggression < 0.8:
                return True
            else:
                return False

        else:
            return False 



# przykłady stworzenia nowego gracza
#
# p1 = Player(isBot=True, color=(255, 0, 0), money=600) - tworzy gracza komputerowego o kolorze czerwonym, który posiada 600 pieniędzy
# p2 = Player(money=100) - tworzy gracza (niekomputerowego) o kolorze czarnym i gotówce 100
