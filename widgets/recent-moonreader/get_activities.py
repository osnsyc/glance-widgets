import argparse
import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from moonreader_tools.finders import FilesystemFinder

MOONREADER_CACHE = Path("/path/to/.Moon+/Cache")
CALIBRE_DB = Path("/path/to/calibre/data/library/metadata.db")
CALIBRE_LIB = Path("/path/to/calibre/data/library/")
GLANCE_ASSETS = Path("/path/to/glance/assets")

def search_book_by_title(db_path: Path, title: str) -> Optional[Dict[str, str]]:
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT author_sort, path FROM books WHERE title = ?", (title,))
            result = cursor.fetchone()
            if result:
                return {
                    "title": title,
                    "author_sort": result[0],
                    "path": result[1]
                }
    except Exception as e:
        print(f"SQLite error: {e}")
    return None

def find_latest_book(extractor: FilesystemFinder) -> Optional[Dict[str, Any]]:
    latest_book = None
    latest_time = 0.0
    books = extractor.get_books()
    for book in books:
        if not book.last_modified:
            continue
        try:
            dt = datetime.strptime(book.last_modified, '%Y-%m-%dT%H:%M:%S')
            timestamp = dt.timestamp()
        except Exception:
            continue
        if timestamp > latest_time:
            latest_time = timestamp
            latest_book = {
                "title": book.title,
                "percentage": book.percentage,
                "last_modified": book.last_modified,
                "last_note": next(
                    (note.to_dict() for note in reversed(book.notes) if note.to_dict().get('style') == "SELECTED"),
                    ""
                )
            }
    return latest_book

def save_cover_and_update_metadata(latest_book: Dict[str, Any]) -> None:
    search_title = latest_book['title']
    result = search_book_by_title(CALIBRE_DB, search_title)
    if result:
        cover_path = CALIBRE_LIB / result['path'] / 'cover.jpg'
        target_cover = GLANCE_ASSETS / 'mr.jpg'
        if cover_path.exists():
            shutil.copy(cover_path, target_cover)
        latest_book.update({
            "title": result['title'],
            "author_sort": result['author_sort']
        })

def save_book_info(latest_book: Dict[str, Any]) -> None:
    output_path = GLANCE_ASSETS / "moonreader.json"
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(latest_book, f, ensure_ascii=False, indent=2)

def main(process_cover: bool):
    extractor = FilesystemFinder(path=str(MOONREADER_CACHE))
    latest_book = find_latest_book(extractor)
    if not latest_book:
        print("No valid Moon+ Reader books found.")
        return
    if process_cover:
        save_cover_and_update_metadata(latest_book)
    save_book_info(latest_book)
    print("Book information saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract latest book from Moon+ and optionally update cover.")
    parser.add_argument('--cover', action='store_true', help="Also copy cover.jpg and enrich metadata from Calibre DB")
    args = parser.parse_args()

    main(process_cover=args.cover)
