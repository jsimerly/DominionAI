
class Card():
    def __init__(self, name, cTypes, cost,
                actions=0, cards=0, buys=0, 
                trash=0, coin=0, vp=0, uAction = None):
        self.name = name
        self.ctypes = cTypes
        self.cost = cost
        self.actions = actions
        self.carddraw = cards
        self.buys = buys
        self.trash = trash
        self.coin = coin
        self.vp = vp
        self.uAction = uAction

#----------Kingdom Cards
#-----2 Cost

#Cellar
def cellarAction(player, opponents, board):
    hand = player.hand
    
    cardsSelected = []
    cardIndex = []
    running = True
    while running:
        cardIndex=[]
        cardsSelected = []
        print('Select the cards that you wish to discard in the format # # #. Example: 1 2 4.')
        print('Choose between these cards:')
        for i, card in enumerate(hand):
            i += 1
            print('('+ str(i) + ') ' + card.name)
            cardIndex.append(i)
        cardIndex.append(i+1)

        print('({}) Do discard.'.format(len(cardIndex)) )

        rawInput = str(input())
        cardsSelected = [int(i) for i in rawInput.split()]

        if set(cardsSelected).issubset(cardIndex):
            running = False
     
   
    if cardIndex[-1] in cardsSelected:
        print('No cards discarded')
    else:
        selectedCards = [hand[i-1] for i in cardsSelected]
        for card in selectedCards:
            hand.remove(card)
            player.discard.append(card)
        player.draw(nCards=len(cardsSelected))

cellar = Card('Cellar', ['Action'], 2, uAction=cellarAction)

#Chapel
def chapelAction(player, opponents, board):
    hand = player.hand
    
    cardsSelected = []
    cardIndex = []
    running = True
    while running:
        cardIndex=[]
        cardsSelected = []
        print('Select the cards that you wish to TRASH in the format # # #. Example: 1 2 4.')
        print('Choose between these cards:')
        for i, card in enumerate(hand):
            i += 1
            print('('+ str(i) + ') ' + card.name)
            cardIndex.append(i)
        cardIndex.append(i+1)

        print('({}) Do TRASH.'.format(len(cardIndex)) )

        rawInput = str(input())
        cardsSelected = [int(i) for i in rawInput.split()]

        if set(cardsSelected).issubset(cardIndex):
            running = False
     
   
    if cardIndex[-1] in cardsSelected:
        print('No cards trashed')
    else:
        selectedCards = [hand[i-1] for i in cardsSelected]
        for card in selectedCards:
            hand.remove(card)
            board.trash.append(card)
chapel = Card('Chapel', ['Action'], 2,uAction=chapelAction)

#Moat
moat = Card('Moat', ['Action', 'Reaction'], 2, cards=2)

#-----3 Cost
#Harbinger
def harbingerAction(player, opponents, board):
    discardPile = player.discard
    if discardPile == []:
        print('Your discard pile is empty')
    else:
        print('Select a card to place onto your deck:')
        cardIndex = []
        cardSelected = 0
        while cardSelected not in cardIndex:
            print('Choose between these cards:')
            for i, card in enumerate(discardPile):
                i += 1
                print('('+ str(i) + ') ' + card.name)
                cardIndex.append(i)
            cardIndex.append(i+1)

            print('({}) Do not select a card.'.format(len(cardIndex)) )

            cardSelected = int(input())

        if cardSelected == cardIndex[-1]:
           print('No card topdecked.')
        else:
            selectedCard = discardPile[cardSelected-1]
            print(selectedCard.name)
            player.deck.cards.insert(0, selectedCard)
            player.discard.remove(selectedCard)

harbinger = Card('Harbinger', ['Action'], 3, actions=1, cards=1, uAction=harbingerAction)

#Merchant
def merchantAction(player, opponents, board):
    if silver in player.hand:
        player.coins += 1
merchant = Card('Merchant', ['Action'], 3, actions=1, cards=1, uAction=merchantAction)

#Vassal
def vassalAction(player, opponents, board):
    player.draw()
    topCard = player.hand[-1]
    if 'Action' in topCard.ctypes:
        print(topCard.name)
vassal = Card('Vassal', ['Action'], 3, coin=2, uAction=vassalAction)

village = Card('Village', ['Action'], 3, actions=2, cards=1)
workshop = Card('Workshop', ['Action'], 3,)

#-----4 Cost
bureaucrat = Card('Bureaucrat', ['Action', 'Attack'], 4,)
feast = Card('Feast', ['Action'], 4,)
gardens = Card('Gardens', ['Victory'], 4)
militia = Card('Milita', ['Action', 'Attack'], 4, coin=2)
moneylender = Card('Moneylender', ['Action'], 4,)
poacher = Card('Poacher', ['Action'], 4, actions=1, coin=1)
remodel = Card('Remodel', ['Action'], 4,)
smithy = Card('Smithy', ['Action'], 4, cards=3,)
throneRoom = Card('Throne Room', ['Action'], 4,)

#-----5 Cost
bandit = Card('Bandit', ['Action', 'Attac'], 5,)
councilRoom = Card('Council Room', ['Action'],5, buys=1)
festival = Card('Festival', ['Action'], 5, actions=5, buys=1, coin=2)
laboratory = Card('Laboratory', ['Action'], 5, cards=2, actions=1)
library = Card('Library', ['Action'], 5,)
market = Card('Market', ['Action'], 5, cards=1, actions=1, buys=1, coin=1)
mine = Card('Mine', ['Action'], 5,)
sentry = Card('Sentry', ['Action'],5, cards=1, actions=1)
witch = Card('Witch', ['Action', 'Attack'], 5, cards=2,)

#-----6 Cost
artisan = Card('Artisan', ['Action'], 6,)

kindomCards = [cellar, chapel, moat, 
                harbinger, merchant, vassal, village, workshop,
                bureaucrat, feast, gardens, militia, moneylender, poacher, remodel, smithy, throneRoom,
                bandit, councilRoom, festival, laboratory, library, market, mine, sentry, witch,
                artisan]

#----------Treasure Cards
copper = Card('Copper', ['Treasure'], 0, coin=1)
silver = Card('Silver', ['Treasure'], 3, coin=2)
gold = Card('Gold', ['Treasure'], 6, coin=3)

treasureCards = [copper, silver, gold]

#----------Victory Cards
estate = Card('Estate', ['Victory'], 2, vp=1)
duchy = Card('Dutchy', ['Victory'], 5, vp=3)
province = Card('Province', ['Victory'], 8, vp=6)
curse = Card('Curse', ['Curse'], 0, vp=-1)

victoryCards = [estate, duchy, province, curse]

if __name__ == '__main__':
    merchant.uAction()
    print('Expected Out Comes----------------')