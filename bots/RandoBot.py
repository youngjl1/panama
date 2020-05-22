from bots.BaseBot import BaseBot
import random

class RandoBot(BaseBot):
    def doMove(self, gameState):
        flippedCards = gameState.flippedCards
        pick = random.randint(0, len(flippedCards)-1)
        gameState.pickCardByIndex(pick)
