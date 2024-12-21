from Board import Board, Move

class Game:
    def __init__(self) -> None:
        self.current_player = Board.WHITE
        self._board = Board()
        self.continue_capture = False
    
    def _switch_player(self):
        if not self.continue_capture:  # Only switch players if no further captures are possible
            self.current_player = Board.BLACK if self.current_player == Board.WHITE else Board.WHITE

    def is_valid_select(self, row, col):
        return self._board.get_square(row, col) is not None and self._board.get_square(row, col) == self.current_player 

    def is_game_over(self):
        return not any(self._board.has_any_valid_move(player) for player in (Board.WHITE, Board.BLACK))

    def get_winner(self):
        if self.is_game_over():
            # Determine winner based on piece count 
            white_pieces = sum(row.count(Board.WHITE) for row in self._board._board)
            black_pieces = sum(row.count(Board.BLACK) for row in self._board._board)
            return Board.WHITE if white_pieces > black_pieces else Board.BLACK
        return None

    def _play_turn(self):
        self._board.print_board()
        print(f"Player {self.current_player}'s turn")

        while True:
            src_row = int(input("Enter source row: "))
            src_col = int(input("Enter source column: "))
            dst_row = int(input("Enter destination row: "))
            dst_col = int(input("Enter destination column: "))

            if self._board.is_valid_move(self.current_player, (src_row, src_col), (dst_row, dst_col)):
                self._board.make_move((src_row, src_col), (dst_row, dst_col))

                self.continue_capture = self._board.has_capture_move(self.current_player, (dst_row, dst_col))
                if not self.continue_capture:
                    self._switch_player()
                break
            else:
                print("Invalid move. Try again.")

    def play_turn(self, move: Move):
        # Attempt to make a move
        if self._board.is_valid_move(self.current_player, move):
            is_move_capture = self._board._is_capture_move(self.current_player, move)
            self.continue_capture = self._board.has_capture_move(self.current_player, (move.dst_row, move.dst_col)) and is_move_capture
            self._board.make_move(move)
            if not self.continue_capture:
                self._switch_player()
        else:
            print("Invalid move. Try again.")


    def run(self):
        while not self.is_game_over():
            self._play_turn()

        winner = self.get_winner()
        if winner:
            print(f"Player {winner} wins!")
        else:
            print("It's a draw!")
