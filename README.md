# NameDecoder

A desktop app that decodes your name through numerology and plays a personalized video based on your result.

---

## Features

- Pythagorean numerology engine — each letter maps to a value 1–9, summed and reduced to a single digit
- Master Numbers 11, 22, and 33 are preserved (not reduced), as per traditional numerology
- A unique video plays for each of the 12 possible outcomes
- "About Numerology" button plays an introduction video explaining the system
- Smooth fade-in animations on the main screen
- Auto-installs its own dependency (PySide6) on first run — no manual setup needed

---

## Requirements

- Python 3.8 or higher
- PySide6 (installed automatically on first run)

> The repository includes all video assets (~312 MB total). Clone size reflects this.

---

## Installation

```bash
git clone https://github.com/Twochill/NameDecoder.git
cd NameDecoder
python main.py
```

If PySide6 is not installed, the app will detect this, offer to install it, and exit. Rerun `python main.py` after installation.

---

## Usage

1. Type your full name in the input field
2. Click **Convert**
3. A video plays revealing your numerology number and its meaning
4. The app returns to the main screen when the video ends
5. Click **About Numerology** at any time to watch an introduction to the system

---

## How it works

NameDecoder uses the Pythagorean system:

- Each letter is assigned a value: A=1, B=2, C=3 ... I=9, J=1, K=2, ...
- All letter values in the name are summed
- The sum is reduced by adding its digits repeatedly until a single digit remains
- Exception: if the sum or any intermediate result is 11, 22, or 33, it stops — these are Master Numbers

Example: `ALEX` → 1+3+5+6 = 15 → 1+5 = **6**

---

## License

[GNU General Public License v2.0](LICENSE)
