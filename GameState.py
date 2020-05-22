from enum import Enum
import random

class Player(Enum):
    PLAYER1 = 1
    PLAYER2 = 2

class State(Enum):
    PLAYER1WINS = 1
    PLAYER2WINS = 2
    DRAWGAME = 3
    FIRSTPICK = 4
    SECONDPICK = 5

class Suit(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4
suits = [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]

class Card:
    suit = None
    number = None
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
    def __repr__(self):
        return F"{self.number} of {self.suit.name}"

class GameState:
    drawPile = []
    discardPile = []
    p1Cards = []
    p2Cards = []
    flippedCards = []
    firstPicker = None # either player 1 or 2
    currentState = None
    wasAPairDraw = None
    p1PickVal = None
    p2PickVal = None
    isGameOver = False
    verboseLog = False

    def __init__(self, verboseLog=False):
        self.drawPile = []
        self.discardPile = []
        self.p1Cards = []
        self.p2Cards = []
        self.flippedCards = []
        self.firstPicker = None # either player 1 or 2
        self.currentState = None
        self.wasAPairDraw = None
        self.p1PickVal = None
        self.p2PickVal = None
        self.isGameOver = False
        self.verboseLog = verboseLog

        self.drawPile = GameState.generateDeck()
        self.drawPile = GameState.shuffleDeck(self.drawPile)
        for i in range(3):
            self.flippedCards.append(self.drawPile.pop(0))
        if self.verboseLog:
            print("The following cards were flipped")
            [print(card) for card in self.flippedCards]
        self.currentState = State.FIRSTPICK
        if random.randint(1, 2) == 1:
            self.firstPicker = Player.PLAYER1
        else:
            self.firstPicker = Player.PLAYER2
        self._processPairFlipped()

    def getCurrentPlayerCards(self):
        currentPicker = self.getCurrentPicker()
        if(currentPicker == Player.PLAYER1):
            return self.p1Cards
        else:
            return self.p2Cards

    def getOtherPlayerCards(self):
        currentPicker = self.getCurrentPicker()
        if(currentPicker == Player.PLAYER1):
            return self.p2Cards
        else:
            return self.p1Cards

    def getCurrentPicker(self):
        currentPicker = Player.PLAYER1
        if((self.currentState == State.FIRSTPICK and self.firstPicker == Player.PLAYER2) or
            (self.currentState == State.SECONDPICK and self.firstPicker == Player.PLAYER1) ):
            currentPicker = Player.PLAYER2
        return currentPicker

    def pickCard(self, card):
        foundCard = False
        for flippedCard in self.flippedCards:
            if(card == flippedCard):
                if(foundCard):
                    raise Exception('Already found matching card. Are there duplicate cards?')
                self._pickCard(card)
                foundCard = True
        if(foundCard == False):
            raise Exception('Did not pick a valid card')

    def pickCardByIndex(self, index):
        assert index >= 0 and index < len(self.flippedCards)
        card = self.flippedCards[index]
        self._pickCard(card)

    def _pickCard(self, card):
        assert self.isGameOver == False
        self.flippedCards.remove(card)

        currentPicker = self.getCurrentPicker()
        if self.verboseLog:
            print(F"{currentPicker.name} has picked {card}")
        if(currentPicker == Player.PLAYER1):
            self.p1Cards.append(card)
            self.p1Cards.sort(key=lambda c: c.number)
            self.p1PickVal = card.number
            numbers = [str(card.number) for card in self.p1Cards]
            if self.verboseLog:
                print(F"my cards: {','.join(numbers)}")
        else:
            self.p2Cards.append(card)
            self.p2Cards.sort(key=lambda c: c.number)
            self.p2PickVal = card.number
            numbers = [str(card.number) for card in self.p2Cards]
            if self.verboseLog:
                print(F"my cards: {','.join(numbers)}")


        if(self.calcIsGameOver()):
            self.isGameOver = True
            return
        if(self.currentState == State.FIRSTPICK):
            self.currentState = State.SECONDPICK
        else:
            self.currentState = State.FIRSTPICK
            # set current picker
            if(self.wasAPairDraw):
                # do nothing because firstPicker doesn't change
                pass
            else:
                assert self.p1PickVal != self.p2PickVal
                if(self.p1PickVal > self.p2PickVal):
                    self.firstPicker = Player.PLAYER1
                else:
                    self.firstPicker = Player.PLAYER2

            # set flipped cards
            self.discardPile += self.flippedCards
            self.flippedCards = []
            if(len(self.drawPile) < 3):
                self.discardPile = GameState.shuffleDeck(self.discardPile)
                self.drawPile += self.discardPile
                self.discardPile = []

            for i in range(3):
                if(len(self.drawPile) > 0):
                    self.flippedCards.append(self.drawPile.pop(0))
            if self.verboseLog:
                print("The following cards were flipped")
                [print(card) for card in self.flippedCards]

            self._processPairFlipped()

            self.p1PickVal = None
            self.p2PickVal = None




    def getGameState(self):
        return self.currentState

    def calcIsGameOver(self):
        if(self.currentState in [State.PLAYER1WINS, State.PLAYER2WINS, State.DRAWGAME]):
            return True

        player1MadeIt = self._playerHasAllNumbers(self.p1Cards)
        player2MadeIt = self._playerHasAllNumbers(self.p2Cards)
        if(player1MadeIt and player2MadeIt):
            self.currentState = State.DRAWGAME
            return True
        if(player1MadeIt and self.currentState == State.SECONDPICK):
            self.currentState = State.PLAYER1WINS
            return True
        if(player2MadeIt and self.currentState == State.SECONDPICK):
            self.currentState = State.PLAYER2WINS
            return True
        player1Got4 = self._playerHasFourOfAKind(self.p1Cards)
        player2Got4 = self._playerHasFourOfAKind(self.p2Cards)
        if(player1Got4 and player2Got4):
            self.currentState = State.DRAWGAME
            return True
        if(len(self.flippedCards) + len(self.drawPile)  + len(self.discardPile) == 0):
            self.currentState = State.DRAWGAME
            return True
        return False

    def _playerHasFourOfAKind(self, cards):
        cardCount = 0
        currentCard = None
        for card in cards:
            if card.number == currentCard:
                cardCount += 1
            else:
                currentCard = card.number
                cardCount = 1
            if(cardCount == 4):
                return True
        return False

    def _playerHasAllNumbers(self, cards):
        lookingFor = 2
        for card in cards:
            if card.number == lookingFor:
                lookingFor += 1
                if lookingFor == 15:
                    return True
            elif card.number > lookingFor:
                return False
        return False



    def _processPairFlipped(self):
        if GameState._isAPairDraw(self.flippedCards):
            if(self.firstPicker == Player.PLAYER1):
                self.firstPicker = Player.PLAYER2
            else:
                self.firstPicker = Player.PLAYER1
            self.wasAPairDraw = True
        else:
            self.wasAPairDraw = False

    @staticmethod
    def _isAPairDraw(flippedCards):
        if(len(flippedCards) == 3):
            return (GameState._isAPair(flippedCards[0], flippedCards[1]) or
                GameState._isAPair(flippedCards[0], flippedCards[2]) or
                GameState._isAPair(flippedCards[1], flippedCards[2]))
        if(len(flippedCards) == 3):
            return GameState._isAPair(flippedCards[0], flippedCards[1])

        return False

    @staticmethod
    def _isAPair(card1, card2):
        return card1.number == card2.number

    @staticmethod
    def generateDeck():
        cards = []
        for suit in suits:
            for i in range(2,15):
                cards.append(Card(suit, i))
        return cards

    @staticmethod
    def shuffleDeck(deck):
        for i in range(1000):
            index1 = random.randint(0, len(deck)-1)
            index2 = random.randint(0, len(deck)-1)
            temp = deck[index1]
            deck[index1] = deck[index2]
            deck[index2] = temp

        return deck
