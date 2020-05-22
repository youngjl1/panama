from GameSim import doGame
from GameState import State
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
from bots.HeuristicBot1 import HeuristicBot1
from bots.HeuristicBot2 import HeuristicBot2
from bots.HeuristicBot3 import HeuristicBot3
from bots.HeuristicBot4 import HeuristicBot4
import time
import sys
import curses

bot1 = HeuristicBot4()
bot2 = HeuristicBot3()

outcome_map = {
    State.PLAYER1WINS: type(bot1).__name__,
    State.PLAYER2WINS: type(bot2).__name__,
    State.DRAWGAME: "Draw"
}

if len(sys.argv) > 1 and sys.argv[1] == "verbose":
    doGame(bot1, bot2, True)
    exit()

outcomes = {
    State.PLAYER1WINS: 0,
    State.PLAYER2WINS: 0,
    State.DRAWGAME: 0
}


def proper_round(num, dec=0):
    num = str(num)[:str(num).index('.')+dec+2]
    if num[-1]>='5':
        return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
    return float(num[:-1])

BAR_SIZE = 60
def getNormalizedMap(outcomes):

    sum = outcomes[State.DRAWGAME] + outcomes[State.PLAYER1WINS] + outcomes[State.PLAYER2WINS]
    decimal_map = {
        State.PLAYER1WINS: int(outcomes[State.PLAYER1WINS] * BAR_SIZE / sum),
        State.PLAYER2WINS: int(outcomes[State.PLAYER2WINS] * BAR_SIZE / sum),
        State.DRAWGAME: int(outcomes[State.DRAWGAME] * BAR_SIZE / sum)
    }
    return decimal_map

def animated(window):
    window.move(5,0)
    # sleep_interval = 1.
    sleep_interval = .00001
    speed_up_cycles = 5
    cycles = 1000
    for i in range(1000):
        outcome = doGame(bot1, bot2, False)
        outcomes[outcome] += 1
        if(i < 200 or i % 25 == 0 or i == cycles-1):
            normalized_outcomes = getNormalizedMap(outcomes)
            window.addstr(1, 2,F"{outcome_map[State.DRAWGAME]}:")
            window.addstr(2, 2,F"{outcome_map[State.PLAYER1WINS]}:")
            window.addstr(3, 2,F"{outcome_map[State.PLAYER2WINS]}:")
            window.addstr(1, 22,F"{outcomes[State.DRAWGAME]}")
            window.addstr(2, 22,F"{outcomes[State.PLAYER1WINS]}")
            window.addstr(3, 22,F"{outcomes[State.PLAYER2WINS]}")
            window.addstr(1, 26,F"{normalized_outcomes[State.DRAWGAME] * '#'}{(BAR_SIZE-normalized_outcomes[State.DRAWGAME]) * ' '}")
            window.addstr(2, 26,F"{normalized_outcomes[State.PLAYER1WINS] * '#'}{(BAR_SIZE-normalized_outcomes[State.DRAWGAME]) * ' '}")
            window.addstr(3, 26,F"{normalized_outcomes[State.PLAYER2WINS] * '#'}{(BAR_SIZE-normalized_outcomes[State.DRAWGAME]) * ' '}")
            window.move(5,0)
            window.refresh()
        if(i >= 200):
            sleep_interval = 0
        elif(i % speed_up_cycles == 0 and i != 0):
            speed_up_cycles = int(speed_up_cycles * 1.5)
            sleep_interval /= 1.5
            # window.addstr(7, 0,F"Speed: {sleep_interval}")
        time.sleep(sleep_interval)


    if(outcomes[State.PLAYER1WINS] == outcomes[State.PLAYER2WINS]):
        window.addstr(5, 0,F"No way! It's a draw!")
    elif(outcomes[State.PLAYER1WINS] > outcomes[State.PLAYER2WINS]):
        win_rate = (outcomes[State.PLAYER1WINS] + (.5 * outcomes[State.DRAWGAME])) / cycles
        window.addstr(5, 0,F"{outcome_map[State.PLAYER1WINS]} wins! Win rate: {win_rate}. Congrats!")
    else:
        win_rate = (outcomes[State.PLAYER2WINS] + (.5 * outcomes[State.DRAWGAME])) / cycles
        window.addstr(5, 0,F"{outcome_map[State.PLAYER2WINS]} wins! Win rate: {win_rate}. Congrats!")
    window.addstr(7, 0,F"<press any key to exit>")
    window.getkey()

def runSimple():
    cycles = 1000
    for i in range(1000):
        outcome = doGame(bot1, bot2, False)
        outcomes[outcome] += 1

    print(F"{outcome_map[State.DRAWGAME]}:\t\t\t{outcomes[State.DRAWGAME]}")
    print(F"{outcome_map[State.PLAYER1WINS]}:\t{outcomes[State.PLAYER1WINS]}")
    print(F"{outcome_map[State.PLAYER2WINS]}:\t{outcomes[State.PLAYER2WINS]}")

    if(outcomes[State.PLAYER1WINS] == outcomes[State.PLAYER2WINS]):
        print(F"No way! It's a draw!")
    elif(outcomes[State.PLAYER1WINS] > outcomes[State.PLAYER2WINS]):
        win_rate = (outcomes[State.PLAYER1WINS] + (.5 * outcomes[State.DRAWGAME])) / cycles
        print(F"{outcome_map[State.PLAYER1WINS]} wins! Win rate: {win_rate}. Congrats!")
    else:
        win_rate = (outcomes[State.PLAYER2WINS] + (.5 * outcomes[State.DRAWGAME])) / cycles
        print(F"{outcome_map[State.PLAYER2WINS]} wins! Win rate: {win_rate}. Congrats!")


if len(sys.argv) > 1 and sys.argv[1] == "simple":
    runSimple()
else:
    curses.wrapper(animated)
