"""Generate an HTML syllabus that includes a diploma policy matrix.

The script reads diploma policy alignment scores for a given course code
from a SQLite database and renders them inside a 5x2 HTML table.  The
resulting HTML document is written to disk and can be embedded or served
in a web page.
"""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple

# Order and metadata for the diploma policy table.
POLICY_ITEMS: List[Tuple[str, str]] = [
    ("DP1", "基礎的な知識・理解"),
    ("DP2", "専門的な知識・技能"),
    ("DP3", "課題解決力"),
    ("DP4", "コミュニケーション能力"),
    ("DP5", "自己管理・主体性"),
]

DB_FILENAME = "syllabus.db"
TABLE_NAME = "diploma_policy_scores"


def ensure_database(path: Path) -> None:
    """Create the database schema and a small sample dataset if necessary."""
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                course_code TEXT NOT NULL,
                policy_code TEXT NOT NULL,
                score INTEGER NOT NULL,
                PRIMARY KEY (course_code, policy_code)
            )
            """
        )

        # Provide a minimal sample so the script can be executed immediately
        # after cloning the repository.
        sample_entries = [
            ("CS101", "DP1", 3),
            ("CS101", "DP2", 4),
            ("CS101", "DP3", 5),
            ("CS101", "DP4", 4),
            ("CS101", "DP5", 3),
        ]
        cursor.executemany(
            f"INSERT OR IGNORE INTO {TABLE_NAME} (course_code, policy_code, score) VALUES (?, ?, ?)",
            sample_entries,
        )
        conn.commit()


def fetch_policy_scores(path: Path, course_code: str) -> Dict[str, int]:
    """Return a mapping of policy code to score for the specified course."""
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT policy_code, score FROM {TABLE_NAME} WHERE course_code = ?",
            (course_code,),
        )
        return {policy: score for policy, score in cursor.fetchall()}


def build_policy_table_rows(score_map: Dict[str, int]) -> str:
    """Construct the HTML table rows for the diploma policy table."""
    rows: List[str] = []
    for code, description in POLICY_ITEMS:
        score = score_map.get(code, "-")
        rows.append(f"                <tr><th>{code}: {description}</th><td>{score}</td></tr>")
    return "\n".join(rows)


def render_html(course_code: str, course_title: str, score_map: Dict[str, int]) -> str:
    """Render the final syllabus HTML document."""
    table_rows = build_policy_table_rows(score_map)
    return f"""
<!DOCTYPE html>
<html lang=\"ja\">
<head>
    <meta charset=\"UTF-8\">
    <title>{course_title} シラバス</title>
    <style>
        body {{ font-family: 'Segoe UI', 'Hiragino Kaku Gothic ProN', Meiryo, sans-serif; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            max-width: 600px;
            margin: 1rem 0;
        }}
        th, td {{
            border: 1px solid #666;
            padding: 0.5rem;
            text-align: left;
        }}
        th {{
            background-color: #f0f0f0;
            width: 70%;
        }}
        caption {{
            text-align: left;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{course_title} シラバス</h1>
        <p><strong>授業コード:</strong> {course_code}</p>
    </header>
    <section>
        <h2>ディプロマ・ポリシーとの対応</h2>
        <table>
            <caption>ディプロマ・ポリシー適合度</caption>
            <thead>
                <tr><th>項目</th><td>達成度</td></tr>
            </thead>
            <tbody>
{table_rows}
            </tbody>
        </table>
    </section>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an HTML syllabus page")
    parser.add_argument("course_code", help="Course code used to look up policy scores")
    parser.add_argument(
        "--course-title",
        default="サンプル授業",
        help="Course title to display in the syllabus header",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("syllabus.html"),
        help="Path of the HTML file to create",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=Path(DB_FILENAME),
        help="Path to the SQLite database file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    db_path: Path = args.database

    ensure_database(db_path)
    scores = fetch_policy_scores(db_path, args.course_code)

    html = render_html(args.course_code, args.course_title, scores)
    args.output.write_text(html, encoding="utf-8")
    print(f"Generated syllabus HTML at {args.output}")


if __name__ == "__main__":
    main()
