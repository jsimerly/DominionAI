
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

        self.kingdomCards = sorted([pile0, pile1, pile2, pile3, pile4, 
                        pile5, pile6, pile7, pile8, pile9], key=lambda pile:pile.cardCost)
        
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
        self.score = 0
        self.phase = None

        self.draw(nCards=5)

    

    def draw(self, nCards=1):
        cards = self.deck.drawCards(nCards)
        self.hand.extend(cards)

    def startTurn(self):
        self.myTurn = True
        self.actions = 1
        self.buys = 1

        self.lookAtHand()
        self.actionPhase()
    
    def actionPhase(self):
        print('----- Action Phase -----')
        self.phase = 'Action'
        self.selectActionCard()

    def startBuyPhase(self):
        print('----- Buy Phase -----')
        self.phase = 'Buy'
        self.playMoney()
        self.selectBuyCard()
    
    def lookAtHand(self):
        cardNames = [card.name for card in self.hand]
        print(cardNames)

    def selectBuyCard(self):
        selectedPile = self.selectCardPile()
        self.buyCard(selectedPile)

        if self.buys <= 0:
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
                phrase = 'Choose between these cards'
                cardSelected = self.selectCards(actionsCards, selectPhrase=phrase)
                
                if cardSelected == None:
                    self.startBuyPhase()
                else:
                    self.playActionCard(cardSelected)
            else:
                print('Out of Actions, moving to buy phase')
                self.startBuyPhase()

    def selectCardPile(self, selectPhrase = None, costMax = 15):
        cardDict = {}

        for cardPile in self.board.treasureCards:
            cardDict[cardPile.card.abrev] = cardPile
        for cardPile in self.board.vicCards:
            cardDict[cardPile.card.abrev] = cardPile
        for i, cardPile in enumerate(self.board.kingdomCards):
            cardDict[str(i+1)] = cardPile

        if costMax != 15:
            for key, item in cardDict.items():
                if item.cost > costMax:
                    del cardDict[key]

        running = True

        while running:
            if selectPhrase == None:
                print('Please Select a card to buy!')
            else:
                print(selectPhrase)
            
            print('--- Treasure Cards ---')
            firstV = False
            firstK = False
            for key, cardPile in cardDict.items():
                card = cardPile.card

                if card in victoryCards and firstV == False:
                    print('')
                    print('--- Victory Cards ---')
                    firstV = True
                
                if card in kindomCards and firstK == False:
                    print('')
                    print('--- Kingdom Cards ---')
                    firstK = True

                if key == '6':
                    print('')
            
                print('({}) | ${} {} | <{}>  '.format(key, card.cost, card.name, cardPile.count), end='')

            print('')
            print('--- Other ---')
            print('(x) Do not select a card.')
            cardAbrSelected = input()

            if set(cardAbrSelected).issubset(cardDict.keys()) or cardAbrSelected == 'x':
                running = False

        if cardAbrSelected == 'x':
            print('No card selected.')
        else:
            cardPileSelected = cardDict[cardAbrSelected]
            return cardPileSelected
                
    def selectCards(self, cardsToSelectFrom ,selectPhrase, nCardsSelected = 1,):
        cardDict = {}
        for i, card in enumerate(cardsToSelectFrom):
            cardDict[str(1 + i)] = card
                   
        running = True
        while running:
            print(selectPhrase)
            print('Choose between these cards:')
            for abrev ,card in cardDict.items():
                print('({})| ${}  {} |'.format(abrev, card.cost, card.name))
            print('(x) Do not select.')
                
            cardAbrSelected = str(input())

            if nCardsSelected == 1:
                if cardAbrSelected in cardDict.keys() or cardAbrSelected == 'x':
                    running = False
            else:
                cardAbrSelected = [i for i in cardAbrSelected.split()]
                if len(cardAbrSelected) <= nCardsSelected:
                    if set(cardAbrSelected).issubset(cardDict.keys()) or cardAbrSelected == ['x']:
                        running = False
                else:
                    print('Too many cards selected.')
        
        if cardAbrSelected == 'x' or cardAbrSelected == ['x']:
            print('You decided not to select any cards.')
            return None
        else:
            if nCardsSelected == 1:
                cardSelected = cardDict[cardAbrSelected]
                return cardSelected
            else:
                cardsSelected = []
                for abr in cardAbrSelected:
                    cardsSelected.append(cardDict[abr])
                return cardsSelected
                

    def playActionCard(self, card):
        print('Player has played ' + card.name)
        self.actions += card.actions
        self.actions -= 1
        self.buys += card.buys
        self.coins += card.coin

        if card.carddraw != 0:
            self.draw(nCards=card.carddraw)

        self.cardAction(card)
        self.handToDiscard(card)

        self.selectActionCard()

    def cardAction(self, card):
        if card.uAction != None:
            card.uAction(self, self.opponents, self.board)

    def handToDiscard(self, card):
        self.hand.remove(card)
        if type(card) != list:
          
            self.discard.append(card)
        else:
            self.discard.extend(card)
    
    def handToTrash(self, card):
        self.hand.remove(card)
        if type(card) != list:
            self.board.trash.append(card)
        else:
            self.board.trash.extend(card)

    def boardToHand(self, cardPile):
        self.hand.append(cardPile.card)
        cardPile.count += 1
            
            

    def playMoney(self):
        total = 0
        for card in self.hand:
            if 'Treasure' in card.ctypes:
                total += card.coin
                self.handToDiscard(card)

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
        self.phase = None
        self.actions = 0
        self.buys = 0
        self.coins = 0

        self.deck.discard.extend(self.hand)
        self.hand = []
        self.draw(nCards=5)
        

        print(self.name + "'s turn has ended.")
        print('New Hand:')
        self.lookAtHand()


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
    
    
    