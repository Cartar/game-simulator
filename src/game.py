from random import random, shuffle
from .player import Player
from .accept_bids import simple_accept
from .bids import simple_bid

# Classes
class Card:
    # Initialize card with a reference to the crypto it belongs to and its value
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name} - ${self.value}"
    

class Game:
    # Initialize the game with the number of players and cryptocurrencies
    # Define methods for simulating a round, checking for a winner, and running the game

    def __init__(self, num_players, starting_cash, cards_per_crypto, winning_cash):
        if num_players < 6:
            self.deck, self.all_cards = create_deck(num_players + 2, cards_per_crypto, 2)
        else:
            self.deck, self.all_cards = create_deck(num_players + 1, cards_per_crypto, 1)
            
        self.players = [
            Player(
                f"Player {i + 1}",
                starting_cash,
                Card(f"Card {i + 1}", i*10),
                200 + round(random() * 50 / 10) * 10, # min_sale
                10 + round(random() * 20 / 10) * 10, # buy_rate
                simple_bid,
                simple_accept,
            ) for i in range(num_players)
        ]
        for player in self.players:
            self.all_cards.append(player.portfolio[0])
        self.winning_cash = winning_cash

    def update_values(self, name, new_value):
        for card in self.all_cards:
            if card.name == name:
                card.value = new_value

    def play_round(self, turn_num):
        if not self.deck:
            return False

        card = self.deck.pop()
        auctioneer = self.players.pop(0)
        
        # get bids from all other players:
        bids = [(player, player.bid(card)) for player in self.players]

        # auctioneer chooses a bid
        chosen_bid = auctioneer.accept_bid(bids, card)
        
        # put actioneer back in player stack, at the end
        self.players.append(auctioneer)
        
        if chosen_bid:
            bidder, (cash_amount, cards_offered) = chosen_bid
            bidder.num_bids_won += 1
            bidder.cash -= cash_amount
            auctioneer.cash += cash_amount
            
            cards_value = sum(card.value for card in cards_offered)

            for card_offered in cards_offered:
                bidder.portfolio.remove(card_offered)
                auctioneer.portfolio.append(card_offered)

            bidder.portfolio.append(card)
            self.update_values(card.name, cash_amount + cards_value)
        else:
            auctioneer.cash -= auctioneer.buy_rate
            auctioneer.portfolio.append(card)
            self.update_values(card.name, auctioneer.buy_rate)

        # all players see if they'd like to sell:
        for player in self.players:
            player.sell_crypto(turn_num)
            
        return True

    def check_winners(self):
        winners = []
        for player in self.players:
            if player.cash >= self.winning_cash:
                winners.append(player)
        return winners
    

# Functions
def create_deck(num_cryptos, cards_per_crypto, extra_cards):
    # Create a shuffled deck of cards with the specified number of cryptocurrencies
    deck = []
    for i in range(cards_per_crypto):
        for j in range(num_cryptos):
            deck.append(Card(f"Card {j + 1}", j*10))
    # Add extra cards for the card types not given to players:
    for i in range(extra_cards):
        deck.append(Card(f"Card {num_cryptos - i}", (num_cryptos - i - 1)*10))
    
    shuffle(deck)
    shuffle(deck)

    return (deck, [card for card in deck])


def play_game(game):
    winners = []
    i = 0
    while game.deck and not winners:
        # play a round:
        i += 1
        game.play_round(i)

        # look for a winner:
        if game.check_winners():
            winners = game.check_winners()
        
    return game, i

def end_game_stats(game, i):
    """Compile end of game stats for multi-game simulations"""
    import math

    tally = []
    for player in game.players:
        tally.append((player.game_end()))

    tally_sorted = sorted(
        tally,
        key=lambda i:i[1], # take the second element of the tupple (their cash)
        reverse=True       # sort by descending order
    )

    N = len(tally_sorted)

    cash_avg = sum(p[1] for p in tally_sorted) / N
    cash_std = math.sqrt(sum((p[1] - cash_avg)**2 for p in tally_sorted) / N)
    if cash_std > 0:
        first_cash = (tally_sorted[0][1] - cash_avg) / cash_std
        last_cash = (tally_sorted[-1][1] - cash_avg) / cash_std
    else:
        first_cash = 0
        last_cash = 0
    
    bids_won_avg = sum(p[7] for p in tally_sorted) / N
    bids_won_std = math.sqrt(sum((p[7] - bids_won_avg)**2 for p in tally_sorted) / N)
    if bids_won_std > 0:
        first_bids = (tally_sorted[0][7] - bids_won_avg) / bids_won_std
        last_bids = (tally_sorted[-1][7] - bids_won_avg) / bids_won_std
    else:
        first_bids = 0
        last_bids = 0

    cards_sold_avg = sum(len(p[2]) for p in tally_sorted) / N
    cards_sold_std = math.sqrt(sum((len(p[2]) - cards_sold_avg)**2 for p in tally_sorted) / N)
    if cards_sold_std > 0:
        first_cards = (len(tally_sorted[0][2]) - cards_sold_avg) / cards_sold_std
        last_cards = (len(tally_sorted[-1][2]) - cards_sold_avg) / cards_sold_std
    else:
        first_cards = 0 
        last_cards = 0 

    cards_sold_GE_avg = sum(len(p[3]) for p in tally_sorted) / N
    cards_sold_GE_std = math.sqrt(sum((len(p[3]) - cards_sold_GE_avg)**2 for p in tally_sorted) / N)
    if cards_sold_GE_std > 0:
        first_end = (len(tally_sorted[0][3]) - cards_sold_GE_avg) / cards_sold_GE_std
        last_end = (len(tally_sorted[-1][3]) - cards_sold_GE_avg) / cards_sold_GE_std
    else:
        first_end = 0
        last_end = 0

    results = {
        "LOG": i,
        "1st pos": int(tally_sorted[0][0][7]),
        "Last pos": int(tally_sorted[-1][0][7]),

        "Cash AVG": cash_avg,
        "Cash STD": cash_std,
        "1st cash STD": first_cash,
        "Last cash STD": last_cash,

        "Bids won AVG": bids_won_avg,
        "Bids won STD": bids_won_std,
        "1st bids won STD": first_bids,
        "Last bids won STD": last_bids,

        "Cards sold AVG": cards_sold_avg,
        "Cards sold STD": cards_sold_std,
        "1st cards sold STD": first_cards,
        "Last cards sold STD": last_cards,

        "Cards sold GE AVG": cards_sold_GE_avg,
        "Cards sold GE STD": cards_sold_GE_std,
        "1st cards sold GE STD": first_end,
        "Last cards sold GE STD": last_end,
    }

    return results

def print_game(game, i):
    print(f"Game complete in {i} turns! \n")
    
    print("Final standings:")
    tally = []
    for player in game.players:
        tally.append((player.game_end()))

    tally_ordered = sorted(
        tally,
        key=lambda i:i[1], # take the second element of the tupple (their cash)
        reverse=True       # sort by descending order
    )
    for player in tally_ordered:
        print(player[0])
        print(f"Minimum sale value: ${player[5]}")
        print(f"Buy from bank threshold: ${player[6]}")
        print(f"Number of bids won: {player[7]}")
        print(f"Crypto Sold during the game: {[(turn, card.__str__()) for turn, card in player[2]]}")
        print(f"Crypto Sold at the end of the game: {[card.__str__() for card in player[3]]}")
        print(f"Remaining portfolio: {[card.__str__() for card in player[4]]} \n")
