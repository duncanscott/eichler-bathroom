#!/usr/bin/env python3
"""Copy the ventilation references into GitHub Pages and refresh its static index.

Run from any directory. --check validates without writing. Only the explicitly
listed notes and PDFs inside bathroom-ventilation are eligible for publication.
"""
import argparse
import hashlib
import html
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT.parent / "docs" / "bathroom-ventilation"
GROUPS = {
    "fantech": "Fantech roof fans",
    "grilles": "Ceiling grilles",
    "alternatives": "Other fans considered",
    "code": "California & certification",
    "notes": "Project notes",
}
META = {
    "Fantech-commercial-accessories-curbs.pdf": ("fantech", "Fantech roof curb specifications — 5ACC15FS", "Undated catalog excerpt · PDF page 1 (printed page 272) lists 5ACC15FS, item 49580, for REC54 / REC6. Catalog prices are historical."),
    "Fantech-RE-REC-installation.pdf": ("fantech", "RE / REC installation manual", "2021 revision · Curb / pitched-roof arrangements, dimensions and wiring. Start here."),
    "Fantech-RE-REC-brochure-performance-2010.pdf": ("fantech", "RE / REC brochure & airflow curves", "2010 · RE54 / REC54 performance and typical applications."),
    "Fantech-RE-REC-detailed-performance-2008.pdf": ("fantech", "RE / REC detailed air & sound performance", "2008 · Historical AMCA data; not an HVI bathroom sound rating."),
    "Fantech-RE-REC-submittal-2007.pdf": ("fantech", "RE / REC historical submittal", "2007 · Historical ENERGY STAR claim. Use the 2021 manual for dimensions."),
    "405262_RE_C__OIPM_EN_20190426_185331269.pdf": ("fantech", "RE / REC manual — original-filename copy", "Additional project download. Identical contents to the 2021 installation manual; retained so every downloaded file is linked."),
    "Fantech-CG-grilles-specifications-2005.pdf": ("grilles", "Fantech CG grille specifications", "2005 · CG5 / CG45 dimensions, materials, pressure and noise curves."),
    "Fantech-accessories-catalog-2004.pdf": ("grilles", "Fantech accessories catalog", "2004 · MGE5 dimensions on page 3. Confirm current dimensions before fabrication."),
    "Hart-Cooley-RH45-submittal.pdf": ("grilles", "Hart & Cooley RH45 grille submittal", "2020 drawing · Face dimensions, mounting-screw offsets and rectangular duct interface."),
    "Panasonic-FV-0511VQ1-submittal.pdf": ("alternatives", "Panasonic FV-0511VQ1 specifications", "Already installed, per owner · 7⅜-inch-deep housing; actual projection and duct route need measurement."),
    "Panasonic-FV-0511VQ1-installation.pdf": ("alternatives", "Panasonic FV-0511VQ1 installation manual", "Mounting, ceiling openings, duct guidance and electrical requirements."),
    "Panasonic-FV-0511VQ1-service.pdf": ("alternatives", "Panasonic FV-0511VQ1 service manual & grille part", "Version 1902 · PDF page 7, item 13 identifies FFV1115VQ1A Grill Assembly; exploded mounting drawing on page 3."),
    "Panasonic-FV-0510VS1-submittal.pdf": ("alternatives", "Panasonic FV-0510VS1 specifications", "Proposed indoor soffit · 3⅜-inch fan body; enclosure also needs space for the side duct."),
    "Panasonic-FV-0510VS1-installation.pdf": ("alternatives", "Panasonic FV-0510VS1 installation manual", "WhisperValue installation and duct details."),
    "Panasonic-FV-0510VS1-service.pdf": ("alternatives", "Panasonic FV-0510VS1 service manual & grille part", "Version 2502 · PDF page 6, item 9 identifies FFV3400146S Louver Assy; exploded mounting drawing on page 3."),
    "Broan-L100E-L300E-specifications.pdf": ("alternatives", "Broan L100E–L300E specifications", "Includes L100E vertical-outlet airflow and sound ratings."),
    "Broan-L100E-L300E-installation.pdf": ("alternatives", "Broan L100E–L300E installation manual", "Top-outlet conversion; indoor fan housing still needs a protected enclosure."),
    "Broan-504-505-specifications.pdf": ("alternatives", "Broan 504 / 505 specifications", "Rejected candidate · Excessive sound; not the recommended shower solution."),
    "Broan-504-505-installation.pdf": ("alternatives", "Broan 504 / 505 installation manual", "Retained for completeness of the original fan comparison."),
    "California-2025-CALGreen-residential-checklist.pdf": ("code", "2025 CALGreen residential checklist", "California HCD · Bathroom ventilation requirements at §4.506.1, page 12."),
    "California-2025-CF2R-MCH-27-H-ventilation.pdf": ("code", "2025 CEC ventilation compliance form", "CF2R-MCH-27-H · Sound criteria and remote-fan exception, page 6."),
    "ENERGY-STAR-ventilating-fans-historical-list.pdf": ("code", "Historical ENERGY STAR fan list", "EPA · January 9, 2009. Historical evidence, not proof of current certification."),
    "README.md": ("notes", "Full bathroom ventilation research", "Fan comparison, existing-opening implications, roof options and unresolved requirements."),
    "ceiling-grilles.md": ("notes", "Ceiling grille comparison & installation notes", "Product links, archived price observations, fit calculations and source limitations."),
    "sources.json": ("notes", "Original document source record", "Download URLs, retrieval timestamps and verification data; includes the unsuccessful county-handout download."),
    "contractor-brief.txt": ("notes", "Contractor questions — printable text", "Ten questions to coordinate the roofer and ventilation/electrical installer."),
}


class Questions(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.capture = False
        self.questions = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div":
            if self.depth:
                self.depth += 1
            elif attrs.get("class") == "question":
                self.depth = 1
                self.questions.append([])
        if self.depth and tag in ("h3", "p"):
            self.capture = True
            self.questions[-1].append("")

    def handle_endtag(self, tag):
        if tag == "div" and self.depth:
            self.depth -= 1
        if tag in ("h3", "p"):
            self.capture = False

    def handle_data(self, data):
        if self.capture and self.depth:
            self.questions[-1][-1] += data


def render_record(record):
    esc = html.escape
    file_type = Path(record["file"]).suffix.lstrip(".").upper()
    size = record["bytes"]
    size_text = f"{size / 1_000_000:.1f} MB" if size >= 1_000_000 else f"{size / 1_000:.0f} KB"
    return (f'<article class="document" data-category="{record["category"]}">'
            f'<span class="file-badge" aria-hidden="true">{file_type}</span>'
            f'<div><a class="title" href="references/{esc(record["file"], quote=True)}">'
            f'{esc(record["title"])} <span class="small">({file_type})</span></a>'
            f'<p>{esc(record["note"])}</p></div><span class="file-meta">{size_text}</span></article>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    page_path = SITE / "index.html"
    page = page_path.read_text()
    questions = Questions()
    questions.feed(page)
    assert len(questions.questions) == 10, "Expected ten contractor questions"
    brief = ("EICHLER BATHROOM — VENTILATION OPTIONS\n"
             "Contractor discussion brief | Updated: September 23, 2026\n\n"
             "Option under consideration, not an approved construction detail.\n"
             "Known: no attic; tongue-and-groove ceiling directly below the roof;\n"
             "Panasonic FV-0511VQ1 already installed, per owner; projection unmeasured.\n"
             "Actual opening, roof layers, slope, clear depth and room size need measurement.\n\n")
    for number, (title, body) in enumerate(questions.questions, 1):
        brief += f"{number}. {title}\n{body}\n\n"
    brief = brief.rstrip() + "\n"
    brief_path = ROOT / "contractor-brief.txt"
    if args.check:
        assert brief_path.read_text() == brief, "Contractor brief is stale"
    else:
        brief_path.write_text(brief)

    sources = sorted(ROOT.rglob("*.pdf"))
    sources += [ROOT / name for name in ("README.md", "ceiling-grilles.md", "sources.json", "contractor-brief.txt")]
    records = []
    for source in sources:
        relative = source.relative_to(ROOT).as_posix()
        category, title, note = META[source.name]
        data = source.read_bytes()
        target = SITE / "references" / relative
        if args.check:
            assert target.read_bytes() == data, f"Missing or stale public copy: {relative}"
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        records.append({"file": relative, "title": title, "category": category, "note": note,
                        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})

    library = []
    for category, heading in GROUPS.items():
        group_records = sorted((r for r in records if r["category"] == category),
                               key=lambda r: list(META).index(Path(r["file"]).name))
        library.append(f'<div class="document-group"><h3>{html.escape(heading)}</h3>')
        library.extend(render_record(r) for r in group_records)
        library.append('</div>')
    block = '<!-- DOCUMENT_LIBRARY_START -->\n' + '\n'.join(library) + '\n    <!-- DOCUMENT_LIBRARY_END -->'
    updated, count = re.subn(r'<!-- DOCUMENT_LIBRARY_START -->.*?<!-- DOCUMENT_LIBRARY_END -->', block, page, flags=re.S)
    assert count == 1
    inventory = json.dumps(records, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert page == updated, "Document library is stale"
        assert (SITE / "documents.json").read_text() == inventory, "Inventory is stale"
    else:
        page_path.write_text(updated)
        (SITE / "documents.json").write_text(inventory)
    print(f'{"Verified" if args.check else "Prepared"} {len(records)} documents, '
          f'{sum(p.suffix == ".pdf" for p in sources)} PDFs, and ten contractor questions.')


if __name__ == "__main__":
    main()
