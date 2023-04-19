import pytest

from src import simple_accept, Card, Player

CARDS = {
    "C1": Card("C1", 10),
    "C2": Card("C2", 20),
    "C3": Card("C3", 30),
    "C4": Card("C4", 40),
    "C5": Card("C5", 50),
    "C6": Card("C6", 60),
}

PLAYERS = {
    "P1": Player("P1", 100, CARDS["C1"], 200, 30),
    "P2": Player("P2", 100, CARDS["C2"], 200, 30),
    "P3": Player("P3", 100, CARDS["C3"], 200, 30),
    "P4": Player("P4", 100, CARDS["C4"], 200, 30),
    "P5": Player("P5", 100, CARDS["C5"], 200, 30),
    "P6": Player("P6", 100, CARDS["C6"], 200, 30),
}


def test_simple_accept1():
    mock_bids_single_card = [
        (PLAYERS["P1"], (40, [CARDS["C1"]])), # 50
        (PLAYERS["P2"], (20, [CARDS["C6"]])), # 80
        (PLAYERS["P3"], (30, [CARDS["C3"]])), # 60
    ]
    highest_bid = simple_accept(mock_bids_single_card, None, 0)
    assert highest_bid[0] == PLAYERS["P2"]

def test_simple_accept2():
    mock_bids_multi_card = [
        (PLAYERS["P1"], (40, [CARDS["C1"]])), # 50
        (PLAYERS["P2"], (20, [CARDS["C6"], CARDS["C3"]])), # 110
        (PLAYERS["P3"], (30, [CARDS["C3"], CARDS["C6"]])), # 120
    ]
    highest_bid = simple_accept(mock_bids_multi_card, None, 0)
    assert highest_bid[0] == PLAYERS["P3"]

