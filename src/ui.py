import pygame
from game import Game
import time

class UI:

    def __init__(self, game):
        self.game = game
        self.closed = False
        self.needRedraw = True

        pygame.display.init()
        info = pygame.display.Info()
        pygame.display.set_caption("Monopoly UWR")
        # self.surface = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        self.surface = pygame.display.set_mode((info.current_w - 300, info.current_h - 150), pygame.RESIZABLE)

        pygame.font.init()
        self.font = pygame.font.SysFont("Courier", 32, True)
        self.timer = time.time()
        
    def gameTick(self):

        if time.time() - self.timer >= 0.5:
            self.game.takeAction()
            self.timer = time.time()
            self.needRedraw = True

        # przetworzenie zdarzeń okna gry
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.closed = True

            if event.type == pygame.VIDEORESIZE:
                self.needRedraw = True

        # leniwe rysowanie interfejsu - tylko wtedy gdy jest potrzeba
        if self.needRedraw:
            self.surface.fill((255, 255, 255)) # czyszczenie ekranu
            self.drawBoard()
            self.needRedraw = False
            pygame.display.update() # pokazanie narysowanego interfejsu

    # tymczasowa (bardzo brzydka) implementacja rysowania planszy
    # TODO(Karol M.): napisać ten kod porządnie!
    def drawBoard(self):
        w = self.surface.get_width() # szerokość okna
        h = self.surface.get_height() # wysokość okna
        boardSize = min(w, h) - (min(w, h) / 10) # długość boku planszy
        marginHorizontal = (w - boardSize) / 2 # margines poziomy
        marginVertical = (h - boardSize) / 2 # margines pionowy
        fieldWidth = (boardSize / 11) # "szerokość" pola
        cornerSize = fieldWidth * 1.5 # rozmiar pola narożnego
        fieldHeight = cornerSize # "wysokość" pola, taka sama jak pole narożne
        borderWidth = 2 # szerokość obrysu pól

        x = marginHorizontal + boardSize - cornerSize
        y = marginVertical + boardSize - cornerSize

        rect = pygame.Rect(x, y, cornerSize, cornerSize)
        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
        offset = 0

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

        image = pygame.image.load(self.game.fields[0].imagePath)
        image = pygame.transform.smoothscale(image, (int(cornerSize / 1.5), int(cornerSize / 1.5)))
        self.surface.blit(image, (x + (cornerSize / 2) - int(cornerSize / 3), y + (cornerSize / 2) - int(cornerSize / 3)))

        x -= fieldWidth

        offset = 1

        for _ in range(8):
            rect = pygame.Rect(x, y, fieldWidth, fieldHeight)
            pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)
        
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

                # gracze
                px = x + (fieldWidth / 12) 
                py = y + (fieldWidth / 12) 
                for p in self.game.players:
                    if p.position == offset:
                        rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                        pygame.draw.rect(self.surface, p.color, rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
                        px += fieldWidth / 8 + fieldWidth / 12

                rect = pygame.Rect(x, y + (4 * fieldHeight / 5), fieldWidth, fieldHeight / 5)
                pygame.draw.rect(self.surface, self.game.fields[offset].color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

            x -= fieldWidth
            offset += 1

        x -= (fieldWidth / 2)

        rect = pygame.Rect(x, y, cornerSize, cornerSize)
        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

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

        image = pygame.image.load(self.game.fields[offset].imagePath)
        image = pygame.transform.smoothscale(image, (int(cornerSize / 1.5), int(cornerSize / 1.5)))
        self.surface.blit(image, (x + (cornerSize / 2) - int(cornerSize / 3), y + (cornerSize / 2) - int(cornerSize / 3)))

        offset += 1
        y -= fieldWidth

        for _ in range(8):
            rect = pygame.Rect(x, y, fieldHeight, fieldWidth)
            pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

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

                # gracze
                px = x + fieldHeight - (fieldHeight / 6)
                py = y + (fieldWidth / 12) 
                for p in self.game.players:
                    if p.position == offset:
                        rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                        pygame.draw.rect(self.surface, p.color, rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
                        py += fieldWidth / 8 + fieldWidth / 12

                rect = pygame.Rect(x, y, fieldHeight / 5, fieldWidth)
                pygame.draw.rect(self.surface, self.game.fields[offset].color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

            y -= fieldWidth
            offset += 1

        y -= (fieldWidth / 2)
        rect = pygame.Rect(x, y, cornerSize, cornerSize)
        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

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

        image = pygame.image.load(self.game.fields[offset].imagePath)
        image = pygame.transform.smoothscale(image, (int(cornerSize / 1.5), int(cornerSize / 1.5)))
        self.surface.blit(image, (x + (cornerSize / 2) - int(cornerSize / 3), y + (cornerSize / 2) - int(cornerSize / 3)))

        offset += 1
        x += cornerSize

        for _ in range(8):
            rect = pygame.Rect(x, y, fieldWidth, fieldHeight)
            pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

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

                # gracze
                px = x + (fieldWidth / 12)
                py = y + fieldHeight - (fieldWidth / 4) 
                for p in self.game.players:
                    if p.position == offset:
                        rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                        pygame.draw.rect(self.surface, p.color, rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
                        px += fieldWidth / 8 + fieldWidth / 12

                rect = pygame.Rect(x, y, fieldWidth, fieldHeight / 5)
                pygame.draw.rect(self.surface, self.game.fields[offset].color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

            x += fieldWidth
            offset += 1

        rect = pygame.Rect(x, y, cornerSize, cornerSize)
        pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

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

        image = pygame.image.load(self.game.fields[offset].imagePath)
        image = pygame.transform.smoothscale(image, (int(cornerSize / 1.5), int(cornerSize / 1.5)))
        self.surface.blit(image, (x + (cornerSize / 2) - int(cornerSize / 3), y + (cornerSize / 2) - int(cornerSize / 3)))

        offset += 1
        y += cornerSize

        for _ in range(8):
            rect = pygame.Rect(x, y, fieldHeight, fieldWidth)
            pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

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

                # gracze
                px = x + (fieldWidth / 12)
                py = y + (fieldWidth / 12)
                for p in self.game.players:
                    if p.position == offset:
                        rect = pygame.Rect(px, py, fieldWidth / 5, fieldWidth / 5)
                        pygame.draw.rect(self.surface, p.color, rect)
                        pygame.draw.rect(self.surface, (0, 0, 0), rect, 1)
                        py += fieldWidth / 8 + fieldWidth / 12

                rect = pygame.Rect(x + (4 * fieldHeight / 5), y, fieldHeight / 5, fieldWidth)
                pygame.draw.rect(self.surface, self.game.fields[offset].color, rect)
                pygame.draw.rect(self.surface, (0, 0, 0), rect, borderWidth)

            y += fieldWidth
            offset += 1
