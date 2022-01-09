
import random
from cards import *

class Deck():
    def __init__(self):
        self.cards = [copper, copper, copper, copper, copper, copper, copper,
                    estate, estate, estate]
        self.discard = []
        self.shuffle()
        

    def getTopCard(self, nCards=1):
        topCards = []

        if len(self.cards) >= nCards:
            for i in range(nCards):
                topCards.append(self.cards[i])

            return topCards
        elif nCards >= len(self.cards) + len(self.discard):
            if self.discard == []:
                return self.cards
            else:
                self.cards.extend(self.discard)
                self.discard = []
                self.shuffle()
                
                return self.cards
        else:
            self.cards.extend(self.discard)
            self.discard = []
            self.shuffle()
            for i in range(nCards):
                topCards.append(self.cards[i])

            return topCards
            

    def drawCards(self, nCards=1):
        cards = self.getTopCard(nCards)
        del self.cards[0:nCards]
        return cards


    def shuffle(self):
        random.shuffle(self.cards)


class CardPile():
    def __init__(self, card, nPlayers):
        self.card = card
        self.cardName = card.name
        self.cardCost = card.cost
        self.count = self.pileCount(card, nPlayers)
        self.empty = False

    def pileCount(self, card, nPlayers):
        if 'Victory' in card.ctypes:
            if nPlayers == 2:
                return 8
            else:
                return 12
        elif card.name == 'Copper':
            return (60-(7*nPlayers))
        elif card.name == 'Silver':
            return 40
        elif card.name == 'Gold':
            return 30
        elif card.name == 'Curse':
            return ((nPlayers*10)-10)
        else:
            return 10


class Board():
    
    nPlayers = 4 

    #Treasure
    coppers = CardPile(copper, nPlayers)
    silvers = CardPile(silver, nPlayers)
    golds = CardPile(gold, nPlayers)

    #Curse Cards
    curses = [curse]*((nPlayers*10)-10)

    #Kingdom Cards
    sampledCards = random.sample(kindomCards, 10)
    pile0 = CardPile(sampledCards[0], nPlayers)
    pile1 = CardPile(sampledCards[1], nPlayers)
    pile2 = CardPile(sampledCards[2], nPlayers)
    pile3 = CardPile(sampledCards[3], nPlayers)
    pile4 = CardPile(sampledCards[4], nPlayers)
    pile5 = CardPile(sampledCards[5], nPlayers)
    pile6 = CardPile(sampledCards[6], nPlayers)
    pile7 = CardPile(sampledCards[7], nPlayers)
    pile8 = CardPile(sampledCards[8], nPlayers)
    pile9 = CardPile(sampledCards[9], nPlayers)

    kingdomCards=[pile0, pile1, pile2, pile3, pile4, 
                    pile5, pile6, pile7, pile8, pile9]
    
    #Victory Cards
    estates = CardPile(estate, nPlayers)
    dutchies = CardPile(duchy, nPlayers)
    provinces = CardPile(province, nPlayers)

    #Trash
    trash = []

class Player():
    def __init__(self, name, board,):
        self.board = board
        self.name = name
        self.hand = []
        self.deck = Deck()

        self.opponents = None
        self.actions = 0
        self.buys = 0
        self.coins = 0
        self.myTurn = False

        self.draw(nCards=5)

    

    def draw(self, nCards=1):
        cards = self.deck.drawCards(nCards)
        self.hand.extend(cards)

    def startTurn(self):
        self.myTurn = True
        self.actions = 1
        self.buys = 1

        actionCards = self.getActionsCard()
        if actionCards == []:
            print('You have no actions cards to play.')
        else:
            self.selectActionCard()
    
    def lookAtHand(self):
        cardNames = [card.name for card in self.hand]
        print(cardNames)

    def actionPhaseOptions(self):
        print('Please select from the following Options:')
        option = 0
        while option not in (1,2):
            print('(1) Play Action Card')
            print('(2) End Action Phase')
            option = int(input())

        if option == 1:
            self.selectActionCard()
        else:
            self.buyPhaseOptions()

            

    def buyPhaseOptions(self):
        print('Please select from the following Options:')
        option = 0
        while option not in (1,2):
            print('(1) Buy a Card')
            print('(2) End Turn')
            option = int(input())

        if option == 1:
            self. selectBuyCard()
        else:
            self.endTurn()

    def getBuyCards(self):
        cards = [cardPile.card.name for cardPile in Board.kingdomCards]

        return cards

    def selectBuyCard(self):
        self.getBuyCards()
        pass

    def getActionsCard(self):
        actionCards = [card for card in self.hand if 'Action' in card.ctypes]

        return actionCards  
    
    def selectActionCard(self):
        if self.actions != 0:
            actionsCards = self.getActionsCard()
            actionCardNames = [card.name for card in actionsCards]
            
            cardIndex = []
            cardSelected = 0
            while cardSelected not in cardIndex:
                print('Choose between these cards:')
                for i, card in enumerate(actionsCards):
                    i += 1
                    print('('+ str(i) + ') ' + card.name)
                    cardIndex.append(i)

                cardIndex.append(i+1)
                print('({}) Do not play action card.'.format(len(cardIndex)) )
                

                cardSelected = int(input())

                if cardSelected == cardIndex[-1]:
                    self.buyPhaseOptions()
                else:
                    selectedCard = actionsCards[cardSelected-1]

                    self.playActionCard(selectedCard)
        else:
            print('Out of Actions, moving to buy phase')
            self.buyPhaseOptions()
        
    
    def playActionCard(self, card):
        print('Player has played ' + card.name)
        self.actions += card.actions
        self.buys += card.buys
        self.coins += card.buys

        if card.carddraw != 0:
            self.draw(nCards=card.carddraw)

        print(card.uAction)

        if card.uAction != None:
            print('action not nones')
            card.uAction()

        self.actions -= 1
        pass
        

    def playMoney(self):
        total = 0
        for card in self.hand:
            if 'Treasure' in card.ctypes:
                total += card.coin

        self.coins += total
            
    def buyCard(self, cardslot):
        if self.buys >= 1:
            if cardslot.count != 0:
                card = cardslot.card
                if card.cost <= self.coins:
                    self.deck.discard.append(card)
                    self.coins -= card.cost 
                    self.buys -= 1
                    
                else:
                    print('Not enough money')
            else:
                print('out of cards')
        else:
            print('You have no buys')

        if self.buys == 0:
            self.endTurn()


    def endTurn(self):
        self.myTurn = False
        self.actions = 0
        self.buys = 0
        self.coins = 0

        self.deck.discard.extend(self.hand)
        self.hand = []
        self.draw(nCards=5)

def runGame():
    #Set Up Game
    nPlayers = 0
    while nPlayers not in (2,3,4):
            print('Enter the number of players (2-4):')
            nPlayers = int(input())
    
    board = Board()
    players = []
    for i in range(nPlayers):
        name = 'Player ' + str(i+1)
        players.append(Player(name, board=board))

    def getOpponents(pList, n):
        newList = pList[:n] + pList[n+1:]
        return newList
        
    for i, player in enumerate(players):
        opps = getOpponents(players, i)
        player.opponents = opps

    #Start game
    def checkPiles():
        emptyPilesCouinter = 0
        for pile in board.kingdomCards:
            if pile.count == 0:
                emptyPilesCouinter += 1

        if nPlayers is not 4:
            if emptyPilesCouinter == 3:
                return False
            else:
                return True
        else:
            if emptyPilesCouinter == 4:
                return False
            else:
                return True

    def checkProvince():
        if board.provinces.count == 0:
            return False
        else:
            return True

    playerTurn = 0
    roundCounter = 0
    MAX_ROUNDS = 5

    while checkPiles() and checkProvince() and roundCounter < MAX_ROUNDS:
        activePlayer = players[playerTurn]
        print('It is ' + activePlayer.name + "'s Turn!")

        activePlayer.startTurn()




        playerTurn += 1
        if playerTurn == nPlayers:
            playerTurn = 0
            roundCounter += 1
            print('Beginning Round ' + str(roundCounter))



if __name__ == '__main__':
    runGame()
    # game = GameManager()
    # game.runGame()

    # board = Board(nPlayers=3)
    # player = Player()
    # player.playMoney()
    # print(player.coins)
    # player.startTurn()
    # print('hand at start of turn')
    # for card in player.hand:
    #     print(card.name)
    # print('-------')
    # player.coins=100
    # player.buys = 10
    # player.buyCard(board.golds)
    # player.buyCard(board.golds)
    # player.buyCard(board.golds)
    # player.buyCard(board.golds)
    # player.buyCard(board.golds)
    # print('Discard')
    # for card in player.deck.discard:
    #     print(card.name)
    # print('Hand After Draw')
    # player.draw(nCards=3)
    # for card in player.hand:
    #     print(card.name)
    
    # print('Deck after draw')
    # for card in player.deck.cards:
    #     print(card.name)

    # print('End Turn')
    # player.endTurn()
    # for card in player.hand:
    #     print(card.name)

    # print('end of turn discard')
    # for card in player.deck.discard:
    #     print(card.name)

    # print('Player next end of turn Deck')
    # for card in player.deck.cards:
    #     print(card.name)
    
    
    