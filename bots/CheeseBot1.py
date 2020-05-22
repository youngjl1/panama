from bots.BaseBot import BaseBot
import random

class CheeseBot1(BaseBot):

    def doMove(self, gameState):
        cardsINeed = self.cardsINeed(gameState)
        cardsMyOpponentNeeds = self.cardsMyOpponentNeeds(gameState)
        cardsWinMeFirstPick = self.cardsWinMeFirstPick(gameState)
        howCloseIsMyOpp = self.howCloseIsMyOpp(gameState)
        howCloseAmI = self.howCloseAmI(gameState)

        if(self.IHaveFourOfAKind(gameState) == False):
            if(len(cardsMyOpponentNeeds) > 0):
                gameState.pickCard(cardsMyOpponentNeeds[0])
                return

        if(len(cardsINeed) > 0):
            gameState.pickCard(cardsINeed[0])
        elif(len(cardsWinMeFirstPick) > 0):
            gameState.pickCard(cardsWinMeFirstPick[0])
        else:
            flippedCards = gameState.flippedCards
            pick = random.randint(0, len(flippedCards)-1)
            gameState.pickCardByIndex(pick)
