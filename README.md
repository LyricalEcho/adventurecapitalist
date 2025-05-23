# Adventure Capitalist CLI

A terminal-based simulation of the popular **AdVenture Capitalist** game.

## Features

* **Buy Businesses** with exponentially increasing costs
* **Hire Managers** for full automation of profit collection
* **Milestone Upgrades**: profits double at 25, 50, 100, 250, 500, and 1,000 units
* **Persistent State**: save & load game progress (`savegame.json`)
* **Offline Earnings**: managers accrue profits while the game is closed
* **Dynamic Intervals**: each business has a growth interval 10× longer than the previous
* **Formatted Numbers**: abbreviations for thousands (`k`), millions (`mil`), billions (`bil`)

## Project Structure

```
adventure-capitalist-cli/
├── constants.py       # Global constants and thresholds
├── business.py        # Business class & milestone logic
├── save_load.py       # Persistence (save & load, offline earnings)
├── ui.py              # Terminal display & formatting helpers
├── main.py            # Entry point: game loop & user interaction
└── savegame.json      # Auto-generated save file
```

## Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/adventure-capitalist-cli.git
   cd adventure-capitalist-cli
   ```
2. Ensure you have Python 3.7+ installed.
3. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Linux/macOS
   venv\Scripts\activate    # on Windows
   ```

## Usage

Run the game:

```bash
python main.py
```

### Controls

* **1**: Buy a business — enter the business number when prompted.
* **2**: Manually collect profits from unmanaged businesses.
* **3**: Hire a manager to automate a business — enter the business number.
* **4**: Save progress and exit the game.

## Contribution

Pull requests welcome! Please follow PEP8 styling and include tests where appropriate.

## License

MIT © LyricalEcho
