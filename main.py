import json
import os
import time
from argparse import ArgumentParser


def export_arc_bookmarks(output_file: str) -> None:
    arc_data_path = os.path.expanduser(
        "~/Library/Application Support/Arc/StorableSidebar.json"
    )
    if not os.path.exists(arc_data_path):
        raise FileNotFoundError(f"Cannot find Arc data at: '{arc_data_path}'")

    with open(arc_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        sidebar_data = data["sidebar"]["containers"][1]["items"]

    sidebar_data = [record for record in sidebar_data if isinstance(record, dict)]

    folders = []
    tab_id_map = {}

    found_bookmarks = False

    for record in sidebar_data:
        # Check for tabs
        if "data" in record and "tab" in record["data"]:
            tab_id = record["id"]
            title = record["data"]["tab"]["savedTitle"]
            url = record["data"]["tab"]["savedURL"]
            tab_id_map[tab_id] = {"title": title, "url": url}
            found_bookmarks = True

        # Check for folders
        if record["title"]:
            folder_name = record["title"]
            children_ids: list = record["childrenIds"]
            folders.append({"name": folder_name, "children": children_ids})
            found_bookmarks = True

    html_content = []

    # Netscape Bookmark File Format header
    html_content.append("<!DOCTYPE NETSCAPE-Bookmark-file-1>")
    html_content.append("")
    html_content.append(
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">'
    )
    html_content.append("<Title>Arc Bookmarks</Title>")
    html_content.append("<h1>Arc Bookmarks</h1>")

    # Main bookmark list container
    html_content.append("<DL><p>")

    current_timestamp = int(time.time())

    for folder in folders:
        folder_title = (
            folder["name"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
        html_content.append(
            f'    <DT><H3 ADD_DATE="{current_timestamp}">{folder_title}</H3>'
        )
        # Container for folder contents
        html_content.append("    <DL><p>")

        for child_id in folder["children"]:
            child_title = (
                tab_id_map[child_id]["title"]
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
            )
            child_url = (
                tab_id_map[child_id]["url"]
                .replace("&", "&amp;")
                .replace('"', "&quot;")
                .replace("'", "&#x27;")  # Escape single quotes
                .replace(" ", "%20")  # Encode spaces
            )
            if child_url:
                html_content.append(
                    f'        <DT><A HREF="{child_url}" ADD_DATE="{current_timestamp}" LAST_MODIFIED="{current_timestamp}">{child_title}</A>'
                )

            del tab_id_map[child_id]
        html_content.append("    </DL><p>")  # End folder container

    for tab_data in tab_id_map.values():
        title = (
            tab_data["title"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
        url = (
            tab_data["url"]
            .replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")  # Escape single quotes
            .replace(" ", "%20")  # Encode spaces
        )
        if url:
            html_content.append(
                f'    <DT><A HREF="{url}" ADD_DATE="{current_timestamp}" LAST_MODIFIED="{current_timestamp}">{title}</A>'
            )

    # End main bookmark list
    html_content.append("</DL><p>")

    if found_bookmarks:
        with open(output_file, "w", encoding="utf-8") as of:
            of.write("\n".join(html_content))
        print(f"Successfully exported bookmarks to: {output_file}")
    else:
        print(
            "No pinned tabs (bookmarks) found using the specified structure. Output file not created."
        )


if __name__ == "__main__":
    parser = ArgumentParser(prog="ArcBookmarkExport", description="Export Arc bookmarks to HTML")
    parser.add_argument(
        "output_filename",
        nargs="?",
        default="arc_bookmarks_export.html",
        help="Specify the output HTML filename (default: arc_bookmarks_export.html)"
    )
    args = parser.parse_args()
    export_arc_bookmarks(output_file=args.output_filename)
