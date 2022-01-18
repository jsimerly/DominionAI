from cards import *
from game import *

def testSelectFromHand(n=1):
    nPlayer = 4
    player = Player('Player One', board=Board(nPlayers=nPlayer))

    phrase = 'Please Choose one card to discard!'
    player.selectCardsFromHand(n, phrase)

def testSelectFromBoard():
    nPlayer = 4
    player = Player('Player One', board=Board(nPlayers=nPlayer))

    phrase = 'Please Choose one card to discard!'
    player.selectCardPile()
    pass

def testSelectActionCard():
    nPlayer = 4
    player = Player('Player One', board=Board(nPlayers=nPlayer))
    player.hand.append(village)
    player.actions += 1
    player.selectActionCard()

if __name__ == '__main__':
    #testSelectFromHand()
    #testSelectFromHand(n=4)
    #testSelectFromBoard()
    #testSelectActionCard()
    pass