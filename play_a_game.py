"""Play a game from the terminal
"""
from src import PlayGame

if __name__ == "__main__":

    # Get user input from the terminal
    number_of_players = int(input("Enter the number of players: "))

    game = PlayGame(
        num_players = number_of_players,
        starting_cash = 100,
        cards_per_crypto = 6, # doesn't include the one given to players!
        winning_cash = 1000
    )

    print(f"You are player: {game.human_player.name}")
    
    winners = []
    i = 0
    while game.deck and not winners:
        # play a round:
        i += 1
        game.play_round(i)

        # look for a winner:
        if game.check_winners():
            winners = game.check_winners()
    
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

