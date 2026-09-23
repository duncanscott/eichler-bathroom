#!/usr/bin/env python3
"""Copy the ventilation references into GitHub Pages and refresh document lists beside each option.

Run from any directory. --check validates without writing. Only the explicitly
listed notes, installation photos and PDFs are eligible for publication.
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
DOCUMENT_SECTIONS = {
    "panasonic": ("Documents for both Panasonic layouts", (
        "Panasonic-FV-0510VS1-submittal.pdf", "Panasonic-FV-0510VS1-installation.pdf",
        "Panasonic-FV-0510VS1-service.pdf", "Panasonic-FV-0511VQ1-submittal.pdf",
        "Panasonic-FV-0511VQ1-installation.pdf", "Panasonic-FV-0511VQ1-service.pdf",
    )),
    "broan": ("Broan L100E documents", (
        "Broan-L100E-L300E-specifications.pdf", "Broan-L100E-L300E-installation.pdf",
    )),
    "broan-505": ("Earlier Broan 505 comparison documents", (
        "Broan-504-505-specifications.pdf", "Broan-504-505-installation.pdf",
    )),
    "fantech": ("REC54 and curb documents", (
        "Fantech-RE-REC-installation.pdf", "Fantech-commercial-accessories-curbs.pdf",
        "Fantech-RE-REC-brochure-performance-2010.pdf", "Fantech-RE-REC-detailed-performance-2008.pdf",
        "Fantech-RE-REC-submittal-2007.pdf", "ENERGY-STAR-ventilating-fans-historical-list.pdf",
        "405262_RE_C__OIPM_EN_20190426_185331269.pdf",
    )),
    "grilles": ("Ceiling grille documents", (
        "Hart-Cooley-RH45-submittal.pdf", "Fantech-CG-grilles-specifications-2005.pdf",
        "Fantech-accessories-catalog-2004.pdf",
    )),
    "code": ("Ventilation requirements for the contractor discussion", (
        "California-2025-CALGreen-residential-checklist.pdf",
        "California-2025-CF2R-MCH-27-H-ventilation.pdf",
    )),
}
META = {
    "Fantech-commercial-accessories-curbs.pdf": ("fantech", "Fantech roof curb specifications — 5ACC15FS", "Undated catalog excerpt · PDF page 1 (printed page 272) lists 5ACC15FS, item 49580, for REC54 / REC6. Catalog prices are historical."),
    "Fantech-RE-REC-installation.pdf": ("fantech", "RE / REC installation manual", "2021 revision · Curb / pitched-roof arrangements, dimensions and wiring. Start here."),
    "Fantech-RE-REC-brochure-performance-2010.pdf": ("fantech", "RE / REC brochure & airflow curves", "2010 · REC54 performance and typical applications; shared RE / REC series document."),
    "Fantech-RE-REC-detailed-performance-2008.pdf": ("fantech", "RE / REC detailed air & sound performance", "2008 · Historical AMCA data. Not a certified rating under §7.1, and not an HVI bathroom sound rating."),
    "Fantech-RE-REC-submittal-2007.pdf": ("fantech", "RE / REC historical submittal", "2007 · Historical ENERGY STAR claim; not evidence of a current certified rating under §7.1. Use the 2021 manual for dimensions."),
    "405262_RE_C__OIPM_EN_20190426_185331269.pdf": ("fantech", "RE / REC manual — original-filename copy", "Additional project download. Identical contents to the 2021 installation manual; retained so every downloaded file is linked."),
    "Fantech-CG-grilles-specifications-2005.pdf": ("grilles", "Fantech CG grille specifications", "2005 · CG5 / CG45 dimensions, materials, pressure and noise curves."),
    "Fantech-accessories-catalog-2004.pdf": ("grilles", "Fantech accessories catalog", "2004 · MGE5 dimensions on page 3. Confirm current dimensions before fabrication."),
    "Hart-Cooley-RH45-submittal.pdf": ("grilles", "Hart & Cooley RH45 grille submittal", "2020 drawing · Face dimensions, mounting-screw offsets and rectangular duct interface."),
    "Panasonic-FV-0511VQ1-submittal.pdf": ("alternatives", "Panasonic FV-0511VQ1 specifications", "Already installed, per owner · 7⅜-inch-deep housing; actual projection and duct route need measurement."),
    "Panasonic-FV-0511VQ1-installation.pdf": ("alternatives", "Panasonic FV-0511VQ1 installation manual", "Mounting, ceiling openings, duct guidance and electrical requirements."),
    "Panasonic-FV-0511VQ1-service.pdf": ("alternatives", "Panasonic FV-0511VQ1 service manual & grille part", "Version 1902 · PDF page 7, item 13 identifies FFV1115VQ1A Grill Assembly; exploded mounting drawing on page 3."),
    "Panasonic-FV-0510VS1-submittal.pdf": ("alternatives", "Panasonic FV-0510VS1 specifications", "Shallow indoor fan · 3⅜-inch body; compact and elongated enclosure layouts require measured dimensions."),
    "Panasonic-FV-0510VS1-installation.pdf": ("alternatives", "Panasonic FV-0510VS1 installation manual", "WhisperValue installation and duct details."),
    "Panasonic-FV-0510VS1-service.pdf": ("alternatives", "Panasonic FV-0510VS1 service manual & grille part", "Version 2502 · PDF page 6, item 9 identifies FFV3400146S Louver Assy; exploded mounting drawing on page 3."),
    "Broan-L100E-L300E-specifications.pdf": ("alternatives", "Broan L100E–L300E specifications", "L100E dimensions and HVI-2100 certified vertical-discharge ratings — the evidence for §7.1, §7.3.2 and §5.2. Broan’s product-page Title 24 entry is still unexplained."),
    "Broan-L100E-L300E-installation.pdf": ("alternatives", "Broan L100E–L300E installation manual", "Top-outlet conversion and on/off control, page 8. No custom rooftop enclosure detail."),
    "Broan-504-505-specifications.pdf": ("alternatives", "Broan 504 / 505 specifications", "Utility-fan reference · Model 505 is not listed over tubs/showers; see the published sound data."),
    "Broan-504-505-installation.pdf": ("alternatives", "Broan 504 / 505 installation manual", "Retained for completeness of the original fan comparison."),
    "California-2025-CALGreen-residential-checklist.pdf": ("code", "2025 CALGreen residential checklist", "California HCD · Bathroom ventilation requirements at §4.506.1, page 12."),
    "California-2025-CF2R-MCH-27-H-ventilation.pdf": ("code", "2025 CEC ventilation compliance form", "CF2R-MCH-27-H · §7.1 rating requirement, §7.3 remote-fan sound exception and §7.3.2 sone limits, page 6."),
    "ENERGY-STAR-ventilating-fans-historical-list.pdf": ("code", "Historical ENERGY STAR fan list", "EPA · January 9, 2009. Historical evidence, not proof of current certification."),
    "README.md": ("notes", "Full bathroom ventilation research", "Fan comparison, existing-opening implications, roof options and unresolved requirements."),
    "ceiling-grilles.md": ("notes", "Ceiling grille comparison & installation notes", "Product links, archived price observations, fit calculations and source limitations."),
    "sources.json": ("notes", "Original document source record", "Download URLs, retrieval timestamps and verification data; includes the unsuccessful county-handout download."),
    "contractor-brief.txt": ("notes", "Contractor questions — printable text", "Six questions to coordinate the roofer and ventilation/electrical installer."),
    "photos/README.md": ("notes", "Existing installation — photo observations", "Owner-supplied photo: visible fan, side duct and framing; implications and remaining measurements."),
    "existing-installation-IMG_3828.jpg": ("notes", "Existing installation — viewing photo", "JPEG viewing copy of the owner’s photo, supplied September 23, 2026. No crop or retouching."),
    "existing-installation-IMG_3828.HEIC": ("notes", "Existing installation — original photo", "Unchanged HEIC original. Download if your browser cannot display this format."),
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
    return (f'<li><a href="references/{esc(record["file"], quote=True)}">'
            f'{esc(record["title"])}</a> '
            f'<span class="document-format">({file_type} · {size_text})</span>'
            f'<p>{esc(record["note"])}</p></li>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    page_path = SITE / "index.html"
    page = page_path.read_text()
    questions = Questions()
    questions.feed(page)
    assert len(questions.questions) == 6, "Expected six contractor questions"
    brief = ("EICHLER BATHROOM — VENTILATION OPTIONS\n"
             "Contractor discussion brief | Updated: September 23, 2026\n\n"
             "Compare compact covers with exposed duct, elongated enclosures with concealed duct,\n"
             "exterior fans with ceiling grilles, and an indoor fan in a custom rooftop enclosure.\n"
             "Broan L100E remains an option. Its published HVI-2100 ratings meet the criteria in\n"
             "the 2025 CEC form (§7.1 rating, §7.3.2 sound, §5.2 airflow), but Broan’s product page\n"
             "still marks Title 24 compatibility as No; ask Broan to explain that entry in writing.\n"
             "For the Fantech REC54 the open question is a current certified rating under §7.1,\n"
             "which ranks ahead of ENERGY STAR status.\n"
             "Layout and fabrication details remain open.\n"
             "Known: no attic; tongue-and-groove ceiling directly below a flat roof;\n"
             "Panasonic FV-0511VQ1 already installed, per owner; projection unmeasured.\n"
             "Photo shows fan and side duct below the wood, with an apparent upward turn.\n"
             "A square cutout behind the fan is not visible; verify it separately from the duct hole.\n"
             "Roof layers, termination, dimensions and room size still need site verification.\n\n")
    for number, (title, body) in enumerate(questions.questions, 1):
        brief += f"{number}. {title}\n{body}\n\n"
    brief = brief.rstrip() + "\n"
    brief_path = ROOT / "contractor-brief.txt"
    if args.check:
        assert brief_path.read_text() == brief, "Contractor brief is stale"
    else:
        brief_path.write_text(brief)

    sources = sorted(ROOT.rglob("*.pdf"))
    sources += [ROOT / name for name in ("README.md", "ceiling-grilles.md", "sources.json", "contractor-brief.txt",
                                        "photos/README.md", "photos/existing-installation-IMG_3828.jpg",
                                        "photos/existing-installation-IMG_3828.HEIC")]
    records = []
    for source in sources:
        relative = source.relative_to(ROOT).as_posix()
        key = relative if relative in META else source.name
        category, title, note = META[key]
        data = source.read_bytes()
        target = SITE / "references" / relative
        if args.check:
            assert target.read_bytes() == data, f"Missing or stale public copy: {relative}"
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        records.append({"file": relative, "title": title, "category": category, "note": note,
                        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})

    pdf_records = {Path(r["file"]).name: r for r in records if r["file"].endswith(".pdf")}
    assigned = [name for _, names in DOCUMENT_SECTIONS.values() for name in names]
    assert len(assigned) == len(set(assigned)), "A PDF is assigned to more than one document list"
    assert set(assigned) == set(pdf_records), "Every PDF must have a relevant section"
    updated = page
    for key, (heading, filenames) in DOCUMENT_SECTIONS.items():
        contents = (f'<div class="section-documents" id="{key}-documents" '
                    f'aria-labelledby="{key}-documents-title">\n'
                    f'<h3 id="{key}-documents-title">{html.escape(heading)}</h3>\n'
                    '<ul class="document-list">\n'
                    + '\n'.join(render_record(pdf_records[name]) for name in filenames)
                    + '\n</ul>\n</div>')
        start = f'<!-- SECTION_DOCUMENTS:{key} START -->'
        end = f'<!-- SECTION_DOCUMENTS:{key} END -->'
        block = start + '\n' + contents + '\n    ' + end
        updated, count = re.subn(re.escape(start) + r'.*?' + re.escape(end),
                                 lambda _: block, updated, flags=re.S)
        assert count == 1, f"Expected one document block for {key}"
    inventory = json.dumps(records, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert page == updated, "Section document lists are stale"
        assert (SITE / "documents.json").read_text() == inventory, "Inventory is stale"
    else:
        page_path.write_text(updated)
        (SITE / "documents.json").write_text(inventory)
    print(f'{"Verified" if args.check else "Prepared"} {len(records)} documents, '
          f'{sum(p.suffix == ".pdf" for p in sources)} PDFs, and {len(questions.questions)} contractor questions.')


if __name__ == "__main__":
    main()
