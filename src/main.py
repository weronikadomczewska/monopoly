from game import Game
from player import Player
from ui import UI

# kod testowy, tworzy graczy, grę i pokazuje interfejs
player1 = Player(color=(255, 0, 0))
player2 = Player(color=(0, 255, 0))
player3 = Player(color=(0, 0, 255))
player4 = Player(color=(255, 255, 0))

game = Game()
game.addPlayer(player1)
game.addPlayer(player2)
game.addPlayer(player3)
game.addPlayer(player4)

ui = UI(game)
while not ui.closed:
    ui.gameTick()