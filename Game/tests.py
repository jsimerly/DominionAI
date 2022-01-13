from cards import *
from game import *

def cardActions(card, reaction=False):
    nPlayers = 4
    board = Board(nPlayers)

    players = [Player('Player 1', board=board),
                Player('Player 2', board=board),
                Player('Player 3', board=board),
                Player('Player 4', board=board)]

    for i, player in enumerate(players):
        opps = getOpponents(players, i)
        player.opponents = opps

    player = players[0]

    if reaction:
        for opponent in player.opponents:
            opponent.hand.append(card)
        player.hand.append(bureaucrat)
    else:
        player.hand.append(card)
        #player.hand.append(silver) # for merchant testing
        #player.deck.cards.insert(0, merchant) #for vassal testing
        #player.board.kingdomCards[0].count = 0 #for poacher testing
        #player.hand.append(village) #for throneroom testings
        player.discard.extend([copper, copper, gold])
        player.actions = 1

    if reaction:
        print('{} has played a bureacrat!'.format(player.name))
        bureaucrat.uAction(player, player.opponents, board)
    else:
        print('-----------------Test Begins--------------------')
        #player.playActionCard(card) without moving to the next action 
        print('Player has played ' + card.name)
        player.actions += card.actions
        player.buys += card.buys
        player.coins += card.coin
        player.hand.remove(card)

        if card.carddraw != 0:
            player.draw(nCards=card.carddraw)

        if card.uAction != None:
            card.uAction(player, player.opponents, board)

        player.discard.append(card)
        player.actions -= 1
    print('----------------------Outcomes----------------------')
    print('Actions: ' + str(player.actions))
    print('Coins: ' + str(player.coins))
    print('Buys: ' + str(player.buys))
    print('Hand: ' + str([card.name for card in player.hand]))
    print('Discard :' +str([card.name for card in player.discard]))
    print('Next 2 cards on deck: ' + str([card.name for card in player.deck.cards[0:2]]))
    print('TRASH: ' + str([card.name for card in board.trash]))
    print('-------- Opponent Outcomes ---------')
    for i,opp in enumerate(player.opponents):
        oppHand = [card.name for card in opp.hand]
        oppDiscard = [card.name for card in opp.discard]
        print('Opponent {}\'s Hand: {}'.format(i, oppHand))
        print('Opponent {}\'s Discard: {}'.format(i, oppDiscard))



if __name__ == '__main__':
    #cardActions(harbinger)
    #cardActions(cellar)
    #cardActions(chapel)
    #cardActions(moat)
    #cardActions(merchant) #Appended silver to hand
    #cardActions(vassal) #added action card to top of deck
    #cardActions(workshop)
    #cardActions(bureaucrat)
    #cardActions(moat, reaction=True)
    #cardActions(militia)
    #cardActions(moneylender)
    #cardActions(poacher) #Emptied a supply file
    #cardActions(remodel)
    #cardActions(throneRoom) #appened actioncard to hand