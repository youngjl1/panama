from bots.BaseBot import BaseBot
import random

class DumboBot(BaseBot):

    def doMove(self, gameState):
        flippedCards = gameState.flippedCards
        for i in range(len(flippedCards)):
            if(self.isCardINeed(flippedCards[i], gameState)):
                gameState.pickCardByIndex(i)
                return

        pick = random.randint(0, len(flippedCards)-1)
        gameState.pickCardByIndex(pick)
