from Game import Game
from Board import Board, Move
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt

class GameGUI(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.setWindowTitle("Checkers Game")
        self.setGeometry(100, 100, 600, 600)
        
        self.selected_piece = None  # Track selected piece coordinates
        self.winner = None
        self._initialize_ui()

    def _initialize_ui(self):
        # Create a central widget and set a grid layout for the board
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.grid_layout = QGridLayout()
        central_widget.setLayout(self.grid_layout)
        
        # Draw the board
        self._draw_board()

    def _draw_board(self):
        # Clear current board display
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().deleteLater()

        # Draw each square on the board
        for row in range(self.game._board.BOARD_LENGTH):
            for col in range(self.game._board.BOARD_LENGTH):
                square = QLabel(self)
                square.setFixedSize(70, 70)

                # Set alternating colors for board squares
                color = QColor(139, 69, 19) if (row + col) % 2 == 0 else QColor(245, 245, 220)
                
                # Add green border for the selected square
                border_color = "green" if self.selected_piece == (row, col) else "black"
                square.setStyleSheet(f"background-color: {color.name()}; border: 2px solid {border_color};")

                # Display pieces based on the board state
                piece = self.game._board._board[row][col]
                if piece == self.game._board.WHITE:
                    square.setPixmap(QPixmap("white_piece.png").scaled(60, 60, Qt.KeepAspectRatio))
                elif piece == self.game._board.BLACK:
                    square.setPixmap(QPixmap("black_piece.png").scaled(60, 60, Qt.KeepAspectRatio))

                # Connect square click to move handling
                square.mousePressEvent = lambda event, r=row, c=col: self._handle_square_click(r, c)
                
                # Add square to the grid
                self.grid_layout.addWidget(square, row, col)

    def _handle_square_click(self, row, col):
        # Handle piece selection and movement
        if self.selected_piece is None:
            # Select a piece if one exists at the clicked square
            if self.game.is_valid_select(row, col):
                self.selected_piece = (row, col)
                print(f"Selected piece at {self.selected_piece}")
        else:
            # Attempt to make a move
            self.game.play_turn(Move(self.selected_piece, (row, col)))
            self.selected_piece = None  # Reset selection

        self.update_board()  # Redraw the board with updated selection or move

    def update_board(self):
        # Redraw the board after each move or selection
        if self.game.is_game_over():
            self.winner = self.game.get_winner()
            self._show_winner_popup()
        else:
            self._draw_board()

    def _show_winner_popup(self):
        # Show a popup with the winner and play again option
        winner_text = "White" if self.winner == self.game._board.WHITE else "Black"
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(f"Player {winner_text} wins! Would you like to play again?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        # Check if the user wants to play again
        response = msg_box.exec()
        if response == QMessageBox.Yes:
            self._restart_game()
        else:
            self.close()

    def _restart_game(self):
        # Reset the game state for a new game
        self.game = Game()
        self.winner = None
        self.selected_piece = None
        self._draw_board()

# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Initialize your Game and Board objects (assuming they are defined similarly to your earlier code)
    game = Game()
    game_gui = GameGUI(game)
    game_gui.show()
    
    sys.exit(app.exec_())
