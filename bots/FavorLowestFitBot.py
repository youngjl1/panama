from bots.BaseBot import BaseBot
import random

class FavorLowestFitBot(BaseBot):

    def doMove(self, gameState):
        flippedCards = gameState.flippedCards
        lowestFitIndex = -1
        lowestFitCardVal = -1
        highestIndex = -1
        highestCardVal = -1
        for i in range(len(flippedCards)):
            if(flippedCards[i].number > highestCardVal):
                highestIndex = i
                highestCardVal = flippedCards[i].number

            if(self.isCardINeed(flippedCards[i], gameState)):
                if(flippedCards[i].number > lowestFitCardVal):
                    lowestFitIndex = i
                    lowestFitCardVal = flippedCards[i].number
        if(lowestFitIndex != -1):
            gameState.pickCardByIndex(lowestFitIndex)
        else:
            gameState.pickCardByIndex(highestIndex)
