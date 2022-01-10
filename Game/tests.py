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

    if card.carddraw != 0:
        player.draw(nCards=card.carddraw)

    if card.uAction != None:
        print('action not nones')
        card.uAction(player, player.opponents, board)

    player.actions -= 1
    print('----------------------Outcomes----------------------')
    print('Actions: ' + str(player.actions))
    print('Coins: ' + str(player.coins))
    print('Buys: ' + str(player.buys))
    print('Hand: ' + str([card.name for card in player.hand]))
    print('Discard :' +str([card.name for card in player.discard]))
    print('Next 2 cards on deck: ' + str([card.name for card in player.deck.cards[0:2]]))
    for i,opp in enumerate(player.opponents):
        oppHand = [card.name for card in opp.hand]
        print('Opponent {}\'s Hand: {}'.format(i, oppHand))


if __name__ == '__main__':
    cardActions(harbinger)