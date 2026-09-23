# Eichler Primary Bathroom Remodel

Research, product notes, and reference images for remodeling the primary bathroom of an Eichler home (1960s, slab-on-grade, post-and-beam).

## 🔗 Live contractor page

**https://duncanscott.github.io/eichler-bathroom/**

A single scannable page pulling together the design direction, inspiration images, shower pan options, tile and slip-resistance guidance, and Eichler-specific notes for bidding. This is the link to send to contractors, architects, and designers.

It is built by GitHub Pages from the **`docs/`** folder only. Everything else in this repo is version-controlled but not served publicly.

## Start here

| File | What it is |
|---|---|
| **[DECISIONS.md](DECISIONS.md)** | What's actually been **decided** vs. what's still open. Read this first — the research folders deliberately present options, this file says which way we're going. |
| [docs/index.html](docs/index.html) | Source of the published contractor page. |
| [Bathroom ventilation options page](docs/bathroom-ventilation/index.html) | Prepared GitHub Pages reference comparing a Fantech roof fan and Panasonic shallow soffit, with installation sketches, moisture details, contractor questions, and the document library. |
| [bathroom-ventilation/](bathroom-ventilation/) | Roof-exhaust alternatives for the tongue-and-groove ceiling, comparison table, opening compatibility, and downloaded manufacturer specifications. |
| [window-coverings/](window-coverings/) | Typical Eichler window coverings: period evidence, owner discussions, practical recommendations, and a sourced image collection. |
| [fireplace-remodel/](fireplace-remodel/) | Tiled Eichler fireplace references (26 downloaded source photos), before-and-after remodel accounts, the reconstructed project discussion, and what owners and designers say about tiling over Eichler brick. |
| [master-bath-inspiration-2/](master-bath-inspiration-2/) | Second research pass: material notes, vendors, and the listing archive. |
| [master-bath-inspiration/](master-bath-inspiration/) | First research pass: 19 curated reference images with notes. |

## Current direction

Terrazzo or a terrazzo look-alike for the floor and shower base, paired with a floating wood vanity with flat slab fronts and one saturated period tile colour (green or blue leading) against an otherwise calm envelope. Full reasoning and the alternatives considered are in [DECISIONS.md](DECISIONS.md).

## The research notes

In `master-bath-inspiration-2/`:

- **[custom-terrazzo-shower-bases.md](master-bath-inspiration-2/custom-terrazzo-shower-bases.md)** — custom one-piece terrazzo pans; verified vendors (Angelozzi epoxy, Creative Industries cement, Grifform solid surface), epoxy-vs-cement, and a pre-order checklist.
- **[bathroom-terrazzo-floor.md](master-bath-inspiration-2/bathroom-terrazzo-floor.md)** — terrazzo flooring for the room itself; why grind level and sealer (not the material) set slip resistance.
- **[shower-floor-terrazzo-porcelain.md](master-bath-inspiration-2/shower-floor-terrazzo-porcelain.md)** — terrazzo-look porcelain, the ANSI A326.3 / DCOF ≥ 0.42 standard, and why the pan floor wants a mosaic.
- **[real-terrazzo-in-shower-pan.md](master-bath-inspiration-2/real-terrazzo-in-shower-pan.md)** — using real terrazzo tile underfoot: finish, format, sealing.
- **[shower-pans-terrazzo.md](master-bath-inspiration-2/shower-pans-terrazzo.md)** — pan options overall, from stock pre-tiled bases to custom.
- **[board.html](master-bath-inspiration-2/board.html)** — visual mood board (loads images live from their sources).
- **[sources.csv](master-bath-inspiration-2/sources.csv)** — every reference with page URL, image URL, and a one-line takeaway.

## Reference listing archive

`master-bath-inspiration-2/lancashire/` archives a 1964 Claude Oakland Eichler whose kitchen and baths were designed by Destination Eichler using Fireclay Tile — a built, local example of this direction.

- [listing.md](master-bath-inspiration-2/lancashire/listing.md) — full listing facts, finishes, and takeaways
- [gallery.html](master-bath-inspiration-2/lancashire/gallery.html) — browse all 86 photos offline
- `photos/` — all 86 MLS photos at full size

The live listing will disappear when the property sells; this archive won't. If `photos/` is ever missing, regenerate it:

```bash
cd master-bath-inspiration-2/lancashire
bash download-photos.sh
```

## Standing constraints for any bid

- **Asbestos:** assume any original 9″×9″ floor tile — and the black mastic under it — contains asbestos until lab-tested. Intact tile is harmless; breaking, sanding, or scraping it is not. Test first, then encapsulate or use a Cal/OSHA-registered abatement contractor (required in California above 100 sq ft at >0.1%).
- **Slab-on-grade:** relocating drains or supply lines can mean opening the slab near radiant-heating lines. Prefer solutions that keep the existing drain location.
- **Map and test** radiant heat, water, and sewer lines before demolition.
- **Post-and-beam framing** limits attic and crawl access for new duct and wiring runs.

## Notes on this repo

- GitHub Pages publishes **only `docs/`**. Adding files elsewhere will not expose them on the site.
- MLS listing photos are © CCAR / Bay East / bridgeMLS and are kept here for private design reference, not republication. They are deliberately not linked from the published page.
- `_to_delete/`, if present, is a staging folder for files awaiting removal — safe to delete.

---

*Design references are inspiration and product leads. Confirm waterproofing, ventilation, tempered-glass, electrical, slip ratings, and code requirements with the project team.*
