import sys
sys.path.insert(0, r'C:\Users\test0\OneDrive\שולחן העבודה\checkers\web\checkers_game')

from checkers_logic import Game

INT_MIN = -sys.maxsize - 1
INT_MAX = sys.maxsize

class Bot:
    def __init__(self, game: Game) -> None:
        self.game = game.__copy__()

    def get_minimax_move(self, depth: int, is_max_player: bool):
        moves = self.game.get_all_moves()
        best_move = INT_MIN
        best_move_found = moves[0]

        for move in moves:
            game_copy = self.game.__copy__()
            game_copy.make_move(move, notations=False)
            val = self.minimax(game_copy, depth - 1, INT_MIN, INT_MAX, not is_max_player) # evaluate the position after the move has been made
            if val >= best_move:
                best_move = val
                best_move_found = move
        print(best_move)
        print(best_move_found)
        move = self.game.convert_indices_to_position(best_move_found[0]) + '-' + self.game.convert_indices_to_position(best_move_found[1])
        print(move)
        return move

    def minimax(self, game: Game, depth: int, a: int, b: int, is_max_player: bool):
        if depth == 0 or game.is_game_over():
            return game.evaluate()
        
        moves = game.get_all_moves()

        if is_max_player:
            best_move = INT_MIN

            for move in moves:
                game_copy = game.__copy__()
                game_copy.make_move(move, notations=False)

                best_move = max(best_move, self.minimax(game_copy, depth - 1, a, b, not is_max_player))

                # a = max(a, best_move)

                # if b <= a:
                #     return best_move
                
            return best_move
        else:
            best_move = INT_MAX

            for move in moves:
                game_copy = game.__copy__()
                game_copy.make_move(move, notations=False)

                best_move = min(best_move, self.minimax(game_copy, depth - 1, a, b, not is_max_player))

                # a = min(a, best_move)

                # if b <= a:
                #     return best_move
                
            return best_move