
def simple_accept(bids, card, buy_rate):
    # If multiple cards in an offer, take offer with highest value:
    if len(max(bids, key=lambda bid: len(bid[1][1]))[1][1]) > 1:
        max_len = len(max(bids, key=lambda bid: len(bid[1][1]))[1][1])
        highest_bid = max(
            [bid for bid in bids if len(bid[1][1])==max_len],
            key=lambda bid: (sum(b.value for b in bid[1][1]) + bid[1][0])
        )
    # Otherwise, take highest bid!
    else:
        highest_bid = max(
            bids,
            key=lambda bid: (sum(b.value for b in bid[1][1]) + bid[1][0])
        )
    
    # determine if highest bid is greater than the buy_rate
    if (
        highest_bid[1][0] + sum(c.value for c in highest_bid[1][1])
    ) <= buy_rate:
        return None
    
    return highest_bid
