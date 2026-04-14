# NameDecoder

A desktop app that decodes your name through numerology and plays a video revealing what your number says about you.

Enter your name → get your number → watch your reading.

---

## Features

- Pythagorean numerology engine with full support for Master Numbers (11, 22, 33)
- Custom video reading for each possible result (numbers 1–9 plus 11, 22, 33)
- "About Numerology" video for first-timers who want to understand the system
- Smooth fade-in animations on the main screen
- Auto-installs its own dependency — just run `main.py` and it handles the rest

---

## Requirements

- Python 3.8+
- PySide6 (installed automatically on first run if missing)

---

## Installation

```bash
git clone https://github.com/Twochill/NameDecoder.git
cd NameDecoder
python main.py
```

If PySide6 is not installed, the app will ask to install it for you. After installation, rerun `python main.py`.

> **Note:** the repository includes all video assets (~300 MB). The clone will take a moment depending on your connection.

---

## Usage

1. Run `python main.py`
2. Type your full name into the input field
3. Click **Convert** — your numerology number is calculated and the corresponding video plays
4. The app returns to the main screen when the video ends
5. Click **About Numerology** at any time to watch an introduction to the numerology system used

---

## How it works

Each letter in your name maps to a number 1–9 using the Pythagorean system (A=1, B=2, ... I=9, J=1, and so on). All values are summed and repeatedly digit-reduced until a single digit remains — unless the sum is 11, 22, or 33, which are **Master Numbers** and preserved as-is.

```python
def calculate_number(name: str) -> int:
    total = sum(((ord(c.upper()) - 65) % 9) + 1 for c in name if c.isalpha())
    while total > 9 and total not in {11, 22, 33}:
        total = sum(int(d) for d in str(total))
    return total
```

---

## License

[GNU General Public License v2.0](LICENSE)
