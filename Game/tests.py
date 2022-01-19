from cards import *
from game import *

nPlayer = 4
player = Player('Player One', board=Board(nPlayers=nPlayer))

def testSelectFromHand(n=1):

    phrase = 'Please Choose one card to discard!'
    player.selectCards(n, phrase)

def testSelectFromBoard():
    player.selectCardPile()
    pass

def testSelectActionCard():
    player.hand.append(village)
    player.actions += 1
    player.selectActionCard()

def testSelectBuyCard():
    player.selectBuyCard()


if __name__ == '__main__':
    #testSelectFromHand()
    #testSelectFromHand(n=4)
    #testSelectFromBoard()
    #testSelectActionCard()
    testSelectBuyCard()
    pass