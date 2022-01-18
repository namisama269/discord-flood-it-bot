import random

def generate_random_board(size, num_colors):
    vals = [[None] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            vals[i][j] = random.randint(0, num_colors-1)
    return vals


def floodfill(board, i, j, target, replacement):
    # out of bounds
    if i < 0 or j < 0 or i >= board.size or j >= board.size:
        return
    # check that square has target color
    if board.vals[i][j] != target:
        return
    # flood fill
    board.vals[i][j] = replacement
    floodfill(board, i+1, j, target, replacement)
    floodfill(board, i-1, j, target, replacement)
    floodfill(board, i, j+1, target, replacement)
    floodfill(board, i, j-1, target, replacement)


class Board:
    def __init__(self, size, num_colors):
        self.vals = generate_random_board(size, num_colors)
        self.size = size
        self.num_colors = num_colors
        
    def update(self, val):
        # if same color as top left already then do nothing
        if self.vals[0][0] == val:
            return False
        # update the board after flood filling top left corner value
        floodfill(self, 0, 0, self.vals[0][0], val)
        return True

    def is_uniform(self):
        val = self.vals[0][0]
        for i in range(self.size):
            for j in range(self.size):
                if self.vals[i][j] != val:
                    return False
        return True
