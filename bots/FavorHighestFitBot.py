from bots.BaseBot import BaseBot
import random

class FavorHighestFitBot(BaseBot):

    def doMove(self, gameState):
        flippedCards = gameState.flippedCards
        highestFitIndex = -1
        highestFitCardVal = -1
        highestIndex = -1
        highestCardVal = -1
        for i in range(len(flippedCards)):
            if(flippedCards[i].number > highestCardVal):
                highestIndex = i
                highestCardVal = flippedCards[i].number

            if(self.isCardINeed(flippedCards[i], gameState)):
                if(flippedCards[i].number > highestFitCardVal):
                    highestFitIndex = i
                    highestFitCardVal = flippedCards[i].number
        if(highestFitIndex != -1):
            gameState.pickCardByIndex(highestFitIndex)
        else:
            gameState.pickCardByIndex(highestIndex)
