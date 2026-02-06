# 🎮 Advanced Tic Tac Toe

A modern, feature-rich Tic Tac Toe game built with Python and Tkinter. Play against a friend or challenge the AI with multiple difficulty levels!

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎯 Game Modes
- **2 Player Mode** - Play locally with a friend
- **vs AI Mode** - Challenge the computer

### 🤖 AI Difficulty Levels
- **Easy** - Random moves, perfect for beginners
- **Medium** - Mix of smart and random moves
- **Hard** - Unbeatable Minimax algorithm

### 🎨 Themes
- **Dark** - Modern dark theme with neon accents
- **Light** - Clean light theme
- **Retro** - Classic retro styling

### 📊 Game Statistics
- Tracks total games played
- Win/loss/draw statistics
- Persistent storage of game history

### 🎮 Additional Features
- **Undo Move** - Take back your last move
- **Custom Player Names** - Personalize your experience
- **Win Detection** - Visual highlighting of winning moves
- **Draw Detection** - Properly handles tie games

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Game
```bash
python tic_tac_toe.py
```

## 📖 How to Play

1. **Launch the game** by running `python tic_tac_toe.py`
2. **Select Game Mode:**
   - Choose "2 Player" to play with a friend
   - Choose "vs AI" to play against the computer
3. **Set AI Difficulty** (when playing vs AI):
   - Easy: Random moves
   - Medium: Balanced challenge
   - Hard: Impossible to beat
4. **Customize Player Names** (optional)
5. **Choose Your Theme** from the dropdown
6. **Click on the grid** to make your move
7. **First player to get 3 in a row wins!**

### Controls
- **Undo** - Revert your last move
- **New Round** - Start a fresh game (keeps scores)
- **Stats** - View your game statistics
- **Reset All** - Clear everything including scores

## 🏗️ Architecture

The game is built using an object-oriented architecture:

```
TicTacToeGame      - Main game controller
├── GameStats      - Statistics management
├── TicTacToeAI    - AI opponent (Minimax algorithm)
└── Theme          - Color themes (Dark/Light/Retro)
```

### AI Algorithm
The Hard difficulty uses the **Minimax algorithm**, which:
- Explores all possible game states
- Chooses the optimal move every time
- Is mathematically unbeatable (best you can do is draw)

## 📝 File Structure

```
Advance-Tic-Tac-Toe/
├── tic_tac_toe.py      # Main game file
├── requirements.txt    # Python dependencies
├── game_stats.json     # Game statistics (auto-generated)
└── README.md          # This file
```

## 🎨 Screenshots

*Dark Theme* - Modern look with neon accents  
*Light Theme* - Clean and minimal  
*Retro Theme* - Classic arcade feel

## 🔮 Future Enhancements

- [ ] Online multiplayer
- [ ] Sound effects and music
- [ ] Animated moves and transitions
- [ ] 4x4 and 5x5 board sizes
- [ ] Time attack mode
- [ ] Leaderboards

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📜 License

This project is licensed under the MIT License.

## 🙏 Credits

Created by [codecravings](https://github.com/codecravings)

---

Enjoy the game! If you have any suggestions or find bugs, please open an issue. 🎮
