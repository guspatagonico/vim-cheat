#!/usr/bin/env python3
"""
VIM Cheat Sheet — Interactive TUI App
Cross-platform (Linux, macOS, Windows)
Powered by Textual (https://textual.textualize.io/)

Author:  Gustavo Adrián Salvini <guspatagonico@gmail.com>
         https://github.com/guspatagonico
License: MIT

Usage:
    python vim_cheat.py

Keys:
    j/k       Navigate (sidebar or content area)
    g/G       Go to top / bottom
    d/u       Page down / up
    h/l       Sidebar / Content focus
    Enter     Select category (sidebar only)
    /         Search all commands (fuzzy)
    t         Cycle theme
    ?         Help
    q         Quit
"""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Static, Input, RichLog, ListView, ListItem, Label
from rich.text import Text

# ──────────────────────────────────────────────
#  THEMES
# ──────────────────────────────────────────────

Theme = dict[str, str]

THEMES: dict[str, Theme] = {
    "tokyo-night": {
        "name": "Tokyo Night",
        "type": "dark",
        "bg": "#1e1e2e",
        "sidebar_bg": "#181825",
        "sidebar_footer_bg": "#11111b",
        "bar_bg": "#2d2d3f",
        "key_bg": "#3b3b4f",
        "highlight_bg": "#313244",
        "text": "#ffffff",
        "text_desc": "#cdd6f4",
        "text_muted": "#a6adc8",
        "accent": "#89b4fa",
        "accent_on": "#ffffff",
        "basic": "#a6e3a1",
        "intermediate": "#f9e2af",
        "advanced": "#f38ba8",
        "dim_line": "#585b70",
    },
    "dracula": {
        "name": "Dracula",
        "type": "dark",
        "bg": "#282a36",
        "sidebar_bg": "#21222c",
        "sidebar_footer_bg": "#191a21",
        "bar_bg": "#343746",
        "key_bg": "#44475a",
        "highlight_bg": "#44475a",
        "text": "#f8f8f2",
        "text_desc": "#e0e0e0",
        "text_muted": "#6272a4",
        "accent": "#bd93f9",
        "accent_on": "#f8f8f2",
        "basic": "#50fa7b",
        "intermediate": "#f1fa8c",
        "advanced": "#ff5555",
        "dim_line": "#44475a",
    },
    "catppuccin-latte": {
        "name": "Catppuccin Latte",
        "type": "light",
        "bg": "#eff1f5",
        "sidebar_bg": "#e6e9ef",
        "sidebar_footer_bg": "#dce0e8",
        "bar_bg": "#dce0e8",
        "key_bg": "#ccd0da",
        "highlight_bg": "#ccd0da",
        "text": "#000000",
        "text_desc": "#4c4f69",
        "text_muted": "#6c6f85",
        "accent": "#7287fd",
        "accent_on": "#ffffff",
        "basic": "#40a02b",
        "intermediate": "#df8e1d",
        "advanced": "#d20f39",
        "dim_line": "#acb0be",
    },
    "github-light": {
        "name": "GitHub Light",
        "type": "light",
        "bg": "#ffffff",
        "sidebar_bg": "#f6f8fa",
        "sidebar_footer_bg": "#e8ecf0",
        "bar_bg": "#e8ecf0",
        "key_bg": "#d0d7de",
        "highlight_bg": "#d0d7de",
        "text": "#000000",
        "text_desc": "#24292f",
        "text_muted": "#656d76",
        "accent": "#0969da",
        "accent_on": "#ffffff",
        "basic": "#1a7f37",
        "intermediate": "#9a6700",
        "advanced": "#cf222e",
        "dim_line": "#afb8c1",
    },
}

THEME_NAMES = list(THEMES.keys())

# ──────────────────────────────────────────────
#  DATA — Comprehensive VIM Cheat Sheet
# ──────────────────────────────────────────────

Command = tuple[str, str, str]
Category = dict[str, str | list[Command]]

CHEAT_DATA: list[Category] = [
    {
        "name": "🟢  Movement",
        "commands": [
            ("h", "Move cursor left", "basic"),
            ("j", "Move cursor down", "basic"),
            ("k", "Move cursor up", "basic"),
            ("l", "Move cursor right", "basic"),
            ("w", "Jump forward to start of a word", "basic"),
            ("W", "Jump forward to start of a WORD (non-blank)", "intermediate"),
            ("e", "Jump forward to end of a word", "basic"),
            ("E", "Jump forward to end of a WORD (non-blank)", "intermediate"),
            ("b", "Jump backward to start of a word", "basic"),
            ("B", "Jump backward to start of a WORD (non-blank)", "intermediate"),
            ("0", "Jump to beginning of line", "basic"),
            ("^", "Jump to first non-blank character of line", "basic"),
            ("$", "Jump to end of line", "basic"),
            ("g_", "Jump to last non-blank character of line", "intermediate"),
            ("gg", "Go to first line of document", "basic"),
            ("G", "Go to last line of document", "basic"),
            ("5G | :5", "Go to line 5", "basic"),
            ("H", "Move to top of screen", "intermediate"),
            ("M", "Move to middle of screen", "intermediate"),
            ("L", "Move to bottom of screen", "intermediate"),
            ("zt", "Scroll screen so cursor is at top", "intermediate"),
            ("zz", "Scroll screen so cursor is at middle", "intermediate"),
            ("zb", "Scroll screen so cursor is at bottom", "intermediate"),
            ("Ctrl-d", "Scroll down half a page", "basic"),
            ("Ctrl-u", "Scroll up half a page", "basic"),
            ("Ctrl-f", "Page down (forward)", "basic"),
            ("Ctrl-b", "Page up (backward)", "basic"),
            ("%", "Jump to matching bracket/paren/brace", "basic"),
            ("{", "Jump backward to previous paragraph/block", "intermediate"),
            ("}", "Jump forward to next paragraph/block", "intermediate"),
            ("('.`)", "Jump to mark (line / exact position)", "advanced"),
            ("''", "Jump back to last jumped-from line", "advanced"),
        ],
    },
    {
        "name": "✏️  Editing",
        "commands": [
            ("i", "Insert mode — insert before cursor", "basic"),
            ("I", "Insert mode — insert at beginning of line", "basic"),
            ("a", "Insert mode — append after cursor", "basic"),
            ("A", "Insert mode — append at end of line", "basic"),
            ("o", "Open a new line below and insert", "basic"),
            ("O", "Open a new line above and insert", "basic"),
            ("s", "Delete character under cursor and insert", "basic"),
            ("S | cc", "Delete entire line and insert", "basic"),
            ("r", "Replace a single character (no insert mode)", "basic"),
            ("R", "Replace mode — overwrite characters", "intermediate"),
            ("x", "Delete character under cursor", "basic"),
            ("X", "Delete character before cursor (backspace)", "basic"),
            ("dd", "Delete current line", "basic"),
            ("dw", "Delete from cursor to start of next word", "basic"),
            ("d$ | D", "Delete from cursor to end of line", "basic"),
            ("d0", "Delete from cursor to beginning of line", "intermediate"),
            ("diw", "Delete inner word (under cursor)", "intermediate"),
            ("das", "Delete a sentence", "advanced"),
            ("dap", "Delete a paragraph", "intermediate"),
            ("cc", "Change (replace) entire line", "basic"),
            ("C", "Change to end of line", "basic"),
            ("ciw", "Change inner word", "intermediate"),
            ("ci'/ci\"/ci(", "Change inside quotes/parens", "intermediate"),
            ("cit", "Change inside HTML/XML tag", "advanced"),
            (".", "Repeat last change", "basic"),
            ("u", "Undo", "basic"),
            ("Ctrl-r", "Redo", "basic"),
            ("yy | Y", "Yank (copy) current line", "basic"),
            ("yiw", "Yank inner word", "intermediate"),
            ("p", "Paste after cursor / below current line", "basic"),
            ("P", "Paste before cursor / above current line", "basic"),
            ("xp", "Swap two characters (cut+paste)", "intermediate"),
            (">>", "Indent line", "intermediate"),
            ("<<", "Un-indent line", "intermediate"),
            ("g~", "Toggle case (motion)", "advanced"),
            ("gu", "Make lowercase (motion)", "advanced"),
            ("gU", "Make uppercase (motion)", "advanced"),
            ("~", "Toggle case of character under cursor", "intermediate"),
            ("J", "Join next line to current", "intermediate"),
            ("gJ", "Join lines without inserting space", "advanced"),
            ("Ctrl-a", "Increment number under cursor", "intermediate"),
            ("Ctrl-x", "Decrement number under cursor", "intermediate"),
        ],
    },
    {
        "name": "🔍  Search & Replace",
        "commands": [
            ("/pattern", "Search forward for pattern", "basic"),
            ("?pattern", "Search backward for pattern", "basic"),
            ("n", "Repeat search in same direction", "basic"),
            ("N", "Repeat search in opposite direction", "basic"),
            ("*", "Search forward for word under cursor", "intermediate"),
            ("#", "Search backward for word under cursor", "intermediate"),
            ("g* / g#", "Search for partial word under cursor", "advanced"),
            (":%s/old/new/g", "Replace all occurrences in file", "basic"),
            (":%s/old/new/gc", "Replace with confirmation each", "basic"),
            (":s/old/new/", "Replace first match on current line", "intermediate"),
            (":s/old/new/g", "Replace all matches on current line", "intermediate"),
            (":3,5s/old/new/g", "Replace between lines 3-5", "intermediate"),
            (":%s/old/new/gi", "Replace case-insensitive", "intermediate"),
            ("gn", "Visually select next search match (motion)", "advanced"),
            ("g;", "Jump to last edited position (changelist)", "advanced"),
            ("g,", "Jump forward in changelist", "advanced"),
        ],
    },
    {
        "name": "👁   Visual Mode",
        "commands": [
            ("v", "Start visual mode — character-wise select", "basic"),
            ("V", "Start visual mode — line-wise select", "basic"),
            ("Ctrl-v", "Start visual block mode (column select)", "basic"),
            ("gv", "Re-select last visual selection", "intermediate"),
            ("o", "Jump to other end of selection", "intermediate"),
            ("aw", "Select 'a word' (in visual mode)", "intermediate"),
            ("iw", "Select 'inner word' in visual mode", "intermediate"),
            ("ab", "Select 'a block' (parentheses block)", "advanced"),
            ("ib", "Select 'inner block' (inside parentheses)", "advanced"),
            ("aB", "Select 'a Block' (curly-brace block)", "advanced"),
            ("iB", "Select 'inner Block' (inside braces)", "advanced"),
            ("at", "Select 'a tag' (HTML/XML tag block)", "advanced"),
            ("it", "Select 'inner tag'", "advanced"),
            ("d", "Delete selection", "basic"),
            ("c", "Change selection", "intermediate"),
            ("y", "Yank (copy) selection", "basic"),
            (">", "Indent selection", "intermediate"),
            ("<", "Un-indent selection", "intermediate"),
            ("gU", "Uppercase selection", "intermediate"),
            ("gu", "Lowercase selection", "intermediate"),
            ("~", "Toggle case of selection", "intermediate"),
            ("J", "Join selected lines", "advanced"),
            ("I", "Insert at start of block selection", "advanced"),
            ("A", "Append at end of block selection", "advanced"),
        ],
    },
    {
        "name": "📂  Windows & Tabs",
        "commands": [
            (":split | :sp", "Split window horizontally", "intermediate"),
            (":vsplit | :vsp", "Split window vertically", "intermediate"),
            ("Ctrl-w w", "Cycle between windows", "intermediate"),
            ("Ctrl-w h/j/k/l", "Move to window left/down/up/right", "intermediate"),
            ("Ctrl-w H/J/K/L", "Move current window to far side", "advanced"),
            ("Ctrl-w =", "Equalize window sizes", "intermediate"),
            ("Ctrl-w _", "Maximize window height", "intermediate"),
            ("Ctrl-w |", "Maximize window width", "advanced"),
            ("Ctrl-w +/-", "Increase / decrease window height", "intermediate"),
            ("Ctrl-w >/<", "Increase / decrease window width", "advanced"),
            ("Ctrl-w q / :q", "Close current window", "intermediate"),
            ("Ctrl-w o", "Close all other windows (keep current)", "intermediate"),
            (":tabnew | :tabnew file", "Open a new tab", "intermediate"),
            ("gt | :tabn", "Go to next tab", "intermediate"),
            ("gT | :tabp", "Go to previous tab", "intermediate"),
            ("{i}gt", "Go to tab number i (e.g., 3gt)", "advanced"),
            (":tabmove +N/-N", "Move tab right/left N positions", "advanced"),
            (":tabs", "List all tabs", "intermediate"),
            (":tabclose | :tabc", "Close current tab", "intermediate"),
            (":tabonly | :tabo", "Close all other tabs", "advanced"),
        ],
    },
    {
        "name": "🏷   Marks & Registers",
        "commands": [
            ("ma", "Mark current position with mark 'a'", "intermediate"),
            ("`a", "Jump to exact position of mark 'a'", "intermediate"),
            ("'a", "Jump to line of mark 'a'", "intermediate"),
            (":marks", "List all marks", "intermediate"),
            ("`.", "Jump to last change position", "advanced"),
            (":reg", "List all registers", "advanced"),
            ('"ay', "Yank into register 'a'", "advanced"),
            ('"ap', "Paste from register 'a'", "advanced"),
            ('"ad', "Delete into register 'a'", "advanced"),
            ('"+y', "Yank into system clipboard", "intermediate"),
            ('"+p', "Paste from system clipboard", "intermediate"),
            ('"*y / "*p', "Yank/paste from selection clipboard", "advanced"),
            ("qa", "Record macro into register 'a'", "intermediate"),
            ("q", "Stop recording macro", "intermediate"),
            ("@a", "Play macro from register 'a'", "intermediate"),
            ("@@", "Repeat last macro", "intermediate"),
            ("[count]@a", "Play macro 'a' N times", "advanced"),
            (":reg a b c", "View specific registers", "advanced"),
        ],
    },
    {
        "name": "⚡  Ex Commands",
        "commands": [
            (":w", "Write (save) file", "basic"),
            (":q", "Quit current window (fails if unsaved)", "basic"),
            (":q!", "Force quit (discard changes)", "basic"),
            (":wq | :x | ZZ", "Write and quit", "basic"),
            (":wqa", "Write and quit all tabs", "intermediate"),
            (":w !sudo tee %", "Save file with sudo (Linux/macOS)", "advanced"),
            (":e!", "Reload file (discard changes)", "intermediate"),
            (":e file", "Edit another file", "intermediate"),
            (":bn | :bp", "Go to next / previous buffer", "intermediate"),
            (":bd", "Close buffer (delete)", "intermediate"),
            (":ls | :buffers", "List open buffers", "intermediate"),
            (":noh", "Clear search highlight", "basic"),
            (":set number | :set nu", "Show line numbers", "basic"),
            (":set nonumber", "Hide line numbers", "basic"),
            (":set relativenumber", "Show relative line numbers", "intermediate"),
            (":set hlsearch", "Enable search highlighting", "intermediate"),
            (":set ignorecase", "Case-insensitive search", "intermediate"),
            (":set smartcase", "Smart case (case-sensitive if caps)", "advanced"),
            (":set tabstop=4", "Set tab width to 4 spaces", "intermediate"),
            (":set expandtab", "Use spaces instead of tabs", "intermediate"),
            (":syntax on/off", "Toggle syntax highlighting", "intermediate"),
            ("Ctrl-] / :tag", "Jump to tag definition (ctags)", "advanced"),
            ("Ctrl-t", "Jump back from tag", "advanced"),
            (":g/pattern/d", "Delete all lines matching pattern", "advanced"),
            (":v/pattern/d", "Delete lines NOT matching pattern", "advanced"),
            (":!command", "Run shell command", "intermediate"),
            (":r !command", "Insert shell command output", "advanced"),
        ],
    },
    {
        "name": "🔧  Insert Mode",
        "commands": [
            ("Esc | Ctrl-c | Ctrl-[", "Exit insert mode", "basic"),
            ("Ctrl-h", "Delete character before cursor (backspace)", "basic"),
            ("Ctrl-w", "Delete word before cursor", "intermediate"),
            ("Ctrl-u", "Delete all before cursor on current line", "intermediate"),
            ("Ctrl-j | Ctrl-m", "Insert newline (Enter)", "basic"),
            ("Ctrl-t", "Indent current line one shiftwidth", "intermediate"),
            ("Ctrl-d", "Un-indent current line one shiftwidth", "intermediate"),
            ("Ctrl-r {reg}", "Insert content from register {reg}", "intermediate"),
            ("Ctrl-r =", "Insert result of expression register", "advanced"),
            ("Ctrl-k {c1}{c2}", "Insert digraph (e.g., :),  → …)", "advanced"),
            ("Ctrl-o {cmd}", "Execute one normal mode command", "intermediate"),
            ("Ctrl-v {code}", "Insert literal character by decimal code", "advanced"),
            ("Ctrl-x Ctrl-f", "Complete filename (completion menu)", "advanced"),
            ("Ctrl-x Ctrl-l", "Complete whole line", "advanced"),
            ("Ctrl-n / Ctrl-p", "Word completion (next/previous)", "advanced"),
            ("Ctrl-e", "Insert character below cursor", "advanced"),
            ("Ctrl-y", "Insert character above cursor", "advanced"),
            ("Ctrl-a", "Insert previously inserted text", "advanced"),
            ("Ctrl-@", "Insert previously inserted text and exit", "advanced"),
        ],
    },
    {
        "name": "🧠  Advanced & Tips",
        "commands": [
            ("g;", "Cycle backward through changelist", "advanced"),
            ("g,", "Cycle forward through changelist", "advanced"),
            ("gf", "Open file under cursor", "intermediate"),
            ("gx", "Open URL under cursor in browser", "advanced"),
            ("K", "Open keyword under cursor (man / help)", "intermediate"),
            ("ga", "Show hex/ASCII value of character under cursor", "advanced"),
            ("g8", "Show UTF-8 bytes of character under cursor", "advanced"),
            ("[i", "Show match for keyword under cursor", "advanced"),
            ("[I", "Show all matches for keyword", "advanced"),
            ("[c / ]c", "Previous / next diff hunk (vimdiff)", "advanced"),
            ("do | :diffget", "Get changes from other window (vimdiff)", "advanced"),
            ("dp | :diffput", "Put changes to other window (vimdiff)", "advanced"),
            ("z=5", "Suggest spelling corrections (position 5)", "advanced"),
            ("zg", "Add word to spell dictionary", "advanced"),
            ("zw", "Mark word as incorrect (spell)", "advanced"),
            ("zug", "Revert zg/zw for word", "advanced"),
            (":set spell spelllang=en_us", "Enable English spell check", "intermediate"),
            ("q:", "Open command-line window (edit commands)", "advanced"),
            ("q/", "Open search history window", "advanced"),
            (":r file", "Insert content of file below cursor", "intermediate"),
            (":r!cmd", "Insert output of shell command", "advanced"),
            ("gq{motion}", "Format/reflow text (hard-wrap)", "advanced"),
            ("gqq", "Format current line", "advanced"),
            ("gp", "Paste and leave cursor after pasted text", "advanced"),
            ("gP", "Paste before and leave cursor", "advanced"),
            ("[count]z.", "Center screen on line N", "advanced"),
        ],
    },
]


# ──────────────────────────────────────────────
#  SEARCH SCREEN
# ──────────────────────────────────────────────

class SearchScreen(ModalScreen[None]):
    """Full-screen search with live results."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._all_commands: list[tuple[str, str, str, str]] = []
        for cat in CHEAT_DATA:
            cat_name = str(cat["name"])
            for key, desc, diff in cat["commands"]:
                self._all_commands.append((cat_name, key, desc, diff))

    @property
    def _theme(self) -> Theme:
        return self.app.theme_data  # type: ignore[attr-defined]

    def compose(self) -> ComposeResult:
        with Vertical(id="search-dialog"):
            yield Input(
                placeholder="  🔍 Type to search VIM commands...",
                id="search-input",
            )
            yield RichLog(
                id="search-results",
                highlight=True,
                markup=True,
            )
            yield Static(id="search-info")

    def on_mount(self) -> None:
        t = self._theme
        dlg = self.query_one("#search-dialog")
        dlg.styles.background = t["bg"]
        dlg.styles.border = ("thick", t["accent"])
        inp = self.query_one("#search-input", Input)
        inp.styles.background = t["key_bg"]
        inp.styles.color = t["text"]
        inp.styles.border = "none"
        self.query_one("#search-results", RichLog).styles.background = t["bg"]
        info = self.query_one("#search-info", Static)
        info.styles.color = t["text_muted"]
        info.styles.text_align = "center"
        self.query_one("#search-input", Input).focus()
        self._update_results("")

    def on_input_changed(self, event: Input.Changed) -> None:
        self._update_results(event.value)

    def _update_results(self, query: str) -> None:
        results = self.query_one("#search-results", RichLog)
        results.clear()
        q = query.strip().lower()
        t = self._theme

        if not q:
            results.write(
                Text("  Type to search commands by key or description...", style=f"dim {t['text_muted']}")
            )
            self.query_one("#search-info", Static).update("")
            return

        matches = []
        for cat_name, key, desc, diff in self._all_commands:
            if q in key.lower() or q in desc.lower():
                matches.append((cat_name, key, desc, diff))

        if not matches:
            results.write(Text(f"  No matches for '{query}'", style=f"bold {t['advanced']}"))
            self.query_one("#search-info", Static).update("0 results")
            return

        dc = {"basic": t["basic"], "intermediate": t["intermediate"], "advanced": t["advanced"]}
        for cat_name, key, desc, diff in matches:
            badge_color = dc.get(diff, t["dim_line"])
            badge = diff[0].upper()
            row = Text()
            row.append(f"  [{cat_name}]", style=f"dim {t['accent']}")
            row.append("  ")
            row.append(f"{key:<24}", style=f"bold {t['text']} on {t['key_bg']}")
            row.append("  ")
            row.append(desc, style=t["text_desc"])
            row.append("  ")
            row.append(f"[{badge}]", style=f"bold {badge_color}")
            results.write(row)

        self.query_one("#search-info", Static).update(
            f"{len(matches)} match{'es' if len(matches) != 1 else ''}"
        )


# ──────────────────────────────────────────────
#  CATEGORY LIST ITEM
# ──────────────────────────────────────────────

class CatListItem(ListItem):
    """A list item representing a category in the sidebar."""

    def __init__(self, name: str, index: int) -> None:
        self.cat_index = index
        super().__init__(Label(Text(f"  {name}")))


# ──────────────────────────────────────────────
#  MAIN APP
# ──────────────────────────────────────────────

class VimCheatApp(App):
    """Interactive VIM Cheat Sheet TUI App."""

    TITLE = "VIM Cheat Sheet"

    current_theme_name: str = reactive("tokyo-night")  # type: ignore[assignment]

    CSS = """
    VimCheatApp {
        background: #1e1e2e;
    }
    #top-bar { height: 3; background: #2d2d3f; color: #ffffff; padding: 0 0; }
    #sidebar { width: 28; min-width: 24; background: #000000; }
    #sidebar-title { height: 1; text-align: center; padding: 0 1; text-style: bold; background: #181825; }
    #category-list { height: 1fr; background: #181825; }
    #sidebar-footer { height: 1; text-align: center; background: #181825; color: #a6adc8; }
    #main-area { height: 1fr; width: 1fr; }
    #main-area-header { height: 1; padding: 0 1; text-style: bold; background: #2d2d3f; color: #ffffff; }
    #main-scroll { height: 1fr; overflow-y: auto; overflow-x: hidden; padding: 0 1; }
    .cmd-row { padding: 0; }
    #status-bar { height: 1; background: #2d2d3f; color: #a6adc8; }
    #status-bar > Static { padding: 0 1; }
    ListView { background: transparent; }
    ListView:focus { border: none; }
    ListItem { padding: 0; background: #181825; }
    ListItem > Label { padding: 0; background: #181825; }
    """

    BINDINGS = [
        Binding("j", "move_down", "Down", show=False),
        Binding("k", "move_up", "Up", show=False),
        Binding("g", "move_top", "Top", show=False),
        Binding("G", "move_bottom", "Bottom", show=False),
        Binding("/", "open_search", "Search"),
        Binding("h", "focus_sidebar", "Sidebar", show=False),
        Binding("l", "focus_content", "Content", show=False),
        Binding("q", "quit", "Quit"),
        Binding("?", "show_help", "Help"),
        Binding("r", "refresh", "Refresh", show=False),
        Binding("d", "page_down", "PgDown", show=False),
        Binding("u", "page_up", "PgUp", show=False),
        Binding("t", "cycle_theme", "Theme"),
    ]

    def __init__(self) -> None:
        self._dom_ready = False
        super().__init__()
        self._current_category_index = 0

    @property
    def theme_data(self) -> Theme:
        return THEMES[self.current_theme_name]

    def compose(self) -> ComposeResult:
        yield Static("  ╔══════════════════════════════════════════════╗\n"
                     "  ║         V I M   C H E A T   S H E E T        ║\n"
                     "  ╚══════════════════════════════════════════════╝",
                     id="top-bar")

        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static("  📚 CATEGORIES", id="sidebar-title")
                items = [CatListItem(str(c["name"]), i) for i, c in enumerate(CHEAT_DATA)]
                yield ListView(*items, id="category-list")
                yield Static("  ? help  \\  / search  \\  t theme  \\  q quit", id="sidebar-footer")

            with Vertical(id="main-area"):
                yield Static("", id="main-area-header")
                yield ScrollableContainer(id="main-scroll")

        yield Static(id="status-bar")

    # ── Theme ──────────────────────────────────

    def watch_current_theme_name(self, old_name: str, new_name: str) -> None:
        if not self._dom_ready:
            return
        self._apply_theme()

    def _apply_theme(self) -> None:
        t = self.theme_data

        # App bg
        self.styles.background = t["bg"]

        # Top bar
        self.query_one("#top-bar").styles.background = t["bar_bg"]
        self.query_one("#top-bar").styles.color = t["text"]

        # Sidebar
        sidebar = self.query_one("#sidebar")
        sidebar.styles.background = t["sidebar_bg"]
        sidebar.styles.border_right = ("solid", t["accent"])

        # Sidebar category list
        cat_list = self.query_one("#category-list", ListView)
        cat_list.styles.background = t["sidebar_bg"]

        # Sidebar title — same bg as sidebar, accent text
        title = self.query_one("#sidebar-title")
        title.styles.background = t["sidebar_bg"]
        title.styles.color = t["accent"]

        # Sidebar footer — same bg as sidebar
        footer = self.query_one("#sidebar-footer")
        footer.styles.background = t["sidebar_bg"]
        footer.styles.color = t["text_muted"]

        # Main area header
        mh = self.query_one("#main-area-header")
        mh.styles.background = t["bar_bg"]
        mh.styles.color = t["text"]

        # Status bar
        sb = self.query_one("#status-bar")
        sb.styles.background = t["bar_bg"]
        sb.styles.color = t["text_muted"]

        # Sidebar items — explicit bg matching sidebar, highlight uses accent
        lv = self.query_one("#category-list", ListView)
        for li in lv.query(ListItem):
            li.styles.background = t["sidebar_bg"]
            label = li.query_one(Label)
            if label:
                label.styles.color = t["text_desc"]
                label.styles.background = t["sidebar_bg"]
        # Highlighted item — accent background for maximum contrast
        try:
            idx = lv.index
            highlighted = lv.children[idx]
            highlighted.styles.background = t["accent"]
            hl_label = highlighted.query_one(Label)
            if hl_label:
                hl_label.styles.background = t["accent"]
                hl_label.styles.color = t["accent_on"]
        except (IndexError, TypeError):
            pass

        # Re-render content
        self._render_category(self._current_category_index)

        # Update status bar
        theme_type = t["type"]
        icon = "🌙" if theme_type == "dark" else "☀️"
        sb.update(
            f"  j↓  k↑  g/G top/bot  /search  ?help  q:quit  h/l:pane  t:theme  "
            f"{icon} {t['name']}"
        )

    # ── Rendering ──────────────────────────────

    def _render_category(self, index: int) -> None:
        if index < 0 or index >= len(CHEAT_DATA):
            return

        cat = CHEAT_DATA[index]
        name = str(cat["name"])
        commands = list(cat["commands"])
        self._current_category_index = index
        t = self.theme_data

        scroll = self.query_one("#main-scroll", ScrollableContainer)
        scroll.remove_children()

        header = self.query_one("#main-area-header", Static)
        header.update(f"  {name}  —  {len(commands)} commands")

        # Legend
        legend = Text()
        legend.append("  ● ", style=f"bold {t['basic']}")
        legend.append("Basic  ", style=t["basic"])
        legend.append("● ", style=f"bold {t['intermediate']}")
        legend.append("Intermediate  ", style=t["intermediate"])
        legend.append("● ", style=f"bold {t['advanced']}")
        legend.append("Advanced", style=t["advanced"])
        scroll.mount(Static(legend))
        scroll.mount(Static(Text("  " + "─" * 60, style=f"dim {t['dim_line']}")))

        # Command rows
        dc = {"basic": t["basic"], "intermediate": t["intermediate"], "advanced": t["advanced"]}
        for key, desc, difficulty in commands:
            badge_color = dc.get(difficulty, t["dim_line"])
            badge = difficulty[0].upper()
            row = Text()
            row.append("  ")
            row.append(f"{key:<24}", style=f"bold {t['text']} on {t['key_bg']}")
            row.append("  ")
            row.append(desc, style=t["text_desc"])
            row.append("    ")
            row.append(f"[{badge}]", style=f"bold {badge_color}")
            scroll.mount(Static(row, classes="cmd-row"))

        scroll.scroll_home(animate=False)

    # ── Navigation Actions ─────────────────────

    def action_move_down(self) -> None:
        focused = self.focused
        if focused and getattr(focused, "id", None) == "category-list":
            self.query_one("#category-list", ListView).action_cursor_down()
        else:
            self.query_one("#main-scroll", ScrollableContainer).scroll_down()

    def action_move_up(self) -> None:
        focused = self.focused
        if focused and getattr(focused, "id", None) == "category-list":
            self.query_one("#category-list", ListView).action_cursor_up()
        else:
            self.query_one("#main-scroll", ScrollableContainer).scroll_up()

    def action_move_top(self) -> None:
        focused = self.focused
        if focused and getattr(focused, "id", None) == "category-list":
            lv = self.query_one("#category-list", ListView)
            lv.index = 0
        else:
            self.query_one("#main-scroll", ScrollableContainer).scroll_home(animate=False)

    def action_move_bottom(self) -> None:
        focused = self.focused
        if focused and getattr(focused, "id", None) == "category-list":
            lv = self.query_one("#category-list", ListView)
            lv.index = len(CHEAT_DATA) - 1
        else:
            self.query_one("#main-scroll", ScrollableContainer).scroll_end(animate=False)

    def action_page_down(self) -> None:
        self.query_one("#main-scroll", ScrollableContainer).scroll_page_down()

    def action_page_up(self) -> None:
        self.query_one("#main-scroll", ScrollableContainer).scroll_page_up()

    def action_open_search(self) -> None:
        self.push_screen(SearchScreen())

    def action_focus_sidebar(self) -> None:
        self.query_one("#category-list", ListView).focus()

    def action_focus_content(self) -> None:
        self.query_one("#main-scroll", ScrollableContainer).focus()

    def action_cycle_theme(self) -> None:
        idx = THEME_NAMES.index(self.current_theme_name)
        self.current_theme_name = THEME_NAMES[(idx + 1) % len(THEME_NAMES)]
        self.notify(
            f"Theme: {self.theme_data['name']} ({'🌙 dark' if self.theme_data['type'] == 'dark' else '☀️ light'})",
            timeout=2,
        )

    def action_show_help(self) -> None:
        self.notify(
            "VIM Cheat Sheet  •  Navigation\n\n"
            "  j/k  — Navigate (sidebar or content)\n"
            "  g/G  — Top / Bottom\n"
            "  d/u  — Page down / up\n"
            "  h/l  — Sidebar / Content focus\n"
            "  Enter — Select category from sidebar\n"
            "  /    — Search all commands\n"
            "  t    — Cycle theme (dark/light)\n"
            "  r    — Refresh\n"
            "  ?    — This help\n"
            "  q    — Quit",
            title="Help",
            timeout=8,
        )

    def action_refresh(self) -> None:
        self._render_category(self._current_category_index)

    # ── Event Handlers ─────────────────────────

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if event.item is None:
            return
        item = event.item
        if hasattr(item, "cat_index"):
            self._render_category(item.cat_index)
            # Re-style all items then highlight the current one
            t = self.theme_data
            lv = self.query_one("#category-list", ListView)
            for li in lv.children:
                li.styles.background = t["sidebar_bg"]
                label = li.query_one(Label)
                if label:
                    label.styles.color = t["text_desc"]
                    label.styles.background = t["sidebar_bg"]
            event.item.styles.background = t["accent"]
            hl_label = event.item.query_one(Label)
            if hl_label:
                hl_label.styles.background = t["accent"]
                hl_label.styles.color = t["accent_on"]

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.query_one("#main-scroll", ScrollableContainer).focus()

    def on_mount(self) -> None:
        self._dom_ready = True
        self._apply_theme()
        self.query_one("#category-list", ListView).focus()
        total = sum(len(c["commands"]) for c in CHEAT_DATA)
        self.SUB_TITLE = f"{len(CHEAT_DATA)} categories · {total} commands"


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────

def main() -> None:
    app = VimCheatApp()
    app.run()


if __name__ == "__main__":
    main()
