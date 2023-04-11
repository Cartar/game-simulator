from random import random, shuffle
from player import Player
from accept_bids import simple_accept
from bids import simple_bid

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
        self.deck, self.all_cards = create_deck(num_players + 1, cards_per_crypto)
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

    def play_round(self):
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
            player.sell_crypto()
            
        return True

    def check_winners(self):
        winners = []
        for player in self.players:
            if player.cash >= self.winning_cash:
                winners.append(player)
        return winners
    

# Functions
def create_deck(num_cryptos, cards_per_crypto):
    # Create a shuffled deck of cards with the specified number of cryptocurrencies
    deck = []
    for i in range(cards_per_crypto):
        for j in range(num_cryptos):
            deck.append(Card(f"Card {j + 1}", j*10))
    
    shuffle(deck)
    shuffle(deck)

    return (deck, [card for card in deck])


def play_game(game):
    winners = []
    while game.deck and not winners:
        # play a round:
        game.play_round()

        # look for a winner:
        if game.check_winners():
            winners = game.check_winners()
        
    print(f"Game complete!")
    print("Final standings:")
    for player in game.players:
        print(player)
    
    return game
