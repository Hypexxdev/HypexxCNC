# Hypexx CNC

A multi-method Layer 4 and Layer 7 stress-testing tool for educational and research purposes. This project provides a command-line CNC (Command & Control) interface to launch various network stress tests using both Python and Node.js scripts.

## Features
- Modern, dark-themed CNC interface
- Layer 7 (HTTP) and Layer 4 (UDP/TCP) test methods
- Modular: Python for CNC and some attacks, Node.js for high-performance HTTP/UDP attacks
- Animated ASCII art and colored output (auto-detects Windows CMD/ANSI support)

## Methods Supported
- **http-raw**: Layer 7 HTTP request flood (Node.js)
- **http-rand**: Layer 7 random path flood (Node.js)
- **http-cookie**: Layer 7 cookie header flood (Node.js)
- **http-post**: Layer 7 POST data flood (Node.js)
- **udp-flood**: Layer 4 UDP packet flood (Node.js)
- **slowloris**: Layer 7 Slowloris (Python)
- **tcp-flood**: Layer 4 TCP SYN flood (Python)
# UDP & TCP & SLOWLORIS NO WORKING


# Preview

-# https://prnt.sc/eqHplC-YJhqz
-# https://prnt.sc/UKZIsw8lXpUw


---

## Installation

### 1. Clone or Extract
Extract the repository or clone it:
```sh
git clone https://github.com/Hypexxdev/HypexxCNC.git
cd HypexxCNC
```

### 2. Install Python Dependencies
Make sure you have Python 3.8+ installed. Then run:
```sh
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies
Make sure you have Node.js (v16+) and npm installed. Then run:
```sh
npm install
```

Or, to install both at once (Windows):
```bat
start-all.bat
```

---

## Usage

### Start the CNC
On Windows:
```bat
start.bat
```
Or, in any terminal:
```sh
python main.py
```

### Using the CNC
- Type `help` to see all commands and methods.
- Use the listed commands to launch different stress tests.
- The CNC will prompt for all required parameters interactively.

---

## Project Structure
- `main.py` — Main CNC interface (Python)
- `resources/` — Node.js attack scripts
- `requirements.txt` — Python dependencies
- `package.json` — Node.js dependencies
- `start.bat` — Start the CNC (Windows)
- `start-all.bat` — Install all dependencies (Windows)

---

## Disclaimer
This project is for **educational and authorized testing** only. Do not use it to attack networks or systems without explicit permission. The author is not responsible for any misuse.

---

## Credits
Developed by: Hypexx
