# A = Ace
# J = Jack
# Q = Queen
# K = King
# 1-10 = 1-10
# D = Diamonds
# H = Heart
# S = Spades
# C = Clubs

a=input().upper()

rank = a[:-1]
suit = a[-1]

print(rank)
print(suit)

def rank_s(rank_val):
    if rank_val == "A":
        return "Ace"
    elif rank_val == "J":
        return "Jack"
    elif rank_val == "K":
        return "King"
    elif rank_val == "Q":
        return "Queen"
    else:
        return rank_val

def suit_s(suit_val):
    if suit_val == "D":
        return "Diamonds"
    elif suit_val == "H":
        return "Hearts"
    elif suit_val == "S":
        return "Spades"
    elif suit_val == "C":
        return "Clubs"

print(f"{rank_s(rank)} of {suit_s(suit)}")