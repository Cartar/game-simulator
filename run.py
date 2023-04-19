import pandas as pd

from src import Game, play_game, end_game_stats

if __name__ == "__main__":

    # Get user input from the terminal
    number_of_players = int(input("Enter the number of players: "))
    cards_per_crypto = int(input("Enter the number of cards per crypto: "))
    number_of_plays = int(input("Enter the number of play throughs: "))
    file_name = str(input("Enter the file name of this simulation: "))

    output = pd.DataFrame()

    for i in range(number_of_plays):
        game = Game(
            num_players = number_of_players,
            starting_cash = 100,
            cards_per_crypto = cards_per_crypto, # doesn't include the one given to players!
            winning_cash = 1000
        )
        game, n = play_game(game)
        results = end_game_stats(game, n)

        df_dictionary = pd.DataFrame([results])
        output = pd.concat([output, df_dictionary], ignore_index=True)

    output.to_csv(
        f"{file_name}_playerN-{number_of_players}_CryptoCardN-{cards_per_crypto}_results.csv",
        sep=',',
        index=True
    )
    output.describe().to_csv(
        f"{file_name}_playerN-{number_of_players}_CryptoCardN-{cards_per_crypto}_desc.csv",
        sep=',',
        index=True
    )
