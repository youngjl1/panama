from GameState import GameState, Player

def doGame(bot1, bot2, verboseLog):
    gameState = GameState(verboseLog)

    while(gameState.isGameOver == False):
        currentPlayer = gameState.getCurrentPicker()
        if(currentPlayer == Player.PLAYER1):
            bot1.doMove(gameState)
        else:
            bot2.doMove(gameState)
    if(verboseLog):
        print(F"Game is over. The outcome is:  {gameState.getGameState()}")
    return gameState.getGameState()
