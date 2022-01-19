
class Card():
    def __init__(self, name, cTypes, cost,
                actions=0, cards=0, buys=0, 
                trash=0, coin=0, vp=0, abrev=None,uAction = None):
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
        self.abrev = abrev

#----------Treasure Cards
copper = Card('Copper', ['Treasure'], 0, coin=1, abrev='c')
silver = Card('Silver', ['Treasure'], 3, coin=2, abrev='s')
gold = Card('Gold', ['Treasure'], 6, coin=3, abrev='g')

treasureCards = [copper, silver, gold]

#----------Victory Cards
estate = Card('Estate', ['Victory'], 2, vp=1, abrev='e')
duchy = Card('Dutchy', ['Victory'], 5, vp=3, abrev='d')
province = Card('Province', ['Victory'], 8, vp=6, abrev='p')
curse = Card('Curse', ['Curse'], 0, vp=-1, abrev='curse')

victoryCards = [estate, duchy, province, curse]

#----------Kingdom Cards
#-----2 Cost

#Cellar
def cellarAction(player, opponents, board):
    hand = player.hand

    phrase = 'Select the cards that you wish to discard in the format # # #. Example: 1 2 4.'
    selectedCards = player.selectCardsFromHand(hand, phrase, nCardsSelected=len(hand))
    
    player.handToDiscard(selectedCards)
    player.draw(len(selectedCards))

cellar = Card('Cellar', ['Action'], 2, uAction=cellarAction)

#Chapel
def chapelAction(player, opponents, board):
    hand = player.hand
    
    phrase = 'Select the cards that you wish to TRASH in the format # # #. Example: 1 2 4.'
    selectedCards = player.selectCardsFromHand(hand, phrase, nCardsSelected=len(hand))

    player.handToTrash(selectedCards)

chapel = Card('Chapel', ['Action'], 2,uAction=chapelAction)

#Moat
moat = Card('Moat', ['Action', 'Reaction'], 2, cards=2)

#-----3 Cost
#Harbinger
def harbingerAction(player, opponents, board):
    discardPile = player.discard

    phrase = 'Select a card to place onto your deck:'
    selectedCard = player.selectCards(discardPile, phrase)

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

    phrase = 'Select a card to obtain.'
    selectedCard = player.selectCardPile(selectPhrase=phrase, costMax=4)

    selectedCard.count -= 1
    player.dicard.append(selectedCard.card)

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

            phrase = '''Select the cards that you wish to discard in the format # #. Example: 1 2.
            Choose between these cards: (MUST select 2 cards)'''
            selectedCards = opponent.selectCards(hand, phrase, nCardsSelected = 2)
           
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

            player.handToTrash(copper)
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

        phrase = ''''Select the cards that you wish to discard in the format # #. Example: 1 2.'
        Choose between these cards: (MUST select {} cards)'''.format(str(emptySupplyCounter))
        selectedCards = player.selectCards(player.hand, phrase, emptySupplyCounter)
        
        for card in selectedCards:
            player.handToDiscard(card)
    else:
        print('No discard needed.')

poacher = Card('Poacher', ['Action'], 4, actions=1, coin=1, uAction=poacherAction)

#Remodel
def remodelAction(player, opponents, board):
    hand = player.hand

    phrase = 'Select a card to TRASH.'
    selectedCard = player.selectCards(hand, phrase)
    obtainCard = player.selectCardPile(costMax=(selectedCard.cost+2))

    player.discard.append(obtainCard)
    obtainCard.count -=1
    
remodel = Card('Remodel', ['Action'], 4, uAction=remodelAction)

#Smithy
smithy = Card('Smithy', ['Action'], 4, cards=3,)

#Throne Room
def throneRoomAction(player, opponents, board):
    actionCards = player.getActionsCard()
    phrase = 'Select which card you would like to play twice.'
    selectedCard = player.selectCard(actionCards, phrase)

    def playCard(selectedCard):
        player.actions += selectedCard.actions
        player.buys += selectedCard.buys
        player.coins += selectedCard.coin

        if selectedCard.carddraw != 0:
            player.draw(nCards=selectedCard.carddraw)

        if selectedCard.uAction != None:
            selectedCard.uAction(player, player.opponents, board)

    playCard(selectedCard)
    playCard(selectedCard)
    player.hand.remove(selectedCard)
    player.discard.append(selectedCard)

throneRoom = Card('Throne Room', ['Action'], 4,uAction=throneRoomAction)

#-----5 Cost
#Bandit
def banditAction(player, opponents, board):
    player.discard.append(gold)
    board.golds.count -= 1


    for opponent in opponents:
        print('- {} -'.format(opponent.name))
        reactionCards = opponent.getReactionCards()
        if reactionCards == []:
            top2Cards = opponent.deck.getTopCard(nCards=2)
            for card in top2Cards:
                if card == gold or card == silver:
                    print('{} TRASHED'.format(card.name))
                else:
                    print('{} has been discarded'.format(card.name))
        else:
             print('{} reacts with has a |{}|'.format(opponent.name, reactionCards[0].name))

bandit = Card('Bandit', ['Action', 'Attac'], 5, uAction=banditAction)

#Council Room
def councilRoomAction(players, opponents, board):
    for opponent in opponents:
        opponent.draw()

councilRoom = Card('Council Room', ['Action'],5, buys=1,cards=4 ,uAction=councilRoomAction)

#Festival
festival = Card('Festival', ['Action'], 5, actions=5, buys=1, coin=2)

#Laboratory
laboratory = Card('Laboratory', ['Action'], 5, cards=2, actions=1)

#Library
def libraryAction(player, opponents, board):
    while len(player.hand) < 7:
        player.draw()
        drawnCard = player.hand[-1]
        if 'Action' in drawnCard.ctypes:
            option = 0
            while option not in (1,2):
                print('Keep {}?:'.format(drawnCard.name))
                print('(1) Keep')
                print('(2) Discard')

                option = int(input())

            if option != 1:
                player.hand.remove(drawnCard)
                player.discard.append(drawnCard)

library = Card('Library', ['Action'], 5, uAction=libraryAction)

#Market
market = Card('Market', ['Action'], 5, cards=1, actions=1, buys=1, coin=1)

#Mine
def mineAction(player, opponents, board):
    treasureCards = []
    
    for card in player.hand:
        if card == copper or card == silver:
            treasureCards.append(card)
            
    if treasureCards == []:
        player.actions += 1
        print('No treasure to TRASH.')
        return

    selectedCard = player.selectCards(treasureCards)

    if selectedCard == copper:
        player.handToTrash(copper)
        player.hand.append(silver)
    else:
        player.handToTrash(silver)
        player.hand.append(gold)

mine = Card('Mine', ['Action'], 5, uAction=mineAction)

#sentry
def sentryAction(player, opponents, board):
    player.draw(nCards=2)
    top2Cards = player.hand[-2:]

    keptCards = []
    for card in top2Cards:
        option = 0
        while option not in (1,2,3):
            print('For |{}| Discard, Trash, or Top Deck:'.format(card.name))
            print('(1) Discard')
            print('(2) TRASH')
            print('(3) Top Deck')

            option = int(input())

            player.hand.remove(card)
            if option == 1:
                player.discard.append(card)
            elif option == 2:
                board.trash.append(card)
            else:
                keptCards.append(card)

    if len(keptCards) == 2:
        option = 0
        while option not in (1,2):
            print('Which card would you like to be on top of the deck?')
            print('(non selected card will be second form the top):')
            print('(1) {}'.format(keptCards[0].name))
            print('(2) {}'.format(keptCards[1].name))

            option = int(input())

        if option == 1:
            player.deck.cards.insert(0, keptCards[1])
            player.deck.cards.insert(0, keptCards[0])
        else:
            player.deck.cards.insert(0, keptCards[0])
            player.deck.cards.insert(0, keptCards[1])
    elif len(keptCards) == 1:
        player.deck.insert(0, keptCards[0])
    else:
        print('No cards put back on deck.')

sentry = Card('Sentry', ['Action'],5, cards=1, actions=1, uAction=sentryAction)

#Witch
def witchAction(player, opponents, board):
    for opponent in opponents:
        opponent.discard.append(curse)
        board.curses.count -= 1
    
witch = Card('Witch', ['Action', 'Attack'], 5, cards=2, uAction=witchAction)

#-----6 Cost
#Artisan
def artisanAction(player, opponents, board):

    hand = player.hand

    phrase = 'Please select a card to add to your hand'
    selectedCard = player.selectCards(hand, phrase)
    player.hand.append(selectedCard.card)
    selectedCard.count -= 1

    phrase = 'Please select a card to Top Deck:'
    topDeckCard =  player.selectCards(hand, phrase)
    player.hand.remove(topDeckCard)
    player.deck.cards.insert(0,topDeckCard)

artisan = Card('Artisan', ['Action'], 6, uAction=artisanAction)

kindomCards = [cellar, chapel, moat, 
                harbinger, merchant, vassal, village, workshop,
                bureaucrat, gardens, militia, moneylender, poacher, remodel, smithy, throneRoom,
                bandit, councilRoom, festival, laboratory, library, market, mine, sentry, witch,
                artisan]


if __name__ == '__main__':
    merchant.uAction()
    print('Expected Out Comes----------------')