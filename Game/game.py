
# import random
import numpy.random as random
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
    def __init__(self, nPlayers):
        #Treasure
        self.coppers = CardPile(copper, nPlayers)
        self.silvers = CardPile(silver, nPlayers)
        self.golds = CardPile(gold, nPlayers)

        self.treasureCards=[self.coppers, self.silvers, self.golds]

        #Curse Cards
        self.curses = CardPile(curse, nPlayers)

        #Kingdom Cards
        sampledCards = random.choice(kindomCards, size=10, replace=False)
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

        self.kingdomCards=[pile0, pile1, pile2, pile3, pile4, 
                        pile5, pile6, pile7, pile8, pile9]
        
        #Victory Cards
        self.estates = CardPile(estate, nPlayers)
        self.dutchies = CardPile(duchy, nPlayers)
        self.provinces = CardPile(province, nPlayers)

        self.vicCards = [self.estates, self.dutchies, self.provinces, self.curses]
        

        #Trash
        self.trash = []

class Player():
    def __init__(self, name, board,):
        self.board = board
        self.name = name
        self.hand = []
        self.discard = []
        self.deck = Deck()

        self.opponents = None
        self.actions = 0
        self.buys = 0
        self.coins = 0
        self.myTurn = False
        self.score = 0

        self.draw(nCards=5)

    

    def draw(self, nCards=1):
        cards = self.deck.drawCards(nCards)
        self.hand.extend(cards)

    def startTurn(self):
        self.myTurn = True
        self.actions = 1
        self.buys = 1
        hand = [card.name for card in self.hand]
        print('Hand: {}'.format(hand))
        print('----- Action Phase -----')
        self.selectActionCard()
        actionCards = self.getActionsCard()
    
    def lookAtHand(self):
        cardNames = [card.name for card in self.hand]
        print(cardNames)

    def startBuyPhase(self):
        print('----- Buy Phase -----')
        self.playMoney()
        self.selectBuyCard()

    def getBuyCards(self):
        cards = [cardPile for cardPile in self.board.kingdomCards]
        return cards

    def selectBuyCard(self):
        cardPiles = self.getBuyCards()
        
        cardDict = {
            'c' : self.board.coppers,
            's' : self.board.silvers,
            'g' : self.board.golds,
            'e' : self.board.estates,
            'd' : self.board.dutchies,
            'p' : self.board.provinces,
            'curse' : self.board.curses,
        }
        for i, cardPile in enumerate(cardPiles):
            cardDict[str(i+1)] = cardPile

        cardSelected = 0
        while cardSelected not in cardDict.keys() and cardSelected != 'x':
            print('Budget: $' + str(self.coins))
            print('--- Treasure Cards ---')
            for key, cardPile in cardDict.items():
                card = cardPile.card
                
                print('({})| ${} {} <{}> |   '.format(key ,card.cost, card.name, cardPile.count), end=' ')
                if key == 'g':
                    print('')
                    print('--- Victory Cards ---')

                if key == 'curse':
                    print('')
                    print('--- Kingdom Cards ---')
                
                if key == '5':
                    print('')
                
            print('')
            print('--- Other ---')
            print('(x) Do not buy a card. End Turn.')
            cardSelected = input()

        if cardSelected == 'x':
            print(self.name + ' did not buy a card.')
            self.endTurn()
        else:
            selectedCard = cardDict[cardSelected]
            self.buyCard(selectedCard)

            if self.buys == 0:
                self.endTurn()
            else:
                self.selectBuyCard()

    def getReactionCards(self):
        reactionCards = [card for card in self.hand if 'Reaction' in card.ctypes]
        return reactionCards


    def getActionsCard(self):
        actionCards = [card for card in self.hand if 'Action' in card.ctypes]

        return actionCards  
    
    def selectActionCard(self):
        actionsCards = self.getActionsCard()
        if actionsCards == []:
            print('You do not have any action cards in hand, moving to buy phase.')
            self.startBuyPhase()
        else:
            if self.actions != 0:
                
                
                cardIndex = []
                cardSelected = 0
                while cardSelected not in cardIndex:
                    print('Choose between these cards:')
                    for i, card in enumerate(actionsCards):
                        i += 1
                        print('('+ str(i) + ') ' + card.name)
                        cardIndex.append(i)
                    cardIndex.append(i+1)

                    print('({}) Do not play action card.'.format(len(cardIndex)))

                    cardSelected = int(input())

                if cardSelected == cardIndex[-1]:
                    self.startBuyPhase()
                else:
                    selectedCard = actionsCards[cardSelected-1]

                    self.playActionCard(selectedCard)
            else:
                print('Out of Actions, moving to buy phase')
                self.startBuyPhase()
        
    
    def playActionCard(self, card):
        print('Player has played ' + card.name)
        self.actions += card.actions
        self.buys += card.buys
        self.coins += card.coin
        
        self.hand.remove(card)

        if card.carddraw != 0:
            self.draw(nCards=card.carddraw)

        if card.uAction != None:
            card.uAction(self, self.opponents, self.board)

        self.discard.append(card)
        self.actions -= 1
        self.selectActionCard()
    
    
            

    def playMoney(self):
        total = 0
        for card in self.hand:
            if 'Treasure' in card.ctypes:
                total += card.coin

        self.coins += total
            
    def buyCard(self, cardslot):
        if cardslot.count != 0:
            card = cardslot.card
            if card.cost <= self.coins:
                cardslot.count -= 1
                self.deck.discard.append(card)
                self.coins -= card.cost 
                self.buys -= 1

                print(self.name + ' bought a ' +card.name)

                
            else:
                print('You do not have enough money, choose another option')
        else:
            print('Card Pile is Empty, choose another option')


    def endTurn(self):
        self.myTurn = False
        self.actions = 0
        self.buys = 0
        self.coins = 0

        self.deck.discard.extend(self.hand)
        self.hand = []
        self.draw(nCards=5)
        hand = [card.name for card in self.hand]

        print(self.name + "'s turn has ended.")
        print('New Hand: {}'.format(hand))


def getOpponents(pList, n):
        newList = pList[:n] + pList[n+1:]
        return newList

def checkPiles(board, nPlayers):
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

def checkProvince(board):
    if board.provinces.count == 0:
        return False
    else:
        return True

def runGame():
    #Set Up Game
    nPlayers = 0
    while nPlayers not in (2,3,4):
            print('Enter the number of players (2-4):')
            nPlayers = int(input())
    
    board = Board(nPlayers)
    players = []
    for i in range(nPlayers):
        name = 'Player ' + str(i+1)
        players.append(Player(name, board=board))

    
        
    for i, player in enumerate(players):
        opps = getOpponents(players, i)
        player.opponents = opps

    #Start game
    playerTurn = 0
    roundCounter = 1
    MAX_ROUNDS = 5

    while checkPiles(board, nPlayers) and checkProvince(board) and roundCounter < MAX_ROUNDS:
        activePlayer = players[playerTurn]
        print('------------------------------------------------')
        print('It is ' + activePlayer.name + "'s Turn!")

        activePlayer.startTurn()




        playerTurn += 1
        if playerTurn == nPlayers:
            playerTurn = 0
            roundCounter += 1
            print('------------------------------------------------')
            print('Beginning Round ' + str(roundCounter))
    
    print('=================The Game Has Ended======================')
    for player in players:
        allCards = []
        allCards.extend(player.discard)
        allCards.extend(player.deck.cards)
        allCards.extend(player.hand)

        gardenCount = 0
        for card in allCards:
            player.score += card.vp
            if card == gardens:
                gardenCount += 1

        deckTotal = len(allCards)
        gardenPoints = gardenCount * (deckTotal//10)
        player.score += gardenPoints
    

    rankedPlayers = sorted(players, key=lambda player:player.score, reverse=True)

    place = 1
    print('{} WINS!!'.format(rankedPlayers[0].name))
    for player in rankedPlayers:
        print('{}) {}: {}pts'.format(str(place), player.name, player.score))
        place += 1



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
    
    
    