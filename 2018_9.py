def marble_game(players, marbles):
    circle = [0]
    player = 0
    scores = [0 for i in range(players)]
    current_marble = 0
    for i in range(1, marbles+1):
        marble_score = i
        if marble_score % 23 != 0:
            mod = len(circle)
            placement = ((current_marble + 1) % mod) + 1
            if placement > mod - 1:
                circle.append(marble_score)
            else:
                circle.insert(placement, marble_score)
            current_marble = placement
        else:
            mod = len(circle)
            scores[player] += marble_score
            removing = (current_marble - 7) % mod
            scores[player] += circle[removing]
            circle.pop(removing)
            current_marble = removing
        # print('Player:', player, 'Circle:', circle)
        player = (player + 1) % players
    return scores


scores = marble_game(452, 71250)
print('Highest score:', max(scores))
print('Winner: Player', scores.index(max(scores)))


class Marble:
    def __init__(self, val):
        self.val = val
        self.right = None
        self.left = None

    def get_right(self, amount):
        if amount == 1:
            return self.right
        else:
            return self.right.get_right(amount-1)

    def get_left(self, amount):
        if amount == 1:
            return self.left
        else:
            return self.left.get_left(amount-1)

    def remove(self):
        self.right.left = self.left
        self.left.right = self.right

    def insert_right(self, val):
        new_marble = Marble(val)
        new_marble.right = self.right
        new_marble.left = self
        self.right.left = new_marble
        self.right = new_marble

    def insert_left(self, val):
        new_marble = Marble(val)
        new_marble.left = self.left
        new_marble.right = self
        self.left.right = new_marble
        self.left = new_marble


def marble_game_fast(players, marbles):
    player = 0
    scores = [0 for i in range(players)]
    current_marble = Marble(0)
    current_marble.left = current_marble
    current_marble.right = current_marble
    for i in range(1, marbles+1):
        if i % 23 != 0:
            current_marble.right.insert_right(i)
            current_marble = current_marble.get_right(2)
        else:
            scores[player] += i
            marble_remove = current_marble.get_left(7)
            scores[player] += marble_remove.val
            current_marble = marble_remove.right
            marble_remove.remove()
        player = (player + 1) % players
    return scores


scores = marble_game_fast(452, 7125000)
print('Highest score:', max(scores))
print('Winner: Player', scores.index(max(scores)))
