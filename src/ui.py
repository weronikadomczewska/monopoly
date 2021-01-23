import pygame
from game import Game
from player import Player
import time

class UI:

    PREGAME = 0
    INGAME = 1
    POSTGAME = 2

    def __init__(self):
        self.game = None
        self.closed = False
        self.needRedraw = True
        self.clicked = False
        self.drawDice = False
        self.fields = []
        self.fieldName = ""
        self.state = self.PREGAME
        self.stateTextSplit = False
        self.botGame = False
        self.buttons = {}
        self.buttonLayout = []

        pygame.display.init()
        info = pygame.display.Info()
        pygame.display.set_caption("Monopoly UWR")
        # self.surface = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        self.surface = pygame.display.set_mode((info.current_w - 300, info.current_h - 150), pygame.RESIZABLE)

        pygame.font.init()
        self.fontName = "Courier"

        self.fontsBold = {
            32: pygame.font.SysFont(self.fontName, 32, True)
        }
        self.fonts = {
            32: pygame.font.SysFont(self.fontName, 32, False)
        }

        self.timer = time.time()
        
        # wczytanie obrazków
        self.images = {}
        for i in range(1, 7):
            self.images[f"dice{i}"] = pygame.image.load(f"res/dice{i}.png")


    def detectClick(self, mousePos, rect):
        return (rect[0] <= mousePos[0] <= rect[2]) and (rect[1] <= mousePos[1] <= rect[3])

    def getField(self, mousePos):
        for i in range(len(self.fields)):
            if self.detectClick(mousePos, self.fields[i]):
                return i
        return -1

    def gameTick(self):

        if self.state == self.PREGAME:

            players = -1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closed = True

                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    if width < 1280:
                        pygame.display.set_mode((1280, pygame.display.get_window_size()[1]), pygame.RESIZABLE)
                    if height < 720:
                        pygame.display.set_mode((pygame.display.get_window_size()[0], 720), pygame.RESIZABLE)
                    self.needRedraw = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        players = 0
                    elif event.key == pygame.K_1:
                        players = 1
                    elif event.key == pygame.K_2:
                        players = 2
                    elif event.key == pygame.K_3:
                        players = 3
                    elif event.key == pygame.K_4:
                        players = 4

            if self.needRedraw:
                self.surface.fill((255, 255, 255))
                self.drawStartScreen()
                pygame.display.update()
                self.needRedraw = False

            if players != -1:
                self.game = Game()
                if players == 0:
                    self.botGame = True
                    player1 = Player(color=(255, 0, 0), isBot=True)
                    player2 = Player(color=(0, 255, 0), isBot=True)
                    player3 = Player(color=(0, 0, 255), isBot=True)
                    player4 = Player(color=(255, 255, 0), isBot=True)

                    self.game.addPlayer(player1)
                    self.game.addPlayer(player2)
                    self.game.addPlayer(player3)
                    self.game.addPlayer(player4)

                elif players == 1:
                    player1 = Player(color=(255, 0, 0))
                    player2 = Player(color=(0, 255, 0), isBot=True)
                    player3 = Player(color=(0, 0, 255), isBot=True)
                    player4 = Player(color=(255, 255, 0), isBot=True)

                    self.game.addPlayer(player1)
                    self.game.addPlayer(player2)
                    self.game.addPlayer(player3)
                    self.game.addPlayer(player4)

                elif players == 2:
                    player1 = Player(color=(255, 0, 0))
                    player2 = Player(color=(0, 255, 0))
                    player3 = Player(color=(0, 0, 255), isBot=True)
                    player4 = Player(color=(255, 255, 0), isBot=True)

                    self.game.addPlayer(player1)
                    self.game.addPlayer(player2)
                    self.game.addPlayer(player3)
                    self.game.addPlayer(player4)

                elif players == 3:
                    player1 = Player(color=(255, 0, 0))
                    player2 = Player(color=(0, 255, 0))
                    player3 = Player(color=(0, 0, 255))
                    player4 = Player(color=(255, 255, 0), isBot=True)

                    self.game.addPlayer(player1)
                    self.game.addPlayer(player2)
                    self.game.addPlayer(player3)
                    self.game.addPlayer(player4)

                elif players == 4:
                    player1 = Player(color=(255, 0, 0))
                    player2 = Player(color=(0, 255, 0))
                    player3 = Player(color=(0, 0, 255))
                    player4 = Player(color=(255, 255, 0))

                    self.game.addPlayer(player1)
                    self.game.addPlayer(player2)
                    self.game.addPlayer(player3)
                    self.game.addPlayer(player4)

                for f in self.game.fields:
                    if f.isSpecial:
                        if f.imagePath not in self.images:
                            self.images[f.imagePath] = pygame.image.load(f.imagePath)

                self.state = self.INGAME
                self.needRedraw = True
                return


        
        elif self.state == self.INGAME:
            # przetworzenie zdarzeń okna gry
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closed = True

                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    if width < 1280:
                        pygame.display.set_mode((1280, pygame.display.get_window_size()[1]), pygame.RESIZABLE)
                    if height < 720:
                        pygame.display.set_mode((pygame.display.get_window_size()[0], 720), pygame.RESIZABLE)
                    self.needRedraw = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

                if event.type == pygame.MOUSEMOTION:
                    f = self.getField(pygame.mouse.get_pos())
                    if f != -1:
                        self.fieldName = self.game.fields[f].name
                    else:
                        self.fieldName = ""
                    self.needRedraw = True

            # obsługa stanów gry
            if self.game.state == self.game.WAITINGFORDICE:
                self.setButtons({0: ("Rzuć kostką", self.rollDice)})
                self.stateText = "Kliknij w przycisk, aby rzucić kością"
                if self.clicked == True:
                    self.runButtons()
                    self.needRedraw = True

            elif self.game.state == self.game.WAITINGFORDECISION:
                self.setButtons({0: ("Potwierdź", "Yes")})
                try:
                    self.stateText = self.game.specialText
                except:
                    print(self.game.players[self.game.activePlayer].position)
                self.stateTextSplit = True
                if self.clicked == True:
                    self.runButtons()
                    self.needRedraw = True
                    self.stateTextSplit = False

            elif self.game.state == self.game.WAITINGFORPURCHASE:
                self.setButtons({0: ("Zapisz się", "Buy"), 1: ("Nie zapisuj się", "Yes")})
                self.stateText = "Czy chcesz zapisać się na ten przedmiot?"
                if self.clicked == True:
                    self.runButtons()
                    self.needRedraw = True

            elif self.game.state == self.game.WAITINGFORREPURCHASE:
                self.setButtons({0: ("Podebranie", "Repurchase"), 1: ("Nie...", "Yes")})
                self.stateText = "Czy chcesz podebrać ten przedmiot?"
                if self.clicked == True:
                    self.runButtons()
                    self.needRedraw = True

            elif self.game.state == self.game.WAITINGFORUPGRADE:
                self.setButtons({0: ("Napisz", "Upgrade"), 1: ("Nie pisz", "Yes")})
                self.stateText = "Czy chcesz napisać pracę?"
                if self.clicked == True:
                    self.runButtons()
                    self.needRedraw = True

            elif self.game.state == self.game.WAITINGFORJAIL:
                self.setButtons({0: ("Napraw", "Bribe"), 1: ("Licz na cud...", "Yes")})
                self.stateText = "Czy chcesz naprawić swój komputer?"
                if self.clicked == True:
                    self.runButtons()
                    self.needRedraw = True

            elif self.game.state == self.game.WAITINGFORTRAM:
                self.setButtons({})
                self.stateText = "Kliknij w przedmiot, na który chcesz się udać"
                if self.clicked == True:
                    f = self.getField(pygame.mouse.get_pos())
                    if f != -1:
                        self.game.tram(f)
                    self.needRedraw = True

            # self.winner przechowuje wygranego
            elif self.game.state == self.game.KONIECGRY:
                self.setButtons({0: ("OK", self.endGame)})
                self.stateText = "Koniec gry! Wygrywa " + ["Czerwony!", "Zielony!", "Niebieski!", "Żółty!"][self.game.players.index(self.game.winner)]
                if self.clicked == True:
                    
                    self.needRedraw = True
                    return


            # leniwe rysowanie interfejsu - tylko wtedy gdy jest potrzeba
            if self.needRedraw:
                self.surface.fill((255, 255, 255)) # czyszczenie ekranu
                self.drawUI()
                self.needRedraw = False
                pygame.display.update() # pokazanie narysowanego interfejsu
            
            # czyszczenie
            self.clicked = False

        elif self.state == self.POSTGAME:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.closed = True

                if event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    if width < 1280:
                        pygame.display.set_mode((1280, pygame.display.get_window_size()[1]), pygame.RESIZABLE)
                    if height < 720:
                        pygame.display.set_mode((pygame.display.get_window_size()[0], 720), pygame.RESIZABLE)
                    self.needRedraw = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.closed = True

            if self.needRedraw:
                self.surface.fill((255, 255, 255))
                self.drawStatsScreen()
                pygame.display.update()
                self.needRedraw = False

        else:
            raise Exception("nieznany stan UI")

    def renderText(self, text, bold=True, size=32, color=(0, 0, 0)):

        font = None
        if bold:
            if size in self.fontsBold:
                font = self.fontsBold[size]
            else:
                newFont = pygame.font.SysFont(self.fontName, size, True)
                font = newFont
                self.fontsBold[size] = newFont

        else:
            if size in self.fonts:
                font = self.fonts[size]
            else:
                newFont = pygame.font.SysFont(self.fontName, size, False)
                font = newFont
                self.fonts[size] = newFont
        
        return font.render(text, True, color) if bold else font.render(text, True, color)
        
    # rysowanie interfejsu
    def drawUI(self):

        self.fields = []

        w = self.surface.get_width() # szerokość okna
        h = self.surface.get_height() # wysokość okna
        boardSize = min(w, h) - (min(w, h) / 8) # długość boku planszy
        marginHorizontal = (w - boardSize) / 2 # margines poziomy
        marginVertical = (h - boardSize) / 2 # margines pionowy
        fieldWidth = (boardSize / 11) # "szerokość" pola
        cornerSize = fieldWidth * 1.5 # rozmiar pola narożnego
        fieldHeight = cornerSize # "wysokość" pola, taka sama jak pole narożne
        borderWidth = 2 # szerokość obrysu pól

        # rysowanie nazwy najechanego pola
        text = self.renderText(self.fieldName)
        scaleFactor = (3 * marginVertical / 4) / text.get_height()
        text = pygame.transform.smoothscale(text, (int(text.get_width() * scaleFactor), int(3 * marginVertical / 4)))
        self.surface.blit(text, (marginHorizontal + boardSize / 2 - text.get_width() / 2, marginVertical / 2 - text.get_height() / 2))

        # rysowanie informacji o graczach 
        self.drawPlayerInfo(marginHorizontal + cornerSize + 5, marginVertical + cornerSize + 5, (boardSize - 2 * cornerSize) / 2)

        # rysowanie guzików i tekstu
        for i in self.buttons:
            buttonText, _ = self.buttons[i]
            lay = self.buttonLayout[i]
            width = lay[2] - lay[0]
            height = lay[3] - lay[1]
            rect = pygame.Rect(lay[0], lay[1], width, height)
            pygame.draw.rect(self.surface, (0, 0, 0), rect, 2)
            text = self.renderText(buttonText)
            scaleFactor = (width - 20) / text.get_width()
            if scaleFactor < 1:
                text = pygame.transform.smoothscale(text, (int(text.get_width() * scaleFactor), int(text.get_height() * scaleFactor)))
            self.surface.blit(text, (lay[0] + width / 2 - text.get_width() / 2, lay[1] + height / 2 - text.get_height() / 2))

        if self.stateTextSplit:
            length = len(self.stateText)
            pos = length // 2
            while self.stateText[pos] != ' ':
                pos += 1
            stateText = [self.stateText[:pos], self.stateText[pos + 1:]]
        else:
            stateText = [self.stateText]

        off = 0
        for s in stateText:
            text = self.renderText(s)
            scaleFactor = ((boardSize - 2 * cornerSize) - 40) / text.get_width()
            if scaleFactor < 1:
                text = pygame.transform.smoothscale(text, (int(text.get_width() * scaleFactor), int(text.get_height() * scaleFactor)))
            x = marginHorizontal + cornerSize + (boardSize - 2 * cornerSize) / 2 - text.get_width() / 2
            y = off + marginVertical + (3 * boardSize / 4) - cornerSize
            self.surface.blit(text, (x, y))
            off += text.get_height() + 4

        # rysowanie kostek po rzucie
        if self.drawDice:
            firstImage = self.images[f"dice{self.drawDice[0]}"]
            secondImage = self.images[f"dice{self.drawDice[1]}"]

            diceSize = fieldWidth / 1.5
            firstImage = pygame.transform.smoothscale(firstImage, (int(diceSize), int(diceSize)))
            secondImage = pygame.transform.smoothscale(secondImage, (int(diceSize), int(diceSize)))

            x = marginHorizontal + boardSize - fieldHeight - 2.2 * diceSize
            y = marginVertical + cornerSize + 5

            # napis "Kości"
            dice = self.renderText("Kości")
            scaleFactor = (diceSize * 2) / dice.get_width()
            dice = pygame.transform.smoothscale(dice, (int(dice.get_width() * scaleFactor), int(dice.get_height())))
            self.surface.blit(dice, (x, y))
            y += diceSize * 0.75

            self.surface.blit(firstImage, (x, y))
            x += diceSize
            self.surface.blit(secondImage, (x, y))
            y += diceSize
            x -= diceSize

            if self.drawDice[0] == self.drawDice[1]:
                double = self.renderText("Dublet!")
                scaleFactor = (diceSize * 2) / double.get_width()
                double = pygame.transform.smoothscale(double, (int(double.get_width() * scaleFactor), int(double.get_height())))
                self.surface.blit(double, (x, y))

        x = marginHorizontal + boardSize - cornerSize
        y = marginVertical + boardSize - cornerSize

        rect = pygame.Rect(x, y, cornerSize, cornerSize)
        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
        offset = 0
        self.fields.append((x, y, x + cornerSize, y + cornerSize))

        px = x + (cornerSize / 12)
        py = y + (cornerSize / 12)
        counter = 0
        for p in self.game.players:
            if p.position == offset and not p.bankrupt:
                center = (px + cornerSize / 12, py + cornerSize / 12)
                pygame.draw.circle(self.surface, p.color, center, fieldWidth / 8)
                pygame.draw.circle(self.surface, (0, 0, 0), center, fieldWidth / 8, 1)

                if counter == 0:
                    px += (cornerSize / 4.4) * 3
                elif counter == 1:
                    py += (cornerSize / 4.4) * 3
                elif counter == 2:
                    px -= (cornerSize / 4.4) * 3

                counter += 1

        image = self.images[self.game.fields[0].imagePath]
        image = pygame.transform.smoothscale(image, (int(cornerSize / 1.5), int(cornerSize / 1.5)))
        self.surface.blit(image, (x + (cornerSize / 2) - int(cornerSize / 3), y + (cornerSize / 2) - int(cornerSize / 3)))

        x -= fieldWidth

        offset = 1

        for _ in range(8):
            rect = pygame.Rect(x, y, fieldWidth, fieldHeight)
            pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

            self.fields.append((x, y, x + fieldWidth, y + fieldHeight))

            if not self.game.fields[offset].isSpecial:

                if self.game.fields[offset].owner != None:
                    off = fieldHeight / 5
                    rect = pygame.Rect(x + fieldWidth - off, y + fieldHeight - (fieldHeight / 5) - off + 2, off, off)
                    pygame.draw.rect(self.surface, self.game.fields[offset].owner.color, rect)
                    pygame.draw.rect(self.surface, (0, 0, 0), rect, 2)
                
                # ulepszenia
                upgradeLevel = self.game.fields[offset].upgradeLevel
                if upgradeLevel > 0:
                    if upgradeLevel == 1:
                        width = fieldWidth / 3
                        height = width * 1.2
                        rect = pygame.Rect(x + (fieldWidth / 4), y + (fieldHeight / 4), width, height)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                    elif upgradeLevel == 2:
                        width = fieldWidth / 3
                        height = width * 1.2
                        rect = pygame.Rect(x + (fieldWidth / 4), y + (fieldHeight / 4), width, height)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                        rect = pygame.Rect(x + (fieldWidth / 4) + fieldWidth / 12, y + (fieldHeight / 4) + fieldWidth / 12, width, height)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                    else:
                        width = fieldWidth / 2
                        height = width
                        rect = pygame.Rect(x + (fieldWidth / 4), y + (fieldHeight / 4), width, height)
                        pygame.draw.rect(self.surface, (198, 245, 236), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

                # kolorowy pasek
                rect = pygame.Rect(x, y + (4 * fieldHeight / 5), fieldWidth, fieldHeight / 5)
                pygame.draw.rect(self.surface, self.game.fields[offset].color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

                # cena pola
                priceTag = None
                isBold = False
                if self.game.fields[offset].owner == None:
                    priceTag = self.game.fields[offset].getPurchaseCost()
                else:
                    priceTag = self.game.fields[offset].getFeeValue()
                    isBold = True
                priceTag = self.renderText(str(priceTag), bold=isBold)
                scaleFactor = (fieldHeight / 5) / priceTag.get_height()
                priceTag = pygame.transform.smoothscale(priceTag, (int(priceTag.get_width() * scaleFactor), int(fieldHeight / 5)))
                self.surface.blit(priceTag, (x + (fieldWidth / 2) - (priceTag.get_width() / 2), y + (4 * fieldHeight / 5)))

            # gracze
            px = x + (fieldWidth / 12) 
            py = y + (fieldWidth / 12) 
            for p in self.game.players:
                if p.position == offset and not p.bankrupt:
                    center = (px + fieldWidth / 10, py + fieldWidth / 10)
                    pygame.draw.circle(self.surface, p.color, center, fieldWidth / 8)
                    pygame.draw.circle(self.surface, (0, 0, 0), center, fieldWidth / 8, 1)
                    px += fieldWidth / 8 + fieldWidth / 12

            x -= fieldWidth
            offset += 1

        x -= (fieldWidth / 2)

        rect = pygame.Rect(x, y, cornerSize, cornerSize)
        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
        self.fields.append((x, y, x + cornerSize, y + cornerSize))

        px = x + (cornerSize / 12)
        py = y + (cornerSize / 12)
        counter = 0
        for p in self.game.players:
            if p.position == offset and not p.bankrupt:
                center = (px + cornerSize / 12, py + cornerSize / 12)
                pygame.draw.circle(self.surface, p.color, center, fieldWidth / 8)
                pygame.draw.circle(self.surface, (0, 0, 0), center, fieldWidth / 8, 1)

                if counter == 0:
                    px += (cornerSize / 4.4) * 3
                elif counter == 1:
                    py += (cornerSize / 4.4) * 3
                elif counter == 2:
                    px -= (cornerSize / 4.4) * 3

                counter += 1

        image = self.images[self.game.fields[offset].imagePath]
        image = pygame.transform.smoothscale(image, (int(cornerSize / 1.5), int(cornerSize / 1.5)))
        self.surface.blit(image, (x + (cornerSize / 2) - int(cornerSize / 3), y + (cornerSize / 2) - int(cornerSize / 3)))

        offset += 1
        y -= fieldWidth

        for _ in range(8):
            rect = pygame.Rect(x, y, fieldHeight, fieldWidth)
            pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

            self.fields.append((x, y, x + fieldHeight, y + fieldWidth))

            if not self.game.fields[offset].isSpecial:
                
                if self.game.fields[offset].owner != None:

                    off = fieldHeight / 5
                    rect = pygame.Rect(x + (fieldHeight / 5) - 2, y, off, off)
                    pygame.draw.rect(self.surface, self.game.fields[offset].owner.color, rect)
                    pygame.draw.rect(self.surface, (0, 0, 0), rect, 2)

                # ulepszenia
                upgradeLevel = self.game.fields[offset].upgradeLevel
                if upgradeLevel > 0:
                    if upgradeLevel == 1:
                        width = fieldWidth / 3
                        height = width * 1.2
                        rect = pygame.Rect(x + (fieldHeight / 4) + (fieldHeight / 6), y + (fieldWidth / 4), height, width)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                        pass
                    elif upgradeLevel == 2:
                        width = fieldWidth / 3
                        height = width * 1.2
                        rect = pygame.Rect(x + (fieldHeight / 4) + (fieldHeight / 6), y + (fieldWidth / 4), height, width)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                        rect = pygame.Rect(x + (fieldHeight / 4) + (fieldHeight / 6) + (fieldWidth / 12), y + (fieldWidth / 4) + (fieldWidth / 12), height, width)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                    else:
                        width = fieldWidth / 2
                        height = width
                        rect = pygame.Rect(x + (fieldHeight / 4) + (fieldHeight / 6), y + (fieldWidth / 4), height, width)
                        pygame.draw.rect(self.surface, (198, 245, 236), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

                # kolorowy pasek
                rect = pygame.Rect(x, y, fieldHeight / 5, fieldWidth)
                pygame.draw.rect(self.surface, self.game.fields[offset].color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

                # cena pola
                priceTag = None
                isBold = False
                if self.game.fields[offset].owner == None:
                    priceTag = self.game.fields[offset].getPurchaseCost()
                else:
                    priceTag = self.game.fields[offset].getFeeValue()
                    isBold = True
                priceTag = self.renderText(str(priceTag), bold=isBold)
                scaleFactor = (fieldHeight / 5) / priceTag.get_height()
                priceTag = pygame.transform.smoothscale(priceTag, (int(priceTag.get_width() * scaleFactor), int(fieldHeight / 5)))
                priceTag = pygame.transform.rotate(priceTag, 270)
                self.surface.blit(priceTag, (x, y + (fieldWidth / 2) - (priceTag.get_width() / 2)))

            # gracze
            px = x + fieldHeight - (fieldHeight / 6)
            py = y + (fieldWidth / 12) 
            for p in self.game.players:
                if p.position == offset and not p.bankrupt:
                    center = (px + fieldWidth / 10, py + fieldWidth / 10)
                    pygame.draw.circle(self.surface, p.color, center, fieldWidth / 8)
                    pygame.draw.circle(self.surface, (0, 0, 0), center, fieldWidth / 8, 1)
                    py += fieldWidth / 8 + fieldWidth / 12

            y -= fieldWidth
            offset += 1

        y -= (fieldWidth / 2)
        rect = pygame.Rect(x, y, cornerSize, cornerSize)
        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
        self.fields.append((x, y, x + cornerSize, y + cornerSize))

        px = x + (cornerSize / 12)
        py = y + (cornerSize / 12)
        counter = 0
        for p in self.game.players:
            if p.position == offset and not p.bankrupt:
                center = (px + cornerSize / 12, py + cornerSize / 12)
                pygame.draw.circle(self.surface, p.color, center, fieldWidth / 8)
                pygame.draw.circle(self.surface, (0, 0, 0), center, fieldWidth / 8, 1)

                if counter == 0:
                    px += (cornerSize / 4.4) * 3
                elif counter == 1:
                    py += (cornerSize / 4.4) * 3
                elif counter == 2:
                    px -= (cornerSize / 4.4) * 3

                counter += 1

        image = self.images[self.game.fields[offset].imagePath]
        image = pygame.transform.smoothscale(image, (int(cornerSize / 1.5), int(cornerSize / 1.5)))
        self.surface.blit(image, (x + (cornerSize / 2) - int(cornerSize / 3), y + (cornerSize / 2) - int(cornerSize / 3)))

        offset += 1
        x += cornerSize

        for _ in range(8):
            rect = pygame.Rect(x, y, fieldWidth, fieldHeight)
            pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

            self.fields.append((x, y, x + fieldWidth, y + fieldHeight))

            if not self.game.fields[offset].isSpecial:

                if self.game.fields[offset].owner != None:

                    off = fieldHeight / 5
                    rect = pygame.Rect(x + fieldWidth - off, y + off - 2, off, off)
                    pygame.draw.rect(self.surface, self.game.fields[offset].owner.color, rect)
                    pygame.draw.rect(self.surface, (0, 0, 0), rect, 2)

                # ulepszenia
                upgradeLevel = self.game.fields[offset].upgradeLevel
                if upgradeLevel > 0:
                    if upgradeLevel == 1:
                        width = fieldWidth / 3
                        height = width * 1.2
                        rect = pygame.Rect(x + (fieldWidth / 4), y + (fieldHeight / 4) + (fieldHeight / 6), width, height)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                    elif upgradeLevel == 2:
                        width = fieldWidth / 3
                        height = width * 1.2
                        rect = pygame.Rect(x + (fieldWidth / 4), y + (fieldHeight / 4) + (fieldHeight / 6), width, height)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                        rect = pygame.Rect(x + (fieldWidth / 4) + fieldWidth / 12, y + (fieldHeight / 4) + (fieldHeight / 6) + fieldWidth / 12, width, height)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                    else:
                        width = fieldWidth / 2
                        height = width
                        rect = pygame.Rect(x + (fieldWidth / 4), y + (fieldHeight / 4) + (fieldHeight / 6), width, height)
                        pygame.draw.rect(self.surface, (198, 245, 236), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

                # kolorwy pasek
                rect = pygame.Rect(x, y, fieldWidth, fieldHeight / 5)
                pygame.draw.rect(self.surface, self.game.fields[offset].color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

                # cena pola
                priceTag = None
                isBold = False
                if self.game.fields[offset].owner == None:
                    priceTag = self.game.fields[offset].getPurchaseCost()
                else:
                    priceTag = self.game.fields[offset].getFeeValue()
                    isBold = True
                priceTag = self.renderText(str(priceTag), bold=isBold)
                scaleFactor = (fieldHeight / 5) / priceTag.get_height()
                priceTag = pygame.transform.smoothscale(priceTag, (int(priceTag.get_width() * scaleFactor), int(fieldHeight / 5)))
                self.surface.blit(priceTag, (x + (fieldWidth / 2) - (priceTag.get_width() / 2), y))

            # gracze
            px = x + (fieldWidth / 12)
            py = y + fieldHeight - (fieldWidth / 4) 
            for p in self.game.players:
                if p.position == offset and not p.bankrupt:
                    center = (px + fieldWidth / 10, py + fieldWidth / 10)
                    pygame.draw.circle(self.surface, p.color, center, fieldWidth / 8)
                    pygame.draw.circle(self.surface, (0, 0, 0), center, fieldWidth / 8, 1)
                    px += fieldWidth / 8 + fieldWidth / 12

            x += fieldWidth
            offset += 1

        rect = pygame.Rect(x, y, cornerSize, cornerSize)
        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
        self.fields.append((x, y, x + cornerSize, y + cornerSize))

        px = x + (cornerSize / 12)
        py = y + (cornerSize / 12)
        counter = 0
        for p in self.game.players:
            if p.position == offset and not p.bankrupt:
                center = (px + cornerSize / 12, py + cornerSize / 12)
                pygame.draw.circle(self.surface, p.color, center, fieldWidth / 8)
                pygame.draw.circle(self.surface, (0, 0, 0), center, fieldWidth / 8, 1)

                if counter == 0:
                    px += (cornerSize / 4.4) * 3
                elif counter == 1:
                    py += (cornerSize / 4.4) * 3
                elif counter == 2:
                    px -= (cornerSize / 4.4) * 3

                counter += 1

        image = self.images[self.game.fields[offset].imagePath]
        image = pygame.transform.smoothscale(image, (int(cornerSize / 1.5), int(cornerSize / 1.5)))
        self.surface.blit(image, (x + (cornerSize / 2) - int(cornerSize / 3), y + (cornerSize / 2) - int(cornerSize / 3)))

        offset += 1
        y += cornerSize

        for _ in range(8):
            rect = pygame.Rect(x, y, fieldHeight, fieldWidth)
            pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

            self.fields.append((x, y, x + fieldHeight, y + fieldWidth))

            if not self.game.fields[offset].isSpecial:

                if self.game.fields[offset].owner != None:
                    off = fieldHeight / 5
                    rect = pygame.Rect(x + fieldHeight - off - fieldHeight / 5 + 2, y + fieldWidth - off, off, off)
                    pygame.draw.rect(self.surface, self.game.fields[offset].owner.color, rect)
                    pygame.draw.rect(self.surface, (0, 0, 0), rect, 2)
                # ulepszenia
                upgradeLevel = self.game.fields[offset].upgradeLevel
                if upgradeLevel > 0:
                    if upgradeLevel == 1:
                        width = fieldWidth / 3
                        height = width * 1.2
                        rect = pygame.Rect(x + (fieldHeight / 4), y + (fieldWidth / 4), height, width)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                        pass
                    elif upgradeLevel == 2:
                        width = fieldWidth / 3
                        height = width * 1.2
                        rect = pygame.Rect(x + (fieldHeight / 4), y + (fieldWidth / 4), height, width)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                        rect = pygame.Rect(x + (fieldHeight / 4) + (fieldWidth / 12), y + (fieldWidth / 4) + (fieldWidth / 12), height, width)
                        pygame.draw.rect(self.surface, (245, 240, 198), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
                    else:
                        width = fieldWidth / 2
                        height = width
                        rect = pygame.Rect(x + (fieldHeight / 4), y + (fieldWidth / 4), height, width)
                        pygame.draw.rect(self.surface, (198, 245, 236), rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

                # kolorowy pasek
                rect = pygame.Rect(x + (4 * fieldHeight / 5), y, fieldHeight / 5, fieldWidth)
                pygame.draw.rect(self.surface, self.game.fields[offset].color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

                # cena pola
                priceTag = None
                isBold = False
                if self.game.fields[offset].owner == None:
                    priceTag = self.game.fields[offset].getPurchaseCost()
                else:
                    priceTag = self.game.fields[offset].getFeeValue()
                    isBold = True
                priceTag = self.renderText(str(priceTag), bold=isBold)
                scaleFactor = (fieldHeight / 5) / priceTag.get_height()
                priceTag = pygame.transform.smoothscale(priceTag, (int(priceTag.get_width() * scaleFactor), int(fieldHeight / 5)))
                priceTag = pygame.transform.rotate(priceTag, 90)
                self.surface.blit(priceTag, (x + (4 * fieldHeight / 5), y + (fieldWidth / 2) - (priceTag.get_width() / 2)))

            # gracze
            px = x + (fieldWidth / 12)
            py = y + (fieldWidth / 12)
            for p in self.game.players:
                if p.position == offset and not p.bankrupt:
                    center = (px + fieldWidth / 10, py + fieldWidth / 10)
                    pygame.draw.circle(self.surface, p.color, center, fieldWidth / 8)
                    pygame.draw.circle(self.surface, (0, 0, 0), center, fieldWidth / 8, 1)
                    py += fieldWidth / 8 + fieldWidth / 12

            y += fieldWidth
            offset += 1

            # środek planszy

    def drawPlayerInfo(self, x, y, width):
        i = 0
        for p in self.game.players:
            pygame.draw.circle(self.surface, p.color, (x + 12, y + 12), 12)
            pygame.draw.circle(self.surface, (0, 0, 0), (x + 12, y + 12), 12, 2)

            txt = ""
            if p.isBot:
                txt += "(B)"
            txt += " ECTS"
            if p.jailed > 0 and not p.bankrupt:
                txt += " (#)"
            if self.game.activePlayer == i:
                txt += " ←"
            color = (0, 0, 0)
            if p.bankrupt:
                color = (128, 128, 128)
            text = self.renderText(str(p.money if not p.bankrupt else 0) + txt, bold=(self.game.activePlayer == i), size=24, color=color)
            self.surface.blit(text, (x + 32, y))

            y += 26
            i += 1

    def drawStatsScreen(self):
        img = pygame.image.load("res/table.png")

        # być może nie ma obrazka?
        if img:
            size = img.get_size()
            surfSize = self.surface.get_size()
            x = surfSize[0] / 2 - size[0] / 2
            y = surfSize[1] / 2 - size[1] / 2
            self.surface.blit(img, (x, y))
        
        text = self.renderText("Kliknij ESC, aby zakończyć program", size=24)
        x = surfSize[0] / 2 - text.get_width() / 2
        y = surfSize[1] - 36
        self.surface.blit(text, (x, y))
    
    def drawStartScreen(self):

        surfSize = self.surface.get_size()

        text = self.renderText("Monopoly UWR", size=72)
        x = surfSize[0] / 2 - text.get_width() / 2
        y = surfSize[1] / 3
        self.surface.blit(text, (x, y))

        y += 90
        text = self.renderText("Wciśnij 0-4 aby wybrać liczbę \"prawdziwych\" graczy", size=32)
        x = surfSize[0] / 2 - text.get_width() / 2
        self.surface.blit(text, (x, y))

        y += 36
        text = self.renderText("Reszta graczy będzie botami", size=32)
        x = surfSize[0] / 2 - text.get_width() / 2
        self.surface.blit(text, (x, y))

    def layoutButtons(self):
        if self.buttons == None or len(self.buttons) == 0:
            return

        self.buttonLayout = [None] * len(self.buttons)
        w = self.surface.get_width() # szerokość okna
        h = self.surface.get_height() # wysokość okna
        boardSize = min(w, h) - (min(w, h) / 8) # długość boku planszy
        fieldWidth = (boardSize / 11) # "szerokość" pola
        cornerSize = fieldWidth * 1.5 # rozmiar pola narożnego
        marginHorizontal = (w - boardSize) / 2 # margines poziomy

        buttonSize = ((boardSize - (2 * cornerSize) - 20) - (10 * (len(self.buttons) - 1))) / len(self.buttons)
        x = marginHorizontal + cornerSize + 10
        y = boardSize - cornerSize

        for i in self.buttons:
            self.buttonLayout[i] = (x, y, x + buttonSize, y + 40)
            x += buttonSize
            x += 10

    def setButtons(self, buttons):
        self.buttons = buttons
        self.layoutButtons()

    def rollDice(self):
        self.drawDice = self.game.inputDice()

    def endGame(self):
        self.game.game_over()
        self.state = self.POSTGAME

    def runButtons(self):
        for i in range(len(self.buttonLayout)):
            button = self.buttons[i]
            if self.detectClick(pygame.mouse.get_pos(), self.buttonLayout[i]):
                if callable(button[1]):
                    button[1]()
                else:
                    self.game.inputDecision(button[1])