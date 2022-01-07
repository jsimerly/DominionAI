
import random

class Card():
    def __init__(self, name, cTypes, cost,
                actions=0, cards=0, buys=0, 
                trash=0, coin=0, vp=0):
        self.name = name
        self.ctypes = cTypes
        self.cost = cost
        self.actions = actions
        self.carddraw = cards
        self.buys = buys
        self.trash = trash
        self.coin = coin
        self.vp = vp

#Kingdom Cards
cellar = Card('Cellar', ['Action'], 2,)
chapel = Card('Chapel', ['Action'], 2,)
moat = Card('Moat', ['Action', 'Reaction'], 2, cards=2)
chancellor = Card('Chancellor', ['Action'], 3, coin=2)
harbinger = Card('Harbinger', ['Action'], 3, actions=1, cards=1)
merchant = Card('Merchant', ['Action'], 3, actions=1, cards=1)
vassal = Card('Vassal', ['Action'], 3, coin=2)
village = Card('Village', ['Action'], 3, actions=2, cards=1)
workshop = Card('Workshop', ['Action'], 3,)
bureaucrat = Card('Bureaucrat', ['Action', 'Attack'], 4,)
feast = Card('Feast', ['Action'], 4,)
gardens = Card('Gardens', ['Victory'], 4)
militia = Card('Milita', ['Action', 'Attack'], 4, coin=2)
moneylender = Card('Moneylender', ['Action'], 4,)
poacher = Card('Poacher', ['Action'], 4, actions=1, coin=1)
remodel = Card('Remodel', ['Action'], 4,)
smithy = Card('Smithy', ['Action'], 4, cards=3,)
throneRoom = Card('Throne Room', ['Action'], 4,)
bandit = Card('Bandit', ['Action', 'Attac'], 5,)
councilRoom = Card('Council Room', ['Action'],5, buys=1)
festival = Card('Festival', ['Action'], 5, actions=5, buys=1, coin=2)
laboratory = Card('Laboratory', ['Action'], 5, cards=2, actions=1)
library = Card('Library', ['Action'], 5,)
market = Card('Market', ['Action'], 5, cards=1, actions=1, buys=1, coin=1)
mine = Card('Mine', ['Action'], 5,)
sentry = Card('Sentry', ['Action'],5, cards=1, actions=1)
witch = Card('Witch', ['Action', 'Attack'], 5, cards=2,)
artisan = Card('Artisan', ['Action'], 6,)

kindomCards = [cellar, chapel, moat, 
                chancellor, harbinger, merchant, vassal, village, workshop,
                bureaucrat, feast, gardens, militia, moneylender, poacher, remodel, smithy, throneRoom,
                bandit, councilRoom, festival, laboratory, library, market, mine, sentry, witch,
                artisan]

#Treasure Cards
copper = Card('Copper', ['Treasure'], 0, coin=1)
silver = Card('Silver', ['Treasure'], 3, coin=2)
gold = Card('Gold', ['Treasure'], 6, coin=3)

treasureCards = [copper, silver, gold]

#Victory Cards
estate = Card('Estate', ['Victory'], 2, vp=1)
duchy = Card('Dutchy', ['Victory'], 5, vp=3)
province = Card('Province', ['Victory'], 8, vp=6)
curse = Card('Curse', ['Curse'], 0, vp=-1)

victoryCards = [estate, duchy, province, curse]


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
    def __init__(self, nPlayers=4):
        #Treasure
        self.coppers = CardPile(copper, nPlayers)
        self.silvers = CardPile(silver, nPlayers)
        self.golds = CardPile(gold, nPlayers)

        #Curse Cards
        self.curses = [curse]*((nPlayers*10)-10)

        #Kingdom Cards
        sampledCards = random.sample(kindomCards, 10)
        self.pile0 = CardPile(sampledCards[0], nPlayers)
        self.pile1 = CardPile(sampledCards[1], nPlayers)
        self.pile2 = CardPile(sampledCards[2], nPlayers)
        self.pile3 = CardPile(sampledCards[3], nPlayers)
        self.pile4 = CardPile(sampledCards[4], nPlayers)
        self.pile5 = CardPile(sampledCards[5], nPlayers)
        self.pile6 = CardPile(sampledCards[6], nPlayers)
        self.pile7 = CardPile(sampledCards[7], nPlayers)
        self.pile8 = CardPile(sampledCards[8], nPlayers)
        self.pile9 = CardPile(sampledCards[9], nPlayers)

        self.kingdomCards=[self.pile0, self.pile1, self.pile2, self.pile3, self.pile4, 
                            self.pile5, self.pile6, self.pile7, self.pile8, self.pile9]
        
        #Victory Cards
        self.estates = CardPile(estate, nPlayers)
        self.dutchies = CardPile(duchy, nPlayers)
        self.provinces = CardPile(province, nPlayers)

        #Trash
        self.trash = []

class Player():
    def __init__(self):
        self.hand = []
        self.deck = Deck()
        
        self.actions = 0
        self.buys = 0
        self.coins = 0
        self.myTurn = False
        self.phase = 'None'

        self.draw(nCards=5)



    def draw(self, nCards=1):
        cards = self.deck.drawCards(nCards)
        self.hand.extend(cards)

    def startTurn(self):
        self.myTurn = True
        self.actions = 1
        self.buys = 1

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


        


if __name__ == '__main__':
    board = Board(nPlayers=3)
    player = Player()
    player.playMoney()
    print(player.coins)
    player.startTurn()
    print('hand at start of turn')
    for card in player.hand:
        print(card.name)
    print('-------')
    player.coins=100
    player.buys = 10
    player.buyCard(board.golds)
    player.buyCard(board.golds)
    player.buyCard(board.golds)
    player.buyCard(board.golds)
    player.buyCard(board.golds)
    print('Discard')
    for card in player.deck.discard:
        print(card.name)
    print('Hand After Draw')
    player.draw(nCards=3)
    for card in player.hand:
        print(card.name)
    
    print('Deck after draw')
    for card in player.deck.cards:
        print(card.name)

    print('End Turn')
    player.endTurn()
    for card in player.hand:
        print(card.name)

    print('end of turn discard')
    for card in player.deck.discard:
        print(card.name)

    print('Player next end of turn Deck')
    for card in player.deck.cards:
        print(card.name)
    
    
    