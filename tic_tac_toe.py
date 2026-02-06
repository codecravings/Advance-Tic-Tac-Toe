"""
Advanced Tic Tac Toe Game
=========================
A modern, feature-rich Tic Tac Toe game with AI opponent,
beautiful UI, themes, sound effects, and game statistics.

Author: codecravings
"""

import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
from datetime import datetime
from enum import Enum
from typing import Optional, List, Tuple

# Try to import pygame for sound effects
try:
    import pygame
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False


class GameMode(Enum):
    """Game mode enumeration."""
    TWO_PLAYER = "2 Player"
    VS_AI = "vs AI"


class Difficulty(Enum):
    """AI difficulty levels."""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class Theme:
    """Color theme definitions."""
    
    DARK = {
        'bg': '#1a1a2e',
        'fg': '#eaeaea',
        'accent': '#e94560',
        'secondary': '#16213e',
        'highlight': '#0f3460',
        'success': '#00d9ff',
        'button_bg': '#16213e',
        'button_fg': '#eaeaea',
        'x_color': '#e94560',
        'o_color': '#00d9ff',
        'win_bg': '#2ecc71'
    }
    
    LIGHT = {
        'bg': '#f5f5f5',
        'fg': '#333333',
        'accent': '#e74c3c',
        'secondary': '#ffffff',
        'highlight': '#3498db',
        'success': '#2ecc71',
        'button_bg': '#ffffff',
        'button_fg': '#333333',
        'x_color': '#e74c3c',
        'o_color': '#3498db',
        'win_bg': '#2ecc71'
    }
    
    RETRO = {
        'bg': '#2c3e50',
        'fg': '#ecf0f1',
        'accent': '#f39c12',
        'secondary': '#34495e',
        'highlight': '#16a085',
        'success': '#27ae60',
        'button_bg': '#34495e',
        'button_fg': '#ecf0f1',
        'x_color': '#e74c3c',
        'o_color': '#f39c12',
        'win_bg': '#27ae60'
    }


class GameStats:
    """Manages game statistics."""
    
    def __init__(self):
        self.stats_file = "game_stats.json"
        self.stats = self._load_stats()
    
    def _load_stats(self) -> dict:
        """Load statistics from file."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'games_played': 0,
            'x_wins': 0,
            'o_wins': 0,
            'draws': 0,
            'history': []
        }
    
    def save_stats(self):
        """Save statistics to file."""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def record_game(self, winner: Optional[str], player_x: str, player_o: str):
        """Record a completed game."""
        self.stats['games_played'] += 1
        
        if winner == 'X':
            self.stats['x_wins'] += 1
        elif winner == 'O':
            self.stats['o_wins'] += 1
        else:
            self.stats['draws'] += 1
        
        self.stats['history'].append({
            'date': datetime.now().isoformat(),
            'winner': winner if winner else 'Draw',
            'player_x': player_x,
            'player_o': player_o
        })
        
        # Keep only last 50 games
        self.stats['history'] = self.stats['history'][-50:]
        self.save_stats()
    
    def get_stats_text(self) -> str:
        """Get formatted statistics text."""
        total = self.stats['games_played']
        if total == 0:
            return "No games played yet!"
        
        x_pct = (self.stats['x_wins'] / total) * 100
        o_pct = (self.stats['o_wins'] / total) * 100
        draw_pct = (self.stats['draws'] / total) * 100
        
        return (
            f"Game Statistics\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"Total Games: {total}\n"
            f"X Wins: {self.stats['x_wins']} ({x_pct:.1f}%)\n"
            f"O Wins: {self.stats['o_wins']} ({o_pct:.1f}%)\n"
            f"Draws: {self.stats['draws']} ({draw_pct:.1f}%)"
        )


class TicTacToeAI:
    """AI opponent using Minimax algorithm."""
    
    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.ai_player = 'O'
        self.human_player = 'X'
    
    def get_move(self, board: List[List[str]]) -> Tuple[int, int]:
        """Get AI's next move based on difficulty."""
        if self.difficulty == Difficulty.EASY:
            return self._get_random_move(board)
        elif self.difficulty == Difficulty.MEDIUM:
            # 50% chance of optimal move, 50% random
            if random.random() < 0.5:
                return self._get_random_move(board)
            else:
                return self._get_best_move(board)
        else:  # HARD
            return self._get_best_move(board)
    
    def _get_random_move(self, board: List[List[str]]) -> Tuple[int, int]:
        """Get a random valid move."""
        available = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    available.append((i, j))
        return random.choice(available) if available else (0, 0)
    
    def _get_best_move(self, board: List[List[str]]) -> Tuple[int, int]:
        """Get the best move using Minimax."""
        best_score = float('-inf')
        best_move = (0, 0)
        
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = self.ai_player
                    score = self._minimax(board, 0, False)
                    board[i][j] = ''
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        return best_move
    
    def _minimax(self, board: List[List[str]], depth: int, is_maximizing: bool) -> int:
        """Minimax algorithm implementation."""
        winner = self._check_winner(board)
        
        if winner == self.ai_player:
            return 10 - depth
        elif winner == self.human_player:
            return depth - 10
        elif self._is_board_full(board):
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = self.ai_player
                        score = self._minimax(board, depth + 1, False)
                        board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = self.human_player
                        score = self._minimax(board, depth + 1, True)
                        board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score
    
    def _check_winner(self, board: List[List[str]]) -> Optional[str]:
        """Check if there's a winner."""
        # Check rows
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != '':
                return board[i][0]
        
        # Check columns
        for j in range(3):
            if board[0][j] == board[1][j] == board[2][j] != '':
                return board[0][j]
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != '':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '':
            return board[0][2]
        
        return None
    
    def _is_board_full(self, board: List[List[str]]) -> bool:
        """Check if board is full."""
        for row in board:
            if '' in row:
                return False
        return True


class TicTacToeGame:
    """Main Tic Tac Toe game class."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Tic Tac Toe")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Game state
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_active = True
        self.move_history = []
        
        # Settings
        self.game_mode = GameMode.TWO_PLAYER
        self.difficulty = Difficulty.MEDIUM
        self.current_theme = Theme.DARK
        self.player_x_name = tk.StringVar(value="Player X")
        self.player_o_name = tk.StringVar(value="Player O")
        
        # Managers
        self.stats = GameStats()
        self.ai: Optional[TicTacToeAI] = None
        
        # UI Elements
        self.buttons: List[List[tk.Button]] = []
        self.status_label: Optional[tk.Label] = None
        
        self._setup_ui()
        self.apply_theme()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Main container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = tk.Label(
            self.main_frame,
            text="TIC TAC TOE",
            font=('Helvetica', 36, 'bold')
        )
        self.title_label.pack(pady=(0, 20))
        
        # Settings Frame
        self._create_settings_frame()
        
        # Game Board Frame
        self._create_board_frame()
        
        # Status Frame
        self._create_status_frame()
        
        # Control Buttons
        self._create_control_buttons()
    
    def _create_settings_frame(self):
        """Create the settings panel."""
        settings_frame = tk.LabelFrame(
            self.main_frame,
            text="Settings",
            font=('Helvetica', 12, 'bold')
        )
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Game Mode
        mode_frame = tk.Frame(settings_frame)
        mode_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(mode_frame, text="Mode:", font=('Helvetica', 11)).pack(side=tk.LEFT)
        self.mode_var = tk.StringVar(value=GameMode.TWO_PLAYER.value)
        mode_menu = ttk.Combobox(
            mode_frame,
            textvariable=self.mode_var,
            values=[mode.value for mode in GameMode],
            state='readonly',
            width=10
        )
        mode_menu.pack(side=tk.LEFT, padx=5)
        mode_menu.bind('<<ComboboxSelected>>', self._on_mode_change)
        
        # Difficulty
        diff_frame = tk.Frame(settings_frame)
        diff_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(diff_frame, text="AI Difficulty:", font=('Helvetica', 11)).pack(side=tk.LEFT)
        self.diff_var = tk.StringVar(value=Difficulty.MEDIUM.value)
        self.diff_menu = ttk.Combobox(
            diff_frame,
            textvariable=self.diff_var,
            values=[diff.value for diff in Difficulty],
            state='readonly',
            width=10
        )
        self.diff_menu.pack(side=tk.LEFT, padx=5)
        self.diff_menu.bind('<<ComboboxSelected>>', self._on_difficulty_change)
        self.diff_menu.configure(state='disabled')
        
        # Theme
        theme_frame = tk.Frame(settings_frame)
        theme_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(theme_frame, text="Theme:", font=('Helvetica', 11)).pack(side=tk.LEFT)
        self.theme_var = tk.StringVar(value="Dark")
        theme_menu = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=["Dark", "Light", "Retro"],
            state='readonly',
            width=10
        )
        theme_menu.pack(side=tk.LEFT, padx=5)
        theme_menu.bind('<<ComboboxSelected>>', self._on_theme_change)
        
        # Player Names
        name_frame = tk.Frame(settings_frame)
        name_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        tk.Label(name_frame, text="X:", font=('Helvetica', 11)).pack(side=tk.LEFT)
        tk.Entry(name_frame, textvariable=self.player_x_name, width=10, font=('Helvetica', 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Label(name_frame, text="O:", font=('Helvetica', 11)).pack(side=tk.LEFT)
        tk.Entry(name_frame, textvariable=self.player_o_name, width=10, font=('Helvetica', 10)).pack(side=tk.LEFT, padx=5)
    
    def _create_board_frame(self):
        """Create the game board."""
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(pady=20)
        
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text='',
                    font=('Helvetica', 40, 'bold'),
                    width=4,
                    height=2,
                    command=lambda r=i, c=j: self._on_cell_click(r, c)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
    
    def _create_status_frame(self):
        """Create the status display."""
        status_frame = tk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="Player X's turn",
            font=('Helvetica', 18, 'bold')
        )
        self.status_label.pack()
        
        # Score display
        self.score_frame = tk.Frame(status_frame)
        self.score_frame.pack(pady=10)
        
        self.x_score_var = tk.StringVar(value="X: 0")
        self.o_score_var = tk.StringVar(value="O: 0")
        
        tk.Label(
            self.score_frame,
            textvariable=self.x_score_var,
            font=('Helvetica', 16, 'bold')
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            self.score_frame,
            textvariable=self.o_score_var,
            font=('Helvetica', 16, 'bold')
        ).pack(side=tk.LEFT, padx=20)
    
    def _create_control_buttons(self):
        """Create control buttons."""
        control_frame = tk.Frame(self.main_frame)
        control_frame.pack(pady=10)
        
        self.undo_btn = tk.Button(
            control_frame,
            text="Undo",
            font=('Helvetica', 14),
            width=10,
            command=self._undo_move
        )
        self.undo_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame,
            text="New Round",
            font=('Helvetica', 14),
            width=12,
            command=self._new_round
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame,
            text="Stats",
            font=('Helvetica', 14),
            width=10,
            command=self._show_stats
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame,
            text="Reset All",
            font=('Helvetica', 14),
            width=12,
            command=self._reset_all
        ).pack(side=tk.LEFT, padx=5)

    def _on_mode_change(self, event=None):
        """Handle game mode change."""
        mode_value = self.mode_var.get()
        if mode_value == GameMode.VS_AI.value:
            self.game_mode = GameMode.VS_AI
            self.diff_menu.configure(state='readonly')
            self.player_o_name.set("AI")
            self.ai = TicTacToeAI(self.difficulty)
        else:
            self.game_mode = GameMode.TWO_PLAYER
            self.diff_menu.configure(state='disabled')
            self.player_o_name.set("Player O")
            self.ai = None
        self._new_round()
    
    def _on_difficulty_change(self, event=None):
        """Handle difficulty change."""
        diff_value = self.diff_var.get()
        for diff in Difficulty:
            if diff.value == diff_value:
                self.difficulty = diff
                break
        if self.ai:
            self.ai.difficulty = self.difficulty
    
    def _on_theme_change(self, event=None):
        """Handle theme change."""
        theme_name = self.theme_var.get()
        if theme_name == "Dark":
            self.current_theme = Theme.DARK
        elif theme_name == "Light":
            self.current_theme = Theme.LIGHT
        else:
            self.current_theme = Theme.RETRO
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme to all UI elements."""
        theme = self.current_theme
        
        self.root.configure(bg=theme['bg'])
        self.main_frame.configure(bg=theme['bg'])
        
        # Update title
        self.title_label.configure(
            bg=theme['bg'],
            fg=theme['accent']
        )
        
        # Update status
        self.status_label.configure(
            bg=theme['bg'],
            fg=theme['fg']
        )
        
        # Update score frame
        self.score_frame.configure(bg=theme['bg'])
        for widget in self.score_frame.winfo_children():
            widget.configure(bg=theme['bg'], fg=theme['fg'])
        
        # Update buttons
        for row in self.buttons:
            for btn in row:
                current_text = btn.cget('text')
                if current_text == '':
                    btn.configure(
                        bg=theme['button_bg'],
                        fg=theme['button_fg'],
                        activebackground=theme['highlight']
                    )
                elif current_text == 'X':
                    btn.configure(bg=theme['button_bg'], fg=theme['x_color'])
                elif current_text == 'O':
                    btn.configure(bg=theme['button_bg'], fg=theme['o_color'])
    
    def _on_cell_click(self, row: int, col: int):
        """Handle cell click."""
        if not self.game_active or self.board[row][col] != '':
            return
        
        self._make_move(row, col)
        
        # AI turn
        if self.game_active and self.game_mode == GameMode.VS_AI and self.current_player == 'O':
            self.root.after(500, self._ai_move)
    
    def _make_move(self, row: int, col: int):
        """Make a move at the specified position."""
        self.board[row][col] = self.current_player
        self.move_history.append((row, col))
        
        # Update button
        btn = self.buttons[row][col]
        btn.configure(
            text=self.current_player,
            fg=self.current_theme['x_color'] if self.current_player == 'X' else self.current_theme['o_color']
        )
        
        # Check for win or draw
        if self._check_win():
            self._handle_win()
        elif self._check_draw():
            self._handle_draw()
        else:
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self._update_status()
    
    def _ai_move(self):
        """Execute AI move."""
        if not self.game_active or self.ai is None:
            return
        
        row, col = self.ai.get_move(self.board)
        self._make_move(row, col)
    
    def _check_win(self) -> bool:
        """Check if current player has won."""
        player = self.current_player
        
        # Check rows
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                self._highlight_win([(i, j) for j in range(3)])
                return True
        
        # Check columns
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                self._highlight_win([(i, j) for i in range(3)])
                return True
        
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            self._highlight_win([(i, i) for i in range(3)])
            return True
        
        if all(self.board[i][2-i] == player for i in range(3)):
            self._highlight_win([(i, 2-i) for i in range(3)])
            return True
        
        return False
    
    def _check_draw(self) -> bool:
        """Check if game is a draw."""
        for row in self.board:
            if '' in row:
                return False
        return True
    
    def _highlight_win(self, cells: List[Tuple[int, int]]):
        """Highlight winning cells."""
        for row, col in cells:
            self.buttons[row][col].configure(bg=self.current_theme['win_bg'])
    
    def _handle_win(self):
        """Handle win condition."""
        self.game_active = False
        winner_name = self.player_x_name.get() if self.current_player == 'X' else self.player_o_name.get()
        
        self.stats.record_game(self.current_player, self.player_x_name.get(), self.player_o_name.get())
        
        # Update score display
        if self.current_player == 'X':
            x_wins = int(self.x_score_var.get().split(': ')[1]) + 1
            self.x_score_var.set(f"X: {x_wins}")
        else:
            o_wins = int(self.o_score_var.get().split(': ')[1]) + 1
            self.o_score_var.set(f"O: {o_wins}")
        
        self.status_label.configure(text=f"{winner_name} wins!")
        messagebox.showinfo("Game Over", f"Congratulations {winner_name}! You won!")
    
    def _handle_draw(self):
        """Handle draw condition."""
        self.game_active = False
        self.stats.record_game(None, self.player_x_name.get(), self.player_o_name.get())
        
        self.status_label.configure(text="It's a draw!")
        messagebox.showinfo("Game Over", "It's a draw! Well played!")
    
    def _update_status(self):
        """Update status label."""
        player_name = self.player_x_name.get() if self.current_player == 'X' else self.player_o_name.get()
        self.status_label.configure(text=f"{player_name}'s turn ({self.current_player})")
    
    def _undo_move(self):
        """Undo the last move."""
        if not self.move_history or not self.game_active:
            return
        
        # In AI mode, undo both AI and player moves
        moves_to_undo = 2 if self.game_mode == GameMode.VS_AI and len(self.move_history) >= 2 else 1
        
        for _ in range(moves_to_undo):
            if self.move_history:
                row, col = self.move_history.pop()
                self.board[row][col] = ''
                self.buttons[row][col].configure(
                    text='',
                    bg=self.current_theme['button_bg']
                )
        
        # Reset to player's turn in AI mode
        if self.game_mode == GameMode.VS_AI:
            self.current_player = 'X'
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        self._update_status()
    
    def _new_round(self):
        """Start a new round."""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_active = True
        self.move_history = []
        
        for row in self.buttons:
            for btn in row:
                btn.configure(
                    text='',
                    bg=self.current_theme['button_bg']
                )
        
        self._update_status()
    
    def _show_stats(self):
        """Show game statistics."""
        stats_text = self.stats.get_stats_text()
        messagebox.showinfo("Statistics", stats_text)
    
    def _reset_all(self):
        """Reset everything including scores."""
        self.x_score_var.set("X: 0")
        self.o_score_var.set("O: 0")
        self._new_round()
    
    def run(self):
        """Start the game."""
        self.root.mainloop()


if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()
