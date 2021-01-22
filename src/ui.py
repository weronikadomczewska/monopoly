import pygame
from game import Game
import time

class UI:

    def __init__(self, game):
        self.game = game
        self.closed = False
        self.needRedraw = True
        self.clicked = False
        self.drawDice = False
        self.fields = []

        pygame.display.init()
        info = pygame.display.Info()
        pygame.display.set_caption("Monopoly UWR")
        # self.surface = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        self.surface = pygame.display.set_mode((info.current_w - 300, info.current_h - 150), pygame.RESIZABLE)

        pygame.font.init()
        self.fontBold = pygame.font.SysFont("Courier", 32, True)
        self.font = pygame.font.SysFont("Courier", 32, False)
        self.timer = time.time()
        
        # wczytanie obrazków
        self.images = {}
        for f in self.game.fields:
            if f.isSpecial:
                if f.imagePath not in self.images:
                    self.images[f.imagePath] = pygame.image.load(f.imagePath)
        
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

        # przetworzenie zdarzeń okna gry
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.closed = True

            if event.type == pygame.VIDEORESIZE:
                self.needRedraw = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = True

        # obsługa stanów gry
        if self.game.state == self.game.WAITINGFORDICE:
            if self.clicked == True:
                self.drawDice = self.game.inputDice()
                self.needRedraw = True

        elif self.game.state == self.game.WAITINGFORDECISION:
            if self.clicked == True:
                self.game.inputDecision("Yes")
                self.needRedraw = True

        elif self.game.state == self.game.WAITINGFORPURCHASE:
            if self.clicked == True:
                self.game.inputDecision("Buy")
                self.needRedraw = True

        elif self.game.state == self.game.WAITINGFORREPURCHASE:
            if self.clicked == True:
                self.game.inputDecision("Repurchase")
                self.needRedraw = True

        elif self.game.state == self.game.WAITINGFORUPGRADE:
            if self.clicked == True:
                self.game.inputDecision("Upgrade")
                self.needRedraw = True

        elif self.game.state == self.game.WAITINGFORJAIL:
            if self.clicked == True:
                self.game.inputDecision("Bribe")
                self.needRedraw = True

        elif self.game.state == self.game.WAITINGFORTRAM:
            if self.clicked == True:
                f = self.getField(pygame.mouse.get_pos())
                if f != -1:
                    self.game.tram(f)
                else:
                    pass
                self.needRedraw = True


        # leniwe rysowanie interfejsu - tylko wtedy gdy jest potrzeba
        if self.needRedraw:
            self.surface.fill((255, 255, 255)) # czyszczenie ekranu
            self.drawBoard()
            self.drawPlayerInfo()
            self.needRedraw = False
            pygame.display.update() # pokazanie narysowanego interfejsu
        
        # czyszczenie
        self.clicked = False

    def renderText(self, text, bold=True):
        return self.fontBold.render(text, True, (0, 0, 0)) if bold else self.font.render(text, True, (0, 0, 0))

    # tymczasowa (bardzo brzydka) implementacja rysowania planszy
    # TODO(Karol M.): napisać ten kod porządnie!
    def drawBoard(self):

        self.fields = []

        w = self.surface.get_width() # szerokość okna
        h = self.surface.get_height() # wysokość okna
        boardSize = min(w, h) - (min(w, h) / 10) # długość boku planszy
        marginHorizontal = (w - boardSize) / 2 # margines poziomy
        marginVertical = (h - boardSize) / 2 # margines pionowy
        fieldWidth = (boardSize / 11) # "szerokość" pola
        cornerSize = fieldWidth * 1.5 # rozmiar pola narożnego
        fieldHeight = cornerSize # "wysokość" pola, taka sama jak pole narożne
        borderWidth = 2 # szerokość obrysu pól

        # rysowanie kostek po rzucie
        if self.drawDice:
            firstImage = self.images[f"dice{self.drawDice[0]}"]
            secondImage = self.images[f"dice{self.drawDice[1]}"]

            diceSize = fieldWidth / 2
            firstImage = pygame.transform.smoothscale(firstImage, (int(diceSize), int(diceSize)))
            secondImage = pygame.transform.smoothscale(secondImage, (int(diceSize), int(diceSize)))

            x = marginHorizontal + (boardSize / 2) - diceSize
            y = marginVertical + boardSize - cornerSize - diceSize - (fieldHeight / 2)

            self.surface.blit(firstImage, (x, y))
            x += diceSize
            self.surface.blit(secondImage, (x, y))

            if self.drawDice[0] == self.drawDice[1]:
                print("dublet!")
                x -= diceSize + boardSize / 4
                double = self.renderText("Dublet! Rzucasz jeszcze raz!")
                scaleFactor = (boardSize / 2) / double.get_width()
                double = pygame.transform.smoothscale(double, (int(double.get_width() * scaleFactor), int(double.get_height())))
                y -= double.get_height() * 1.5
                self.surface.blit(double, (x, y))

            self.drawDice = False

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
            if p.position == offset:
                rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                pygame.draw.rect(self.surface, p.color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)

                if counter == 0:
                    px += (cornerSize / 4.2) * 3
                elif counter == 1:
                    py += (cornerSize / 4.2) * 3
                elif counter == 2:
                    px -= (cornerSize / 4.2) * 3

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
                    pygame.draw.circle(self.surface, self.game.fields[offset].owner.color, (x + (fieldWidth / 6), y + (4 * fieldHeight / 5) - fieldWidth / 7), fieldWidth / 8)
                    pygame.draw.circle(self.surface, (0, 0, 0), (x + (fieldWidth / 6), y + (4 * fieldHeight / 5) - fieldWidth / 7), fieldWidth / 8, borderWidth)
                
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
                if self.game.fields[offset].owner == None:
                    priceTag = self.game.fields[offset].getPurchaseCost()
                else:
                    priceTag = self.game.fields[offset].getFeeValue()
                priceTag = self.renderText(str(priceTag))
                scaleFactor = (fieldHeight / 5) / priceTag.get_height()
                priceTag = pygame.transform.smoothscale(priceTag, (int(priceTag.get_width() * scaleFactor), int(fieldHeight / 5)))
                self.surface.blit(priceTag, (x + (fieldWidth / 2) - (priceTag.get_width() / 2), y + (4 * fieldHeight / 5)))

            # gracze
            px = x + (fieldWidth / 12) 
            py = y + (fieldWidth / 12) 
            for p in self.game.players:
                if p.position == offset:
                    rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                    pygame.draw.rect(self.surface, p.color, rect)
                    pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
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
            if p.position == offset:
                rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                pygame.draw.rect(self.surface, p.color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)

                if counter == 0:
                    px += (cornerSize / 4.2) * 3
                elif counter == 1:
                    py += (cornerSize / 4.2) * 3
                elif counter == 2:
                    px -= (cornerSize / 4.2) * 3

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
                    pygame.draw.circle(self.surface, self.game.fields[offset].owner.color, (x + (fieldHeight / 5) + (fieldHeight / 10), y + fieldWidth / 6), fieldWidth / 8)
                    pygame.draw.circle(self.surface, (0, 0, 0), (x + (fieldHeight / 5) + (fieldHeight / 10), y + fieldWidth / 6), fieldWidth / 8, borderWidth)

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
                if self.game.fields[offset].owner == None:
                    priceTag = self.game.fields[offset].getPurchaseCost()
                else:
                    priceTag = self.game.fields[offset].getFeeValue()
                priceTag = self.renderText(str(priceTag))
                scaleFactor = (fieldHeight / 5) / priceTag.get_height()
                priceTag = pygame.transform.smoothscale(priceTag, (int(priceTag.get_width() * scaleFactor), int(fieldHeight / 5)))
                priceTag = pygame.transform.rotate(priceTag, 270)
                self.surface.blit(priceTag, (x, y + (fieldWidth / 2) - (priceTag.get_width() / 2)))

            # gracze
            px = x + fieldHeight - (fieldHeight / 6)
            py = y + (fieldWidth / 12) 
            for p in self.game.players:
                if p.position == offset:
                    rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                    pygame.draw.rect(self.surface, p.color, rect)
                    pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
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
            if p.position == offset:
                rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                pygame.draw.rect(self.surface, p.color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)

                if counter == 0:
                    px += (cornerSize / 4.2) * 3
                elif counter == 1:
                    py += (cornerSize / 4.2) * 3
                elif counter == 2:
                    px -= (cornerSize / 4.2) * 3

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
                    pygame.draw.circle(self.surface, self.game.fields[offset].owner.color, (x + (4 * fieldWidth / 5) + (fieldWidth / 20), y + (fieldHeight / 5) + (fieldHeight / 10)), fieldWidth / 8)
                    pygame.draw.circle(self.surface, (0, 0, 0), (x + (4 * fieldWidth / 5) + (fieldWidth / 20), y + (fieldHeight / 5) + (fieldHeight / 10)), fieldWidth / 8, 2)
                
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
                if self.game.fields[offset].owner == None:
                    priceTag = self.game.fields[offset].getPurchaseCost()
                else:
                    priceTag = self.game.fields[offset].getFeeValue()
                priceTag = self.renderText(str(priceTag))
                scaleFactor = (fieldHeight / 5) / priceTag.get_height()
                priceTag = pygame.transform.smoothscale(priceTag, (int(priceTag.get_width() * scaleFactor), int(fieldHeight / 5)))
                self.surface.blit(priceTag, (x + (fieldWidth / 2) - (priceTag.get_width() / 2), y))

            # gracze
            px = x + (fieldWidth / 12)
            py = y + fieldHeight - (fieldWidth / 4) 
            for p in self.game.players:
                if p.position == offset:
                    rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                    pygame.draw.rect(self.surface, p.color, rect)
                    pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
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
            if p.position == offset:
                rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                pygame.draw.rect(self.surface, p.color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)

                if counter == 0:
                    px += (cornerSize / 4.2) * 3
                elif counter == 1:
                    py += (cornerSize / 4.2) * 3
                elif counter == 2:
                    px -= (cornerSize / 4.2) * 3

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
                    pygame.draw.circle(self.surface, self.game.fields[offset].owner.color, (x + (4 * fieldHeight / 5) - (fieldHeight / 10), y + fieldWidth - (fieldWidth / 6)), fieldWidth / 8)
                    pygame.draw.circle(self.surface, (0, 0, 0), (x + (4 * fieldHeight / 5) - (fieldHeight / 10), y + fieldWidth - (fieldWidth / 6)), fieldWidth / 8, 2)

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
                if self.game.fields[offset].owner == None:
                    priceTag = self.game.fields[offset].getPurchaseCost()
                else:
                    priceTag = self.game.fields[offset].getFeeValue()
                priceTag = self.renderText(str(priceTag))
                scaleFactor = (fieldHeight / 5) / priceTag.get_height()
                priceTag = pygame.transform.smoothscale(priceTag, (int(priceTag.get_width() * scaleFactor), int(fieldHeight / 5)))
                priceTag = pygame.transform.rotate(priceTag, 90)
                self.surface.blit(priceTag, (x + (4 * fieldHeight / 5), y + (fieldWidth / 2) - (priceTag.get_width() / 2)))

            # gracze
            px = x + (fieldWidth / 12)
            py = y + (fieldWidth / 12)
            for p in self.game.players:
                if p.position == offset:
                    rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                    pygame.draw.rect(self.surface, p.color, rect)
                    pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
                    py += fieldWidth / 8 + fieldWidth / 12

            y += fieldWidth
            offset += 1

    def drawPlayerInfo(self):
        x = 10
        y = 10
        i = 0
        for p in self.game.players:
            pygame.draw.circle(self.surface, p.color, (x + 8, y + 8), 8)
            pygame.draw.circle(self.surface, (0, 0, 0), (x + 8, y + 8), 8, 2)

            text = self.renderText(str(p.money) + " ECTS", (self.game.activePlayer == i))
            scaleFactor = 16 / text.get_height()
            text = pygame.transform.smoothscale(text, (int(text.get_width() * scaleFactor), 16))
            self.surface.blit(text, (x + 20, y))

            y += 20
            i += 1