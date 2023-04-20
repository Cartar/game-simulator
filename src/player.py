import random

from .accept_bids import simple_accept
from .bids import simple_bid

class Player:
    """
    The bid method places a random bid between 0 and the player's available cash,
    up to the card's value. This method does not offer any cards from the player's
    portfolio in the bid, but you can modify it to include cards based on your preferred strategy.
    
    The accept_bid method selects the highest cash bid.
    If there are no bids with cash, it returns None. You can modify this method to
    consider bids with cards or implement other acceptance strategies.

    The sell_crypto method sells the card with the highest value in the player's portfolio.
    This method does not implement any selling restrictions, such as only allowing players
    to sell once during the game. You can add these restrictions or other selling strategies as needed.
    """
    def __init__(self, name, starting_cash, first_card, min_sale, buy_rate, bid_strat=simple_bid, accept_strat=simple_accept):
        # Define methods for bidding, accepting bids, and selling cryptocurrencies
        self.name = name
        self.cash = starting_cash
        self.portfolio = [first_card]
        self.bid_strat = bid_strat
        self.accept_strat = accept_strat
        self.min_sale = min_sale
        self.buy_rate = buy_rate
        self.crypto_sold = []
        self.end_sold = []
        self.num_bids_won = 0

    def bid(self, card):
        # Return a tuple with the cash amount and a list of cards offered in the bid
        return self.bid_strat(card, self.cash, self.portfolio)

    def accept_bid(self, bids, card):
        # Return the chosen bid
        return self.accept_strat(bids, card, self.buy_rate)

    def sell_crypto(self, turn_num):
        # Update the player's cash and portfolio if there is anything to sell:
        max_sold_num = max_sold_math(len(self.portfolio))
        card_to_sell = max(self.portfolio, key=lambda card: card.value)
        sold = False

        while card_to_sell and max_sold_num > 0:
            if card_to_sell.value > self.min_sale:
                self.cash += card_to_sell.value
                self.portfolio.remove(card_to_sell)
                self.crypto_sold.append((turn_num, card_to_sell))
                # decrease max_sold_num and find new card:
                max_sold_num -= 1
                card_to_sell = max(self.portfolio, key=lambda card: card.value)
                sold = True
            else:
                card_to_sell = None

        return sold
    
    def game_end(self):
        # When someone wins, sum all crypto that could be sold
        # Determine max number of cards that could be sold:
        max_sold_num = max_sold_math(len(self.portfolio))
        card_to_sell = max(self.portfolio, key=lambda card: card.value)

        while card_to_sell and max_sold_num > 0:
            self.cash += card_to_sell.value
            self.portfolio.remove(card_to_sell)
            self.end_sold.append(card_to_sell)
            # decrease max_sold_num and find new card:
            max_sold_num -= 1
            card_to_sell = max(self.portfolio, key=lambda card: card.value)
         
        return (
            self.__str__(),
            self.cash,
            [(turn, card) for turn, card in self.crypto_sold],
            [card for card in self.end_sold],
            [card for card in self.portfolio],
            self.min_sale,
            self.buy_rate,
            self.num_bids_won,
        )
        
    def __str__(self):
        return f"{self.name} - Cash: ${self.cash}, Portfolio Value: ${sum(card.value for card in self.portfolio)}"

def max_sold_math(l):
    import math
    return math.ceil(l/2-1)