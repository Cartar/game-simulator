from collections import Counter
from random import random

def nearest_10(cash, max_pct):
    return round(random() * cash * max_pct / 10) * 10

def simple_bid(card, my_cash, my_cards):
    my_card_names = [my_card.name for my_card in my_cards]
    counted = Counter(my_card_names)
    eligible_cards = sorted([my_card for my_card in my_cards if my_card.name != card.name], key=lambda i: i.value)
    
    # Cap amount of cash up for grabs
    if my_cash > 150:
        eligible_cash = 150
    else:
        eligible_cash = my_cash

    cards_offered = []
    cash_offer = 0

    # If already owning multiple cards of this card, go hard -> bidding multiple other cards + up to 50% cash
    if card.name in my_card_names and card.name == counted.most_common(1)[0][0]:
        # Bid your top X cards, were X is the number of cards already owned!
        x = counted.most_common(1)[0][1]
        for i in range(x):
            if eligible_cards:
                cards_offered.append(eligible_cards.pop())
        cash_offer = nearest_10(eligible_cash, 0.5)

    else:
        # If card's name exists in my_cards, up to 30% cash, and highest other card
        if card.name in my_card_names:
            if eligible_cards:
                cards_offered.append(eligible_cards[0])
            cash_offer = nearest_10(eligible_cash, 0.5)

        # If card is new, and we have more than 2 cards, bid with second highest card:
        elif len(eligible_cards) > 2:
            cards_offered.append(eligible_cards[1])
        
        # If we don't have many cards, simply offer up to 40% cash
        else:
            cash_offer = nearest_10(eligible_cash, 0.4)
        
    return (cash_offer, cards_offered)

