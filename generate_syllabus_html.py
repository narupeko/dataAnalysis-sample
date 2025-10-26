"""Generate an HTML syllabus that includes a diploma policy matrix.

The script reads diploma policy alignment scores for a given course code
from a CSV file and renders them inside a 5x2 HTML table. The resulting
HTML document is written to disk and can be embedded or served in a web
page.
"""
from __future__ import annotations

import argparse
import csv
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

CSV_FILENAME = "diploma_policy_scores.csv"


def fetch_policy_scores(path: Path, course_code: str) -> Dict[str, int]:
    """Return a mapping of policy code to score for the specified course."""

    with path.open(encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        scores: Dict[str, int] = {}
        for row in reader:
            if row.get("course_code") != course_code:
                continue
            policy_code = row.get("policy_code")
            score = row.get("score")
            if not policy_code or score is None:
                continue
            try:
                scores[policy_code] = int(score)
            except ValueError:
                # Ignore malformed score entries instead of raising.
                continue
    return scores


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
        "--csv",
        type=Path,
        default=Path(CSV_FILENAME),
        help="Path to the CSV file that stores diploma policy scores",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    csv_path: Path = args.csv

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file '{csv_path}' not found. Please provide a file with diploma policy data."
        )

    scores = fetch_policy_scores(csv_path, args.course_code)

    html = render_html(args.course_code, args.course_title, scores)
    args.output.write_text(html, encoding="utf-8")
    print(f"Generated syllabus HTML at {args.output}")


if __name__ == "__main__":
    main()
