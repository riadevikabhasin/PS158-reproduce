"""Download the AI Index 2026 data behind Figure 9.3.1.

Figure 9.3.1, "Trust in government regulation of AI by country (% of total), 2025",
Stanford HAI AI Index Report 2026, Chapter 9 (Public Opinion).
Underlying survey: Ipsos AI Monitor 2025.

The CSV is published in HAI's public-data Google Drive folder:
https://drive.google.com/drive/folders/1zJTOg0iR0j5SijCwFutwWvDt143lW277
  -> 9. Public Opinion/Data/fig_9.3.1.csv

Usage: python get_data.py
"""

import csv
import hashlib
import urllib.request
from pathlib import Path

FILE_ID = "1dqWREnDNn8ZqpQkoL1aGSuZkZziR3qot"
URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
OUT = Path(__file__).parent / "data" / "raw" / "fig_9.3.1.csv"
EXPECTED_HEADER = ["% of respondents", "Country", "Year"]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(URL) as response:
        content = response.read()

    # Google Drive returns an HTML page instead of the file if the link breaks.
    text = content.decode("utf-8-sig")
    rows = list(csv.reader(text.splitlines()))
    if rows[0] != EXPECTED_HEADER:
        raise ValueError(f"Unexpected download (first line: {rows[0]!r}); check {URL}")

    OUT.write_bytes(content)
    print(f"Saved {len(rows) - 1} rows to {OUT}")
    print(f"SHA-256: {hashlib.sha256(content).hexdigest()}")


if __name__ == "__main__":
    main()
