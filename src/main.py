from game import Game
from player import Player
from ui import UI

ui = UI()
while not ui.closed:
    ui.gameTick()