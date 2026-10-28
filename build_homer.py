import xml.etree.ElementTree as ET
import json
from pathlib import Path

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
DATA = Path("data")

corpus = {}

for work, filename in [
    ("iliad", "iliad.xml"),
    ("odyssey", "odyssey.xml")
]:
    root = ET.parse(DATA / filename).getroot()
    books = []

    for div in root.findall(".//tei:div", NS):
        if div.get("subtype", "").lower() != "book":
            continue

        number = int(div.get("n"))
        verses = []

        for line in div.findall(".//tei:l", NS):
            text = " ".join("".join(line.itertext()).split())
            verses.append({
                "line": int(line.get("n")),
                "text": text
            })

        books.append({
            "book": number,
            "verses": verses
        })

    books.sort(key=lambda b: b["book"])
    corpus[work] = books

    print(
        f"{work}: {len(books)} books, "
        f"{sum(len(b['verses']) for b in books)} verses"
    )

(DATA / "homer.json").write_text(
    json.dumps(corpus, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("Created data/homer.json")
