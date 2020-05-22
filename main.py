from GameSim import doGame
from bots.DumboBot import DumboBot
from bots.RandoBot import RandoBot
from bots.FavorLowestFitBot import FavorLowestFitBot
from bots.FavorHighestFitBot import FavorHighestFitBot
from bots.NotAnIdiotBot1 import NotAnIdiotBot1
from bots.NotAnIdiotBot2 import NotAnIdiotBot2
from bots.NotAnIdiotBot3 import NotAnIdiotBot3
from bots.NotAnIdiotBot4 import NotAnIdiotBot4
from bots.NotAnIdiotBot5 import NotAnIdiotBot5
from bots.CheeseBot1 import CheeseBot1
from bots.CheeseBot2 import CheeseBot2



print("hi")
bot1 = NotAnIdiotBot4()
bot2 = NotAnIdiotBot5()

# doGame( bot1, bot2, True)
# exit()

outcomes = {}
for i in range(10000):
    outcome = doGame(bot1, bot2, False)
    if outcome in outcomes:
        outcomes[outcome] += 1
    else:
        outcomes[outcome] = 1


items = outcomes.items()
items = sorted(items, key=lambda c: c[0].name)
for outcome in items:
    print (F"{outcome[0]}: {outcome[1]}")
