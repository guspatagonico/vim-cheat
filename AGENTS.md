# AGENTS.md — VIM Cheat Sheet TUI

## Project Overview

Interactive TUI (Terminal User Interface) VIM cheat sheet app built with Python + Textual.
Cross-platform: Linux, macOS, Windows.

**Stack:** Python 3.10+ · Textual 8.x · Rich

**Entry point:** `run.py` → `vim_cheat.py:main()`

---

## Architecture

```
run.py                 # Thin entry point
vim_cheat.py           # Single-file app (~820 lines)
  ├── THEMES           # Dict[str, Theme] — 4 themes (2 dark, 2 light)
  ├── CHEAT_DATA       # list[Category] — 9 categories, 224 commands
  ├── SearchScreen     # ModalScreen — live search over all commands
  ├── CatListItem      # ListItem — sidebar category row
  └── VimCheatApp      # App — main application
```

### Data flow

```
User input (keyboard)
  → BINDINGS map key → action method
    → action_cycle_theme → current_theme_name (reactive) → watch → _apply_theme()
    → action_move_down/up → ListView or ScrollableContainer navigation
    → action_open_search → push_screen(SearchScreen())
    → _render_category(index) → rebuilds main-scroll content
```

### Theme system

Each theme is a flat `dict[str, str]` with ~15 color keys.
Switching theme: `current_theme_name` reactive → `_apply_theme()` updates all widget styles inline.
No CSS rebuild needed — inline styles override the static CSS.

### Category rendering

`_render_category(index)`:
1. Clears `#main-scroll` children
2. Builds legend row (● Basic ● Intermediate ● Advanced)
3. Iterates commands, builds `Text` objects with theme colors
4. Mounts each as `Static(cmd-row)`

---

## Key Bindings

| Key | Action | Method |
|-----|--------|--------|
| `j` / `k` | Navigate down/up | `action_move_down/up` |
| `g` / `G` | Top / Bottom | `action_move_top/bottom` |
| `d` / `u` | Page down/up | `action_page_down/up` |
| `h` / `l` | Focus sidebar/content | `action_focus_sidebar/content` |
| `Enter` | Select category | `on_list_view_selected` |
| `/` | Search | `action_open_search` |
| `t` | Cycle theme | `action_cycle_theme` |
| `?` | Help | `action_show_help` |
| `q` | Quit | inherited from App |
| `r` | Refresh | `action_refresh` |

---

## Known Limitations & Future Work

### Short-term (next session)
- [ ] Category colors in sidebar: add per-category tint/color to CatListItem labels
- [ ] Keybinding tooltips in status bar could be dynamic (show current theme name + mode)
- [ ] SearchScreen: add keyboard navigation (j/k) through results
- [ ] SearchScreen: show category context inline (already done via `[cat_name]` prefix)

### Medium-term
- [ ] Config file (`~/.config/vim-cheat/config.toml`) for persistent theme preference
- [ ] Export/print command list as PDF or markdown
- [ ] Practice mode: show keybinding, user types the answer
- [ ] Plugin system for community-contributed command sets (e.g., `:set` options deep-dive, plugin-specific keymaps)

### Long-term
- [ ] i18n / multi-language descriptions
- [ ] Vim motion training mode with live feedback
- [ ] Custom command groups (user adds their own mappings)
- [ ] Neovim integration: read `:map` output and show user's actual keybindings

---

## Development Setup

```bash
cd vim-cheat
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Adding commands

Edit `CHEAT_DATA` in `vim_cheat.py`. Each command is a tuple:
```python
("keybinding", "Description of what it does", "basic|intermediate|advanced")
```

### Adding a theme

1. Add a new dict to `THEMES` with all color keys
2. Add the key name to `THEME_NAMES` (or it auto-derives from dict keys)
3. The `t` key binding cycles through all themes automatically

---

## Testing

No test suite yet. Manual verification:
```bash
# Run the app
python run.py

# Verify search screen (press /)
# Verify theme cycling (press t repeatedly)
# Verify all 9 categories render (press j/k in sidebar)
```
