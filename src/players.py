import random
from math import ceil, floor

class player:
    def __init__(
        self,
        max_cash_utilization,
        max_crypto_utilization,
        less_max_crypto_threshold,
        starting_card
    ):
        self.max_cash_utilization = max_cash_utilization # Used in cash bid to know how much cash is OK to give
        self.max_crypto_utilization = max_crypto_utilization # Used in crypto bid to know how many cards are OK to be sold
        self.less_max_crypto_threshold = less_max_crypto_threshold # Used in crypto bid to know if a card is OK to be sold

        self.cash = 100
        self.crypto = {
            "C1": 0,
            "C2": 0,
            "C3": 0,
            "C4": 0,
            "C5": 0,
            "C6": 0,
            "B": 0,
        }
        self.crypto[starting_card] = 1
        self.last_swing_played = None # The last swing (50% up or down) card played

    def cash_bid(self, current_bet=0):
        if current_bet >= self.max_cash_utilization:
            return None
        bet = ceil((random.random() * self.cash * self.max_cash_utilization) / 5)
        if bet > current_bet:
            return bet
        else:
            return None
    
    def crypto_bid(self, flip, values):
        number_of_cards = 0
        eligible_cards = []
        eligible_values = []
        card_value_threshold = 5 * floor(
            self.less_max_crypto_threshold * sum(values.values())/len(values.values())
        / 5 )
        
        for card, quantity in self.crypto.items():
            if card != flip and values[card] >= card_value_threshold:
                for i in range(quantity):
                    eligible_cards.append(card)
                    eligible_values.append(values[card])
                
        # Now need to determine all possible bets, order them, eliminate plays above max_crypto_threshold, and return actual cyrpto bet
        return None

    def bid(self, flip, current_bet):
        """returns a tuple of (bet, cash amount, crypto amount, crypto cards)"""
        c_bid, cards = self.crypto_bid(flip)
        if c_bid > current_bet:
            return c_bid, 0, c_bid, cards
        elif c_bid + self.cash * self.max_cash_utilization > current_bet:
            cash = self.cash_bid(current_bet - c_bid)
            if cash + c_bid > current_bet:
                return cash + c_bid, cash, c_bid, cards
        else:
            return 0, 0, 0, []
