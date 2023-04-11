import random 
from players import player


def create_game(number_of_players=3):
    players = []
    for i in range(number_of_players):
        players.append(
            player(
                0.3, 0.66, 0.66, f"C{i+1}"
            )
        )
    
    deck = []
    for j in range(6):
        if j>i:
            deck.append(f"C{j+1}")

    for k in range(6):
        deck.append("C1")
        deck.append("C2")
        deck.append("C3")
        deck.append("C4")
        deck.append("C5")
        deck.append("C6")

    random.shuffle(deck)
    random.shuffle(deck)

    cut = deck[10:]
    deck[10:] = []
    for l in range(7):
        cut.append("B")
    random.shuffle(cut)
    random.shuffle(cut)
    for m in cut:
        deck.append(m)
    
    return players, deck


def play_a_turn(auctioneer, players, flip):
    return None
