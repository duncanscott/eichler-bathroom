# Ventilation GitHub Pages reference

Public page source: [`../../docs/bathroom-ventilation/index.html`](../../docs/bathroom-ventilation/index.html).

Intended URL after publication through the existing GitHub Pages setup:
<https://duncanscott.github.io/eichler-bathroom/bathroom-ventilation/>.

The existing project publishes from `/docs`. This addition compares the Fantech roof fan with a Panasonic FV-0510VS1 in an indoor soffit. It is plain HTML, CSS, JavaScript and original SVG illustrations; it requires no build service, external font, image host or JavaScript library. The main bathroom page links to it. Preparing these files does not itself publish them.

## Update the document library

Keep original downloaded files in `bathroom-ventilation/`. After editing the page's contractor questions or the research notes, run:

```sh
python3 bathroom-ventilation/site/sync_documents.py
python3 bathroom-ventilation/site/sync_documents.py --check
```

The script copies every PDF under `bathroom-ventilation/` plus the two research Markdown files, source record and generated contractor text brief into the site's `references/` directory. It builds the static, categorized document list and `documents.json` inventory. New PDFs require descriptive metadata in the script. It does not copy other research folders, photos, hidden files or project decisions. The library works without JavaScript; JavaScript adds filtering and the ceiling-opening overlay.

All public copies preserve their original bytes. The two copies of the 2021 Fantech manual have the same SHA-256 hash but both original paths are retained. The failed county PDF download has no local file; the page labels it as an external link.

## Content and illustration boundaries

- Product selection remains open. No changes to `DECISIONS.md`.
- The Panasonic soffit section at `#panasonic` uses existing saved specifications and the installation manual. Its 16–18-inch width, 48–60-inch length and 6–8-inch finished drop are provisional mock-up allowances, not manufacturer dimensions or a confirmed fit. Its original section drawing shows the side duct and roof turn; actual bend radius, insulation, headroom, framing and roof layers require design.
- The proposed soffit is on the indoor side of the thermal/air boundary, with sealed fan flange and duct, dry construction and inspection access. Side vents are discussed as an unverified alternative, not a guarantee of drying or a manufacturer-prohibited feature. Sources and the distinction between published guidance and project inference are visible on the page.
- The roof illustrations are original conceptual drawings, not manufacturer installation details. They show direct and offset routes. Roof assembly, curb height, support, insulation, damper placement, waterproofing and electrical details require design. The offset route's above-roof connection into a curb/inlet enclosure is a custom concept requiring Fantech and roofer confirmation; the standard manual centers the curb over a roof opening.
- Grille illustrations use a 16-inch-wide field with 25 pixels per inch. RH45 face: 11.75 inches; CG5: 6 inches; MGE5: 6.375 inches from a historical catalog. Proposed round-grille cover plates are 13 inches square. Product-page links provide photographs.
- The dashed opening overlay assumes 10.5 inches square. The Panasonic retrofit drawing specifies 10.875 inches; the actual hole remains unmeasured.
- Historical certification and AMCA sound data are not presented as current certification or HVI bathroom sound ratings.

For a local preview, serve `docs/` using any static HTTP server and open `/bathroom-ventilation/`. Verify all document copies with the check command above and inspect the page at desktop and phone widths before publishing.
