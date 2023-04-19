"""play game object"""

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
    

class PlayGame:
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
        
        rand_int = int(random()*num_players)
        self.player_bots = [player for player in self.players if player != self.players[rand_int]]
        self.human_player = self.players[rand_int]

    def update_values(self, name, new_value):
        for card in self.all_cards:
            if card.name == name:
                card.value = new_value

    def display_turn_state(self, auctioneer, card):
        card_state = set([(card.name, f"${card.value}") for card in self.all_cards])
        print("""

        





Current Card Values:
""")
        for c in card_state:
            print(f"    {c[0]}: {c[1]}")

        print(f"""        
Your cash: {self.human_player.cash}
Your portfolio: {[card.name for card in self.human_player.portfolio]}

""")

        if auctioneer:
            print(f"Turn's Auctioneer: {auctioneer.name}")
            print(f"Flipped Card: {card.name}")
        print("")
        
    def play_round(self, turn_num):
        if not self.deck:
            return False

        card = self.deck.pop()
        auctioneer = self.players.pop(0)

        self.display_turn_state(auctioneer, card)

        # get bids from other bots:
        bids = [(player, player.bid(card)) for player in self.player_bots if player != auctioneer]

        # if auctioneer is a bot, get player's bet:
        if auctioneer in self.player_bots:
            confirmation = False
            while confirmation != True:
                player_cash_bid = input("How, much cash are you betting?: ")
                if player_cash_bid:
                    player_cash_bid = int(player_cash_bid)
                else:
                    player_cash_bid = 0
                cards_bid = input("Which cards are you betting? (list of index seperated by space): ")
                player_cards_bid = []
                if cards_bid:
                    cards_bid = [int(ind) for ind in cards_bid.split()]
                    for c in cards_bid:
                        player_cards_bid.append(self.human_player.portfolio[c])
                    
                confirmation = bool(input(f"""
                    Please confirm your bid (blank for false):
                        ${player_cash_bid},
                        Cards: {[c.name for c in player_cards_bid]}
                """))
            bids.append((self.human_player, (player_cash_bid, player_cards_bid)))

            # auctioneer chooses a bid
            chosen_bid = auctioneer.accept_bid(bids, card)
            if chosen_bid:
                print(f"\n Chosen bidder: {chosen_bid[0].name}, for ${chosen_bid[1][0]} and {[c.name for c in chosen_bid[1][1]]} cards")
            else:
                print(f"\n Auctioneer buys the card for: ${auctioneer.buy_rate}")
        # Otherwise, human is the auctioneer!
        else:
            print("Players have bid the following...") 
            for bid in bids:
                print(f"{bid[0].name}: ${bid[1][0]} & {[c.name for c in bid[1][1]]}")
            select_bidder = input("Would you like to select a bid? (Blank for fals): ")
            if select_bidder:
                bidder_selected = False
                while bidder_selected != True:
                    chosen_bid = int(input("Which bid would you like to select?: "))
                    if chosen_bid:
                        chosen_bid = bids[chosen_bid]
                        bidder_selected = bool(input(f"Is this the correct bid you wanted: {chosen_bid[0].name}?: "))
            else:
                chosen_bid = None

        if chosen_bid:
            bidder, (cash_amount, cards_offered) = chosen_bid
            bidder.num_bids_won += 1
            bidder.cash -= cash_amount
            auctioneer.cash += cash_amount
            
            cards_value = sum(c.value for c in cards_offered)

            for card_offered in cards_offered:
                bidder.portfolio.remove(card_offered)
                auctioneer.portfolio.append(card_offered)

            bidder.portfolio.append(card)
            self.update_values(card.name, cash_amount + cards_value)
        else:
            auctioneer.cash -= auctioneer.buy_rate
            auctioneer.portfolio.append(card)
            self.update_values(card.name, auctioneer.buy_rate)


        # put actioneer back in player stack, at the end
        self.players.append(auctioneer)

        # all players see if they'd like to sell:
        for player in self.player_bots:
            sold_len = len(player.crypto_sold)
            player.sell_crypto(turn_num)
            for new_sold in player.crypto_sold[sold_len:]:
                print(f"Player {player.name} sold {new_sold[1].name}!")
        
        # See if human would like to sell anything?
        display_turn_state(None, None)
        print(f"Your cash: {self.human_player.cash}")
        print(f"Your portfolio: {[c.name for c in self.human_player.portfolio]} \n")
        wants_to_sell = bool(input("Would you like to sell anything? (blank for no)"))
        while wants_to_sell == True:
            card_to_sell = int(input("What card would you like to sell?"))
            confirmation = bool(input(f"Is this the correct card {self.human_player.portfolio[card_to_sell].name}?"))
            if confirmation:
                card_to_sell = self.human_player.portfolio[card_to_sell]
                self.human_player.cash += card_to_sell.value
                self.human_player.portfolio.remove(card_to_sell)
                self.human_player.crypto_sold.append((turn_num, card_to_sell))
                wants_to_sell = bool(input("Do you want to sell another card? (blank for no)?"))
            
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

