
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

    def getTopCard(self, nCards=1):
        if nCards == 1:
            return self.cards[0]
        else:
            topCards = []
            for i in range(nCards):
                topCards.append(self.cards[i])
            return topCards

class Discard():
    def __init__(self):
        self.cards = []
        
class Hand():
    def __init__(self):
        self.cards = []


class Board():
    def __init__(self, nPlayers=4):
        #Treasure
        self.coppers = [copper]*(60-(7*nPlayers))
        self.silvers = [silver]*40
        self.golds = [gold]*30

        #Victory Cards
        if nPlayers == 2:
            self.estates = [estate]*8
            self.dutchies = [duchy]*8
            self.provinces = [province]*8
        else:
            self.estates = [estate]*12
            self.dutchies = [duchy]*12
            self.provinces = [province]*12

        #Curse Cards
        self.curses = [curse]*((nPlayers*10)-10)

        #Kingdom Cards
        sampledCards = random.sample(kindomCards, 10)
        self.cardSlot1 = sampledCards[0]
        self.cardSlot2 = sampledCards[1]
        self.cardSlot3 = sampledCards[2]
        self.cardSlot4 = sampledCards[3]
        self.cardSlot5 = sampledCards[4]
        self.cardSlot6 = sampledCards[5]
        self.cardSlot7 = sampledCards[6]
        self.cardSlot8 = sampledCards[7]
        self.cardSlot9 = sampledCards[8]
        self.cardSlot10 = sampledCards[9]


        #Trash
        self.trash = []

class Player():
    def __init__(self):
        self.hand = Hand()
        self.deck = Deck()

    def draw(self, nCards=1):
        cards = self.deck.getTopCard()
        self.hand.cards.extend(cards)


if __name__ == '__main__':
    board = Board(nPlayers=3)
    print(board.cardSlot1.name)
    print(board.cardSlot2.name)
    print(board.cardSlot3.name)
    print(board.cardSlot4.name)
    print(len(board.dutchies))