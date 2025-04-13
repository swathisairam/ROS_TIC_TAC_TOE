import rclpy
from rclpy.node import Node

class TicTacToe(Node):
    def __init__(self):
        super().__init__('tic_tac_toe')
        
        # Ask the user for the number of players
        while True:
            try:
                self.num_players = int(input("Enter number of players (2 to 4): "))
                if self.num_players in [2, 3, 4]:
                    break
                else:
                    self.get_logger().info("Invalid input. Enter a number between 2 and 4.")
            except ValueError:
                self.get_logger().info("Invalid input. Please enter a number.")

        # Define board size dynamically based on players
        self.board_size = self.num_players + 1  
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.players = ['X', 'O', 'Y', 'Z'][:self.num_players]  # Set player symbols
        self.current_player_index = 0  # Track current player
        
        self.get_logger().info(f"Tic Tac Toe Node has started with {self.num_players} players!")
        self.play_game()

    def print_board(self):
        separator = "-" * (self.board_size * 4 - 1)  # Adjust separator width
        for row in self.board:
            self.get_logger().info(" | ".join(row))
            self.get_logger().info(separator)

    def check_winner(self):
        # Check rows
        for row in self.board:
            if len(set(row)) == 1 and row[0] != ' ':
                return row[0]

        # Check columns
        for col in range(self.board_size):
            col_values = {self.board[row][col] for row in range(self.board_size)}
            if len(col_values) == 1 and ' ' not in col_values:
                return self.board[0][col]

        # Check diagonals
        main_diag = {self.board[i][i] for i in range(self.board_size)}
        anti_diag = {self.board[i][self.board_size - 1 - i] for i in range(self.board_size)}

        if len(main_diag) == 1 and ' ' not in main_diag:
            return self.board[0][0]
        if len(anti_diag) == 1 and ' ' not in anti_diag:
            return self.board[0][self.board_size - 1]

        return None

    def play_game(self):
        move_count = 0
        max_moves = self.board_size ** 2  # Max possible moves

        while move_count < max_moves:
            self.print_board()
            row, col = self.get_player_move()
            self.board[row][col] = self.players[self.current_player_index]

            winner = self.check_winner()
            if winner:
                self.print_board()
                self.get_logger().info(f"Player {winner} wins!")
                return

            # Switch to next player
            self.current_player_index = (self.current_player_index + 1) % self.num_players
            move_count += 1

        self.get_logger().info("It's a draw!")

    def get_player_move(self):
        while True:
            try:
                row = int(input(f"Player {self.players[self.current_player_index]}, enter row (0-{self.board_size-1}): "))
                col = int(input(f"Player {self.players[self.current_player_index]}, enter col (0-{self.board_size-1}): "))

                if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == ' ':
                    return row, col
                else:
                    self.get_logger().info("Invalid move, try again.")

            except ValueError:
                self.get_logger().info("Invalid input. Enter numbers within the valid range.")

def main(args=None):
    rclpy.init(args=args)
    node = TicTacToe()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
