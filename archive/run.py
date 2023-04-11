from src import create_game, play_a_turn

if __name__ == "__main__":
    players, deck = create_game()

    history = []
    auctioneer = 0
    
    for top_card in deck:
        history.append(
            play_a_turn(
                players(auctioneer),
                [i for i in players if i != auctioneer],
                top_card
            )
        )
    
    # save history:
    with open(r'history.txt', 'w') as fp:
        for item in history:
            fp.write("%s\n" % item)
    
    print('Done')
