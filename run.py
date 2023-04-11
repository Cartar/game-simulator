from src import Game, play_game

if __name__ == "__main__":

    game = Game(
        num_players = 5,
        starting_cash = 100,
        cards_per_crypto = 6,
        winning_cash = 1000
    )

    play_game(game)
