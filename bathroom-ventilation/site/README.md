# Ventilation GitHub Pages reference

Public page source: [`../../docs/bathroom-ventilation/index.html`](../../docs/bathroom-ventilation/index.html).

Intended URL after publication through the existing GitHub Pages setup:
<https://duncanscott.github.io/eichler-bathroom/bathroom-ventilation/>.

The existing project publishes from `/docs`. This page compares compact indoor covers with exposed ductwork, elongated enclosures with concealed ductwork, and exterior roof fans. The Broan rooftop-enclosure option remains in the comparison with a potentially serious, unresolved compliance concern. Both Panasonic models are included for the indoor layouts; no layout is identified as preferred. The standalone existing-installation section has been removed; retain the saved photo and observations as research files. It is plain HTML, CSS, JavaScript and original SVG illustrations; it requires no build service, external font, image host or JavaScript library. The main bathroom page links to it. Preparing these files does not itself publish them.

## Update the section document lists

Keep original downloaded files in `bathroom-ventilation/`. After editing the page's contractor questions or the research notes, run:

```sh
python3 bathroom-ventilation/site/sync_documents.py
python3 bathroom-ventilation/site/sync_documents.py --check
```

The script copies every PDF under `bathroom-ventilation/` plus the two research Markdown files, source record, generated contractor text brief, and explicitly listed installation-photo files and observations into the site's `references/` directory. It builds static document lists inside the relevant option sections and the `documents.json` inventory. `DOCUMENT_SECTIONS` assigns every PDF to one list; the script checks that no PDF is missing or assigned twice. New PDFs require descriptive metadata in the script. It does not copy other research folders, unlisted photos, hidden files or project decisions. The document lists work without JavaScript; JavaScript adds the ceiling-opening overlay. The contractor questions remain on the page; the print button and text-download link have been removed. The generated text brief remains in the reference files and inventory.

All public copies preserve their original bytes. The two copies of the 2021 Fantech manual have the same SHA-256 hash but both original paths are retained. The failed county PDF download has no local file; the page labels it as an external link.

PDFs appear beside Panasonic, Broan, REC54/curb and grille discussions; shared California requirements appear beside the contractor questions. Earlier Broan 505 files are in a collapsed reference block within the Broan section. Project notes remain available through contextual links; photo files remain in the inventory. Do not restore the bottom document library, search/filter controls, or a separate Project notes group.

## Content and illustration boundaries

- Open the page with the four-row `#layout-comparison` table. Each layout has an original small SVG section in `assets/layouts/`, a model label, room/roof implications and detail links. The sketches are conceptual and not to scale. The opening title is “Layouts to compare”; do not restore the former hero or priorities strip.
- `DECISIONS.md` lists the choice among Panasonic, Fantech and Broan layouts as open, with Broan compliance unresolved. Present the active layouts without ranking or personal-preference labels; dimensions, fabrication, finish, pricing and final approval remain open.
- The indoor-options section at `#panasonic` uses the saved Panasonic specifications and manual. Its new `panasonic-compact-exposed-duct.svg` is an original conceptual side section, not a dimensioned drawing. It shows a local fan cover and separate visible duct. Material, colour, duct section, transition, supports, insulation and roof details need design.
- The elongated soffit is a visible comparison option with its own sketch. Its preliminary dimensions are qualified as estimates, and the optional second grille is described without assuming active cavity ventilation. All part links remain accessible.
- Keep the compact cover on the room side of the thermal/air boundary, with sealed fan flange and duct, dry materials and service access. Any needed insulation on a visible duct section belongs in the fabricator’s finished exterior detail and dimensions. Appearance must not substitute for airflow or sealing.
- The `#broan` section covers L100E dimensions, HVI vertical-discharge performance, its 8-inch upward outlet, on/off operation and a custom rooftop enclosure concept. Keep the Broan row last in the opening table and the Broan section last in the document. Flag a potentially serious compliance issue in both places without marking L100E as excluded. Broan’s Title 24 listing is “No”; it is ENERGY STAR certified. The reason for the Title 24 entry and a project-specific compliance route remain unresolved; do not imply that a humidity control alone resolves them. Preserve that distinction and the difference between the documented outlet conversion and the unverified custom enclosure detail.
- The roof-fan section features REC54 on a curb for the flat roof; RE54 appears only as a related-model note.
- The roof illustrations are original conceptual drawings, not manufacturer installation details. Present the direct, short connection before the extended/offset route. Roof assembly, curb height, support, insulation, damper placement, waterproofing and electrical details require design. The offset route's above-roof connection into a curb/inlet enclosure is a custom concept requiring Fantech and roofer confirmation; the standard manual centers the curb over a roof opening.
- Grille illustrations use a 16-inch-wide field with 25 pixels per inch. RH45 face: 11.75 inches; CG5: 6 inches; MGE5: 6.375 inches from a historical catalog. Illustrated round-grille cover plates are 13 inches square, conditional on a large cutout being present. The photo does not establish that cutout, so a plate is not treated as automatically necessary. Product-page links provide photographs.
- The photo shows a duct penetration but does not reveal the reported cutout behind the fan. The dashed opening overlay remains a hypothetical 10.5-inch-square scenario. The Panasonic retrofit drawing specifies 10.875 inches; the actual hole remains unmeasured.
- Historical certification and AMCA sound data are not presented as current certification or HVI bathroom sound ratings.

For a local preview, serve `docs/` using any static HTTP server and open `/bathroom-ventilation/`. Verify all document copies with the check command above and inspect the page at desktop and phone widths before publishing.
