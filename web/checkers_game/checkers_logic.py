import copy

class Game:
    BOARD_LENGTH = 8
    WHITE = 1
    BLACK = 0
    WHITE_QUEEN = 3
    BLACK_QUEEN = 2

    def __init__(self):
        self.board = self.initializeboard()
        self.current_turn = 1
        self.continue_capture = False

    def __copy__(self):
        return copy.deepcopy(self)
    
    def initializeboard(self):
        board = [[None for _ in range(self.BOARD_LENGTH)] for _ in range(8)]
        
        for row in range(self.BOARD_LENGTH):
            for col in range(self.BOARD_LENGTH):
                if row < (self.BOARD_LENGTH - 2) // 2:
                    if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0): # diag check
                        board[row][col] = self.WHITE
                elif row >= ((self.BOARD_LENGTH - 2) // 2) + 2:
                    if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0): # diag check
                        board[row][col] = self.BLACK
        return board

    def serialize(self):
        return {
            'board': self.board,
            'current_turn': self.current_turn,
            'continue_capture': self.continue_capture
        }

    @staticmethod
    def deserialize(game_state):
        game = Game()
        game.board = game_state['board']
        game.current_turn = game_state['current_turn']
        game.continue_capture = game_state['continue_capture']
        return game
    
    def play(self, move, error):
        error = 1

    def is_valid_move(self, position: tuple[int], dst: tuple[int], player=None):
        if player == None:
            player = self.current_turn

        start_row, start_col = position
        end_row, end_col = dst

        is_queen = False

        # Check if the source and destination indices are valid
        if not (0 <= start_row < self.BOARD_LENGTH and 0 <= start_col < self.BOARD_LENGTH and
                0 <= end_row < self.BOARD_LENGTH and 0 <= end_col < self.BOARD_LENGTH):
            return False

        # Check if the source square contains the player's queen
        queen = self.WHITE_QUEEN if self.current_turn is self.WHITE else self.BLACK_QUEEN
        if self.board[start_row][start_col] is queen:
            is_queen = True
        else:
            # Check if the source square contains the player's piece
            if self.board[start_row][start_col] is None or self.board[start_row][start_col] != player:
                return False

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        # Check if the move is diagonal
        if abs(row_diff) != abs(col_diff):
            return False

        # Check for single-step moves
        if abs(row_diff) == 1:
            # Ensure the destination square is empty
            if self.board[end_row][end_col] is not None:
                return False
            if self.continue_capture:
                return False
            return True

        if is_queen:
            # Check for captures in the diagonal and make sure the queen lands after one square after a capture
            current_row, current_col = start_row, start_col
            capture = False

            # Check every diagonal square in the direction
            for _ in range(abs(row_diff) - 1):
                current_row = current_row - 1 if row_diff < 0 else current_row + 1
                current_col = current_col - 1 if col_diff < 0 else current_col + 1

                if self.board[current_row][current_col] is not None:
                    if self.board[current_row][current_col] is self.current_turn:
                        return False # Can't go over your own pieces
                    if capture:
                        return False # can't go over 2 pieces in a row
                    else:
                        capture = True
                else:
                    capture = False
            
            # Check the last square
            if self.board[end_row][end_col] is not None:
                return False
            return True
        else:
        # Check for captures regularly 
            if abs(row_diff) == 2: 
                # Calculate the position of the captured piece
                capture_row = (start_row + end_row) // 2
                capture_col = (start_col + end_col) // 2

                queen_capture = self.WHITE_QUEEN if player is self.WHITE else self.BLACK_QUEEN # Player can't capture it's own queen

                # Ensure the captured piece is the opponent's and the destination square is empty
                if self.board[capture_row][capture_col] is None or self.board[capture_row][capture_col] == player or self.board[capture_row][capture_col] == queen_capture: 
                    return False
                if self.board[end_row][end_col] is not None:
                    return False
                if self.continue_capture:
                    self.continue_capture = False

                return True

        return False


    def make_move(self, move, notations=True):
        if notations:
            start_pos, end_pos = move.split('-')
            
            # Convert positions from 'a1' notation to list indices (row, col)
            start_row, start_col = self.convert_position_to_indices(start_pos)
            end_row, end_col = self.convert_position_to_indices(end_pos)
        else:
            start_row, start_col = move[0]
            end_row, end_col = move[1]

        if not self.is_valid_move((start_row, start_col), (end_row, end_col)):
            return False

        if self.board[start_row][start_col] == self.BLACK:
            self.board[end_row][end_col] = self.BLACK if end_row != 0 else self.BLACK_QUEEN
        elif self.board[start_row][start_col] == self.WHITE:
            self.board[end_row][end_col] = self.WHITE if end_row != self.BOARD_LENGTH - 1 else self.WHITE_QUEEN
        else:
            self.board[end_row][end_col] = self.board[start_row][start_col]
        
        self.board[start_row][start_col] = None

        row_diff = end_row - start_row
        col_diff = end_col - start_col

        queen = self.WHITE_QUEEN if self.current_turn is self.WHITE else self.BLACK_QUEEN
        if self.board[end_row][end_col] is queen:
            current_row = start_row
            current_col = start_col

            capture = False

            for i in range(abs(row_diff) - 1):
                current_row = current_row - 1 if row_diff < 0 else current_row + 1
                current_col = current_col - 1 if col_diff < 0 else current_col + 1

                if i == abs(row_diff) - 2 and self.board[current_row][current_col] is not None:
                    capture = True

                self.board[current_row][current_col] = None

            if capture:
                continue_capture = self.has_capture_move((end_row, end_col))
                if not continue_capture:
                    self.switch_player()
                else:
                    self.continue_capture = True
            else:
                self.switch_player()
            
        else:
            if abs(row_diff) == 2:
                # Calculate the position of the captured piece
                capture_row = (start_row + end_row) // 2
                capture_col = (start_col + end_col) // 2

                self.board[capture_row][capture_col] = None

                continue_capture = self.has_capture_move((end_row, end_col))
                if not continue_capture:
                    self.switch_player()
                else:
                    self.continue_capture = True
            else:
                self.switch_player()

        return True

    def is_capture_move(self, position: tuple[int], dst: tuple[int]):
        start_row, start_col = position
        end_row, end_col = dst
    
        if abs(end_row - start_row) != 2 or abs(end_col - start_col) != 2:
            return False

        capture_row = (start_row + end_row) // 2
        capture_col = (start_col + end_col) // 2

        queen_capture = self.WHITE_QUEEN if self.current_turn is self.WHITE else self.BLACK_QUEEN # Player can't capture it's own queen
        return (self.board[capture_row][capture_col] is not None and
                self.board[capture_row][capture_col] != self.current_turn and
                self.board[capture_row][capture_col] != queen_capture and
                self.board[end_row][end_col] is None)
    
    def has_capture_move(self, position: tuple[int, int]) -> bool:
        # Check all potential capture directions for additional captures
        row, col = position
        for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.BOARD_LENGTH and 0 <= new_col < self.BOARD_LENGTH and
                self.is_capture_move(position, (new_row, new_col))):
                return True
        return False
    
    def switch_player(self):
        self.current_turn = self.BLACK if self.current_turn == self.WHITE else self.WHITE

    def is_won(self):
        for player in [self.WHITE, self.BLACK]:
            player_found = False
            queen_found = False
            
            # Check if the player has any pieces
            for row in self.board:
                if player in row:
                    player_found = True
                if player == self.WHITE:
                    queen_found = queen_found or self.WHITE_QUEEN in row
                else:
                    queen_found = queen_found or self.BLACK_QUEEN in row

                if player_found and queen_found:
                    break
            
            if not player_found and not queen_found:
                return True

        return False
    
    def is_draw(self):
        for row in range(self.BOARD_LENGTH):
            for col in range(self.BOARD_LENGTH):
                piece = self.board[row][col]
                if piece in (self.WHITE, self.BLACK):
                    for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        if self.is_valid_move((row, col), (row + dr, col + dc)):
                            return False
        # @TODO here we also need to check so that queens does not have any legel move is we want to prove a draw           
        white_queen_count = self.board.count(self.WHITE_QUEEN)
        black_queen_count = self.board.count(self.BLACK_QUEEN)

        players_queen = self.WHITE_QUEEN if self.current_turn is self.WHITE else self.BLACK_QUEEN

        if players_queen is self.WHITE_QUEEN and white_queen_count == 0:
            return True
        
        if players_queen is self.BLACK_QUEEN and black_queen_count == 0:
            return True

        return white_queen_count == black_queen_count
    
    def is_game_over(self):
        return self.is_won() or self.is_draw()

    def get_winner(self):
        if self.is_game_over():
            # Determine winner based on piece count 
            white_pieces = sum(row.count(self.WHITE) for row in self.board)
            black_pieces = sum(row.count(self.BLACK) for row in self.board)
            return self.WHITE if white_pieces > black_pieces else self.BLACK
        return None
    
    def get_all_moves(self):
        moves: list[tuple[tuple[int]]] = []
        for row in range(self.BOARD_LENGTH):
            for col in range(self.BOARD_LENGTH):
                piece = self.board[row][col]

                if piece is None:
                    continue

                if piece != self.current_turn and piece != (self.WHITE_QUEEN if self.current_turn is self.WHITE else self.BLACK_QUEEN):
                    continue

                if piece in (self.WHITE, self.BLACK):
                    for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        if self.is_valid_move((row, col), (row + dr, col + dc)):
                            moves.append(((row, col), (row + dr, col + dc)))
                else:
                    for d in range(self.BOARD_LENGTH):
                        for dr, dc in [(-d, -d), (-d, d), (d, -d), (d, d)]:
                            if self.is_valid_move((row, col), (row + dr, col + dc)):
                                moves.append(((row, col), (row + dr, col + dc)))
                
        return moves
    
    def evaluate(self):
        white_score = 0
        black_score = 0

        for row in range(self.BOARD_LENGTH):
            for col in range(self.BOARD_LENGTH):
                piece = self.board[row][col]

                if piece is None:
                    continue

                if piece is self.WHITE_QUEEN:
                    white_score += 5
                elif piece is self.WHITE:
                    white_score += 1
                elif piece is self.BLACK_QUEEN:
                    black_score += 5
                else:
                    black_score += 1

                
        return white_score - black_score
    
    def convert_position_to_indices(self, pos):
        column, row = pos
        col_idx = ord(column) - ord('a')
        row_idx = int(row) - 1
        return row_idx, col_idx
    
    def convert_indices_to_position(self, indices):
        row, column = indices
        col_idx = chr(column + ord('a'))
        row_idx = row + 1
        return str(col_idx) + str(row_idx)
