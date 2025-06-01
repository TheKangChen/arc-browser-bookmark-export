# Arc Bookmarks Export

Export your bookmarks from the Arc browser to an HTML file that can be imported by other browsers.

---

## Setup

1. Make sure you have Python **3.12** or above installed. You can check your version in your terminal:

```bash
python3 --version
```

## Export Bookmarks

To export your Arc bookmarks, run the script from your terminal.

> ❗ **Important:** Close any mini Arc windows and floating video players, leaving only the main Arc browser window open before you run the export script.

```bash
python3 main.py <optional_file_destination>
```

*If you don't provide a file destination, the bookmarks will be saved to `./arc_bookmarks_export.html` by default.*
