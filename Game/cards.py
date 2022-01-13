
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
    player.discard.append(topCard)
    option = 0
    while option not in (1,2):
        if 'Action' in topCard.ctypes:
            print('Would you like to play {}:'.format(topCard.name))
            print('(1) Play')
            print('(2) Don\'t play')
            option = int(input())
        else: 
            return

    if option == 1:
        player.actions += topCard.actions
        player.buys += topCard.buys
        player.coins += topCard.coin
        if topCard.uAction != None:
            topCard.uAction(player, opponents, board)
    
vassal = Card('Vassal', ['Action'], 3, coin=2, uAction=vassalAction)

#Village
village = Card('Village', ['Action'], 3, actions=2, cards=1)

#Workshop
def workshopAction(player, opponents, board):
    cardDict = {
        'c' : board.coppers,
        's' : board.silvers,
        'e' : board.estates,
        'curse': board.curses,
    }
    under4 = [cardPile for cardPile in board.kingdomCards if cardPile.card.cost <= 4]
    for i,cardPile in enumerate(under4):
        cardDict[str(i+1)] = cardPile
    
    cardSelected = 0
    while cardSelected not in cardDict.keys() and cardSelected != 'x':
        print('--- Treasure Cards ---')
        for key, cardPile in cardDict.items():
            card = cardPile.card
            print('({})| ${} {} <{}> |   '.format(key ,card.cost, card.name, cardPile.count), end=' ')
            if key == 's':
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
        print(player.name + ' did not buy a card.')
    else:
        selectedCard = cardDict[cardSelected]
        player.discard.append(selectedCard.card)
        selectedCard.count -= 1

workshop = Card('Workshop', ['Action'], 3, uAction=workshopAction)

#-----4 Cost
#Bureacrat
def bureacratAction(player, opponents, board):
    player.deck.cards.insert(0, silver)
    board.silvers.count -= 1

    for opponent in opponents:
        reactionCards = opponent.getReactionCards()
        if reactionCards == []:
            reveal = False
            for card in opponent.hand:
                if 'Victory' in card.ctypes and reveal == False:
                    print('{} reveals |{}| and places it on the top of their deck.'.format(opponent.name, card.name))
                    opponent.hand.remove(card)
                    opponent.deck.cards.insert(0, card)

                    reveal = True
            if reveal == False:
                print('{} reveals thier hand: {}'.format(opponent.name, str([card.name for card in opponent.hand])))
        else:
            print('{} reacts with has a |{}|'.format(opponent.name, reactionCards[0].name))

bureaucrat = Card('Bureaucrat', ['Action', 'Attack'], 4, uAction=bureacratAction)

#Gardens
gardens = Card('Gardens', ['Victory'], 4)

#Militia
def militiaAction(player, opponents, board):
    for opponent in opponents:
        reactionCards = opponent.getReactionCards()
        if reactionCards == []:
            
            hand = opponent.hand
            cardsSelected = []
            cardIndex = []
            running = True

            while running:
                cardIndex=[]
                cardsSelected = []
                print('------- {}\'s choice ------'.format(opponent.name))
                print('Select the cards that you wish to discard in the format # #. Example: 1 2.')
                print('Choose between these cards: (MUST select 2 cards)')
                for i, card in enumerate(hand):
                    i += 1
                    print('('+ str(i) + ') ' + card.name)
                    cardIndex.append(i)

                rawInput = str(input())
                cardsSelected = [int(i) for i in rawInput.split()]

                if set(cardsSelected).issubset(cardIndex) and len(cardsSelected) == 2:
                    running = False
            
            
            selectedCards = [hand[i-1] for i in cardsSelected]
            for card in selectedCards:
                hand.remove(card)
                opponent.discard.append(card)
            
            print('{}\'s new hand is: {}'.format(opponent.name, str([card.name for card in hand])))
        else:
             print('{} reacts with has a |{}|'.format(opponent.name, reactionCards[0].name))

militia = Card('Milita', ['Action', 'Attack'], 4, coin=2, uAction=militiaAction)

#Moneylender:
def moneylenderAction(player, opponents, board):
    if copper not in player.hand:
        print('No copper to trash and cannot play moneylender')
        player.actions += 1
    else:
        option = 0
        while option not in (1,2):
            print('Select form the following:')
            print('(1) TRASH a copper for +3 coins')
            print('(2) Do not trash')
            option = int(input())

        if option == 1:
            print('{} TRASHED a copper and gained 3 coins.'.format(player.name))
            player.coins += 3
            player.hand.remove(copper)
            board.trash.append(copper)
        else:
            print('{} decides not to play Moneylender.'.format(player.name))
            player.actions += 1

moneylender = Card('Moneylender', ['Action'], 4,uAction=moneylenderAction)

#Poacher
def poacherAction(player, opponents, board):
    emptySupplyCounter = 0
    for cardPile in board.kingdomCards:
        if cardPile.count == 0:
            emptySupplyCounter += 1
    
    if emptySupplyCounter != 0:
        print('Discard {} cards.'.format(str(emptySupplyCounter)))

        cardsSelected = []
        cardIndex = []
        running = True

        while running:
            cardIndex=[]
            cardsSelected = []
            print('Select the cards that you wish to discard in the format # #. Example: 1 2.')
            print('Choose between these cards: (MUST select {} cards)'.format(str(emptySupplyCounter)))
            for i, card in enumerate(player.hand):
                i += 1
                print('('+ str(i) + ') ' + card.name)
                cardIndex.append(i)

            rawInput = str(input())
            cardsSelected = [int(i) for i in rawInput.split()]

            if set(cardsSelected).issubset(cardIndex) and len(cardsSelected) == emptySupplyCounter:
                running = False
        
        
        selectedCards = [player.hand[i-1] for i in cardsSelected]
        for card in selectedCards:
            player.hand.remove(card)
            player.discard.append(card)
            
    else:
        print('No discard needed.')

poacher = Card('Poacher', ['Action'], 4, actions=1, coin=1, uAction=poacherAction)

#Remodel
def remodelAction(player, opponents, board):
    hand = player.hand

    cardIndex = []
    cardSelected = 0
    while cardSelected not in cardIndex:
        print('Choose between these cards:')
        for i, card in enumerate(hand):
            i += 1
            print('('+ str(i) + ') ' + card.name)
            cardIndex.append(i)
        cardIndex.append(i+1)

        print('({}) Do not remodel.'.format(len(cardIndex)))

        cardSelected = int(input())
    
    if cardSelected == cardIndex[-1]:
        print('{} decided not to remodel.'.format(player.name))
        player.actions += 1
    else:
        selectedCard = hand[cardSelected-1]
        hand.remove(selectedCard)
        board.trash.append(selectedCard)
        maxValue = selectedCard.cost + 2

        cardDict = {}
        
        eligableTCards = [cardPile for cardPile in board.treasureCards if cardPile.card.cost <= maxValue]
        for cardPile in eligableTCards:
            if cardPile.card.name == 'Copper':
                cardDict['c'] = cardPile
            if cardPile.card.name == 'Silver':
                cardDict['s'] = cardPile
            if cardPile.card.name == 'Gold':
                cardDict['g'] = cardPile

        eligableVCards = [cardPile for cardPile in board.vicCards if cardPile.card.cost <= maxValue]
        for cardPile in eligableVCards:
            if cardPile.card.name == 'Estate':
                cardDict['e'] = cardPile
            if cardPile.card.name == 'Duchy':
                cardDict['d'] == cardPile
            if cardPile.card.name == 'Provinces':
                cardDict['p'] == cardPile
            if cardPile.card.name == 'Curse':
                cardDict['curse'] = cardPile
        
        

        eligableKCards = [cardPile for cardPile in board.kingdomCards if cardPile.card.cost <= maxValue]
        for i,cardPile in enumerate(eligableKCards):
            cardDict[str(i+1)] = cardPile

        cardSelected = 0
        while cardSelected not in cardDict.keys():
            print('--- Treasure Cards ---')
            for key, cardPile in cardDict.items():
                card = cardPile.card
                print('({})| ${} {} <{}> |   '.format(key ,card.cost, card.name, cardPile.count), end=' ')
                if key == 's':
                    print('')
                    print('--- Victory Cards ---')
                if key == 'curse':
                    print('')
                    print('--- Kingdom Cards ---')
                if key == '5':
                    print('')

            print('')
            print('Select which card you would like to obtain.')
            cardSelected = str(input())
        
        selectedCard = cardDict[cardSelected]
        player.discard.append(selectedCard.card)
        selectedCard.count -= 1   
    
remodel = Card('Remodel', ['Action'], 4, uAction=remodelAction)

#Smithy
smithy = Card('Smithy', ['Action'], 4, cards=3,)

#Throne Room
def throneRoomAction(player, opponents, board):
    hand = player.hand

    actionCards = player.getActionsCard()

    cardSelected = 0
    cardIndex = []
    while cardSelected not in cardIndex:    
        print('Select which card you would like to play twice.')
        for i, card in enumerate(actionCards):
            print('({}) {}'.format(i+1, card.name))
            cardIndex.append(i+1)

        cardSelected = int(input())

    selectedCard = actionCards[cardSelected-1]

    def playCard(selectedCard):
        player.actions += selectedCard.actions
        player.buys += selectedCard.buys
        player.coins += selectedCard.coin

        if selectedCard.carddraw != 0:
            player.draw(nCards=selectedCard.carddraw)

        if card.uAction != None:
            selectedCard.uAction(player, player.opponents, board)

    playCard(selectedCard)
    playCard(selectedCard)
    player.hand.remove(selectedCard)
    player.discard.append(selectedCard)

throneRoom = Card('Throne Room', ['Action'], 4,uAction=throneRoomAction)

#-----5 Cost
#Bandit
def banditAction(player, opponents, board):
    pass

bandit = Card('Bandit', ['Action', 'Attac'], 5, uAction=banditAction)
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
                bureaucrat, gardens, militia, moneylender, poacher, remodel, smithy, throneRoom,
                bandit, councilRoom, festival, laboratory, library, market, mine, sentry, witch,
                artisan]


if __name__ == '__main__':
    merchant.uAction()
    print('Expected Out Comes----------------')