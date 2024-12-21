from math import ceil

class Move:
    def __init__(self, src: tuple[int], dst: tuple[int]) -> None:
        self.src_row, self.src_col = src
        self.dst_row, self.dst_col = dst

class Board:
    BOARD_LENGTH = 8
    WHITE = 1
    BLACK = 0
    WHITE_QUEEN = 3
    BLACK_QUEEN = 2

    def __init__(self) -> None:
        self._board = [[None] * self.BOARD_LENGTH for _ in range(self.BOARD_LENGTH)]
        self._initialize_figures()
    
    def _initialize_figures(self):
        for i in range(self.BOARD_LENGTH):
            for j in range(self.BOARD_LENGTH):
                if i < (self.BOARD_LENGTH - 2) // 2:
                    if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0): # diag check
                        self._board[i][j] = self.WHITE
                elif i >= ((self.BOARD_LENGTH - 2) // 2) + 2:
                    if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0): # diag check
                        self._board[i][j] = self.BLACK

    def make_move(self, move: Move):
        if self._board[move.src_row][move.src_col] == self.BLACK:
            self._board[move.dst_row][move.dst_col] = self.BLACK if move.dst_row != 0 else self.BLACK_QUEEN
        else:
            self._board[move.dst_row][move.dst_col] = self.WHITE if move.dst_row != self.BOARD_LENGTH - 1 else self.WHITE_QUEEN
        
        self._board[move.src_row][move.src_col] = None

        row_diff = move.dst_row - move.src_row
        if abs(row_diff) == 2:
            # Calculate the position of the captured piece
            capture_row = (move.src_row + move.dst_row) // 2
            capture_col = (move.src_col + move.dst_col) // 2

            self._board[capture_row][capture_col] = None


    def is_valid_move(self, current_player: int, move: Move):
        # Check if the source and destination indices are valid
        if not (0 <= move.src_row < self.BOARD_LENGTH and 0 <= move.src_col < self.BOARD_LENGTH and
                0 <= move.dst_row < self.BOARD_LENGTH and 0 <= move.dst_col < self.BOARD_LENGTH):
            return False

        # Check if the source square contains the player's piece
        if self._board[move.src_row][move.src_col] is None or self._board[move.src_row][move.src_col] != current_player:
            return False

        # Calculate the direction of the move
        row_diff = move.dst_row - move.src_row
        col_diff = move.dst_col - move.src_col

        # Check if the move is diagonal and in the correct direction
        if abs(row_diff) != abs(col_diff):
            return False

        # Check for single-step moves
        if abs(row_diff) == 1:
            # Ensure the destination square is empty
            if self._board[move.dst_row][move.dst_col] is not None:
                return False
            return True

        # Check for captures
        if abs(row_diff) == 2: 
            # Calculate the position of the captured piece
            capture_row = (move.src_row + move.dst_row) // 2
            capture_col = (move.src_col + move.dst_col) // 2

            # Ensure the captured piece is the opponent's and the destination square is empty
            if self._board[capture_row][capture_col] is None or self._board[capture_row][capture_col] == current_player:
                return False
            if self._board[move.dst_row][move.dst_col] is not None:
                return False

            return True

        return False
    
    def _is_capture_move(self, current_player: int, move: Move):
        if abs(move.dst_row - move.src_row) != 2 or abs(move.dst_col - move.src_col) != 2:
            return False

        capture_row = (move.src_row + move.dst_row) // 2
        capture_col = (move.src_col + move.dst_col) // 2
        return (self._board[capture_row][capture_col] is not None and
                self._board[capture_row][capture_col] != current_player and
                self._board[move.dst_row][move.dst_col] is None)
    
    def has_capture_move(self, player: int, position: tuple[int, int]) -> bool:
        # Check all potential capture directions for additional captures
        row, col = position
        for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.BOARD_LENGTH and 0 <= new_col < self.BOARD_LENGTH and
                self._is_capture_move(player, Move(position, (new_row, new_col)))):
                return True
        return False
    
    def has_any_valid_move(self, player: int) -> bool:
        # Check if there are any valid moves for the player
        for row in range(self.BOARD_LENGTH):
            for col in range(self.BOARD_LENGTH):
                if self._board[row][col] == player:
                    for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        if self.is_valid_move(player, Move((row, col), (row + dr, col + dc))):
                            return True
        return False
    
    def get_square(self, row, col):
        return self._board[row][col]

    def print_board(self):
        for row in self._board:
            print("|", end="")
            print("|".join(str(col) if col is not None else " " for col in row), end="|\n")
                