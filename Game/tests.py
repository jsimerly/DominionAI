from cards import *
from game import *

def cardActions(card):
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

    player.hand.append(card)
    player.discard.extend([copper, copper, gold])
    player.actions = 1

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
        print('action not nones')
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

def cardReactions(card):
    pass


if __name__ == '__main__':
    #cardActions(harbinger)
    #print('------------------Expected Outcomes-----------------------')
    #cardActions(cellar)
    #cardActions(chapel)
    #cardActions(moat)
    cardReactions(moat)
    #cardActions(merchant) #Appended silver to hand
    cardActions(vassal)