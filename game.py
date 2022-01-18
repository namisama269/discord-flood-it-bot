from board import Board
from colors import *

BOARD_SIZE = 14

class Game:
    def __init__(self, num_moves_allowed, unused_colors):
        self.colors = [color for color in COLORS if color not in unused_colors]
        self.board = Board(BOARD_SIZE, len(self.colors))
        self.num_moves_used = 0
        self.num_moves_allowed = num_moves_allowed

    def make_move(self, val):
        did_use_move = self.board.update(val)
        if did_use_move:
            self.num_moves_used += 1

    def content(self):
        out_str = ""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                out_str += EMOJI_NAMES[self.colors[self.board.vals[i][j]]]
            out_str += "\n"
        return out_str

    def title(self):
        if self.num_moves_used > self.num_moves_allowed:
            return "You Lose!"
        elif self.board.is_uniform():
            return "You Win!"
        else:
            return f"Moves used: {self.num_moves_used}/{self.num_moves_allowed}"
    
    def get_reaction_emojis(self):
        return [EMOJIS[color] for color in self.colors]