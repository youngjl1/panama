from bots.BaseBot import BaseBot
import random

class NotAnIdiotBot2(BaseBot):

    def doMove(self, gameState):
        cardsINeed = self.cardsINeed(gameState)
        cardsMyOpponentNeeds = self.cardsMyOpponentNeeds(gameState)

        if(len(cardsMyOpponentNeeds) > 0):
            gameState.pickCard(cardsMyOpponentNeeds[0])
        elif(len(cardsINeed) > 0):
            gameState.pickCard(cardsINeed[0])
        else:
            flippedCards = gameState.flippedCards
            pick = random.randint(0, len(flippedCards)-1)
            gameState.pickCardByIndex(pick)
