from GameState import State
from collections import Counter

class BaseBot:
    def __init__(self):
        pass

    def doMove(self, gameState):
        raise Exception('Abstract Class', 'please implement this method in child class')
        # does move

    def cardsINeed(self, gameState):
        flippedCards = gameState.flippedCards
        cardsINeed = []
        for card in flippedCards:
            if(self.isCardINeed(card, gameState)):
                cardsINeed.append(card)
        return cardsINeed

    def isCardINeed(self, card, gameState):
        myCards = gameState.getCurrentPlayerCards()
        for myCard in myCards:
            if myCard.number == card.number:
                return False
        return True

    def cardsMyOpponentNeeds(self, gameState):
        flippedCards = gameState.flippedCards
        cardsMyOpponentNeeds = []
        for card in flippedCards:
            if(self.isCardMyOpponentNeeds(card, gameState)):
                cardsMyOpponentNeeds.append(card)
        return cardsMyOpponentNeeds

    def isCardMyOpponentNeeds(self, card, gameState):
        myCards = gameState.getOtherPlayerCards()
        for myCard in myCards:
            if myCard.number == card.number:
                return False
        return True

    def cardsWinMeFirstPick(self, gameState):
        flippedCards = gameState.flippedCards
        if(gameState.wasAPairDraw == True):
            if(gameState.currentState == State.FIRSTPICK):
                return []
            else:
                return flippedCards
        else:
            highestCard = max(gameState.flippedCards, key=lambda c: c.number)
            if(gameState.currentState == State.FIRSTPICK):
                return [highestCard]
            elif((gameState.p1PickVal is None or highestCard.number > gameState.p1PickVal) and
                (gameState.p2PickVal is None or highestCard.number > gameState.p2PickVal)):
                return [highestCard]
        return []

    def howCloseIsMyOpp(self, gameState):
        cards = gameState.getOtherPlayerCards()
        numbers = [card.number for card in cards]
        return len(set(numbers))

    def howCloseAmI(self, gameState):
        cards = gameState.getCurrentPlayerCards()
        numbers = [card.number for card in cards]
        return len(set(numbers))

    def IHaveFourOfAKind(self, gameState):
        cards = gameState.getCurrentPlayerCards()
        return self.hasFourOfAKind(cards)

    def OppHasFourOfAKind(self, gameState):
        cards = gameState.getOtherPlayerCards()
        return self.hasFourOfAKind(cards)

    def hasFourOfAKind(self, cards):
        numbers = [card.number for card in cards]
        most_common = Counter(numbers).most_common(1)
        return len(most_common) > 0 and most_common[0][1] == 4


    def printMyCards(self, gameState):
        myCards = gameState.getCurrentPlayerCards()
        numbers = [str(card.number) for card in myCards]
        print(F"my cards: {','.join(numbers)}")
