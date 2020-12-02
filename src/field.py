
''' klasa reprezentująca pojedyncze pole na planszy w grze '''
class Field:

    ''' 
    konstruktor pola

    Argumenty:
        name (str): nazwa tworzonego pola
        color (tuple(int, int, int)): kolor reprezentujący tworzone pole (RGB)
        financial (tuple(int, int, int, int, int)): ... TODO: uzupełnić informacje co znaczy co 
        isSpecial (bool): czy tworzone pole, jest polem specjalnym
        specialFunction (func(Player)): funkcja, która przyjmuje przez argument gracza i wykonuje specjalną akcję pola, None jeśli pole nie jest specjalne

    '''
    def __init__(self, name="DEFAULT", color=(0, 0, 0), financial=(0, 0, 0, 0, 0), isSpecial=False, specialFunction=None):
        self.name = name
        self.color = color
        self.financial = financial
        self.isSpecial = isSpecial
        self.specialFunction = specialFunction
        self.upgradeLevel = 0
        self.owner = None

    '''
    zwraca kwotę, którą musi zapłacić gracz, aby kupić wolne pole
    
    Zwraca:
        (int): kwota, którą musi zapłacić gracz, aby kupić wolne pole

    '''
    def getPurchaseCost(self):
        raise NotImplementedError("TODO: zaimplementować Field:getPurchaseCost()")

    '''
    zwraca kwotę, którą musi zapłacić gracz (nie posiadacz), który na polu stanie
    
    Zwraca:
        (int): kwota, którą musi zapłacić gracz (nie posiadacz), który na polu stanie

    '''
    def getFeeValue(self):
        raise NotImplementedError("TODO: zaimplementować Field:getFeeValue()")

    '''
    zwraca kwotę, jaką należy zapłacić, aby ulepszyć pole

    Zwraca:
        (int): kwota, jaką należy zapłacić, aby ulepszyć pole

    '''
    def getUpgradeCost(self):
        raise NotImplementedError("TODO: zaimplementować Field:getUpgradeCost()")

    '''
    zwraca kwotę, jaką należy zapłacić, aby odkupić pole

    Zwraca:
        (int): kwota, jaką należy zapłacić, aby odkupić pole

    '''
    def getRepurchaseCost(self):
        raise NotImplementedError("TODO: zaimplementować Field:getRepurchaseCost()")

# przykłady stworzenia nowego gracza
#
# p1 = Player(isBot=True, color=(255, 0, 0), money=600) - tworzy gracza komputerowego o kolorze czerwonym, który posiada 600 pieniędzy
# p2 = Player(money=100) - tworzy gracza (niekomputerowego) o kolorze czarnym i gotówce 100
