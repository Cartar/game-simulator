
def simple_accept(bids, card, buy_rate):
    # If multiple cards in an offer, take that offer:
    if len(max(bids, key=lambda bid: len(bid[1][1]))[1][1]) > 1:
        highest_bid = max(bids, key=lambda bid: len(bid[1][1]))
    # If all offers have single cards, take highest cash offer: 
    else:
        highest_bid = max(bids, key=lambda bid: bid[1][0])
    
    # determine if highest bid is greater than the buy_rate
    cards_value = sum(card.value for card in highest_bid[1][1])
    if (highest_bid[1][0] + cards_value) <= buy_rate:
        return None
    
    return highest_bid
