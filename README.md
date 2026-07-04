# VIM Cheat Sheet — Interactive TUI

[![platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-blue)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-green)]()
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

An interactive terminal UI for browsing VIM commands, organized by category with live search and switchable themes.

![screenshot](https://img.shields.io/badge/status-stable-brightgreen)

---

## Features

- **9 categories** — Movement, Editing, Search & Replace, Visual Mode, Windows & Tabs, Marks & Registers, Ex Commands, Insert Mode, Advanced & Tips
- **224 commands** — from basic to advanced, with difficulty badges ([B] [I] [A])
- **Live search** — press `/` to search all commands by key or description
- **4 themes** — 2 dark (Tokyo Night, Dracula) + 2 light (Catppuccin Latte, GitHub Light); cycle with `t`
- **Vim-style navigation** — `j/k` to move, `g/G` to top/bottom, `h/l` to switch panels
- **Cross-platform** — works on Linux, macOS, and Windows

---

## Quick Start

```bash
git clone https://github.com/guspatagonico/vim-cheat.git
cd vim-cheat

# Linux/macOS
chmod +x vim-cheat.sh && ./vim-cheat.sh

# Windows
vim-cheat.bat

# Or manually:
pip install -r requirements.txt
python run.py
```

---

## Controls

| Key | Action |
|-----|--------|
| `j` / `k` | Navigate down / up |
| `g` / `G` | Go to top / bottom |
| `d` / `u` | Page down / up |
| `h` / `l` | Focus sidebar / content |
| `Enter` | Select category |
| `/` | Live search |
| `t` | Cycle theme (4 themes) |
| `?` | Help |
| `q` | Quit |

---

## Themes

| Theme | Type | Accent |
|-------|------|--------|
| Tokyo Night | 🌙 Dark | Blue `#89b4fa` |
| Dracula | 🌙 Dark | Purple `#bd93f9` |
| Catppuccin Latte | ☀️ Light | Blue `#7287fd` |
| GitHub Light | ☀️ Light | Blue `#0969da` |

Press `t` to cycle. Theme is active for the current session only (persistence via config coming in a future version).

---

## Customizing

### Adding commands

Edit the `CHEAT_DATA` list in `vim_cheat.py`. Each entry is:

```python
("keybinding", "Description", "basic|intermediate|advanced")
```

### Adding a theme

Add a new dict to `THEMES` in `vim_cheat.py` with all required color keys:

```python
"my-theme": {
    "name": "My Theme",
    "type": "dark",          # or "light"
    "bg": "#...",
    "sidebar_bg": "#...",
    # ... see existing themes for all keys
}
```

---

## Project Structure

```
vim-cheat/
├── vim_cheat.py       # Single-file app
├── run.py             # Entry point
├── AGENTS.md          # Dev notes & roadmap
├── vim-cheat.sh       # Linux/macOS launcher
├── vim-cheat.bat      # Windows launcher
├── requirements.txt   # Dependencies (textual)
└── README.md          # This file
```

---

## License

MIT License — see [LICENSE](LICENSE) below.

Copyright © 2025 **Gustavo Adrián Salvini**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Author

**Gustavo Adrián Salvini**  
📧 guspatagonico@gmail.com  
🐙 [github.com/guspatagonico](https://github.com/guspatagonico)

---

## Contributing

Pull requests, issues, and feature requests are welcome! Feel free to:

- Report bugs or suggest features via [Issues](https://github.com/guspatagonico/vim-cheat/issues)
- Submit PRs for new commands, themes, or features
- Fork and adapt for your own projects (MIT license)

See [AGENTS.md](AGENTS.md) for the development roadmap and architecture notes.
