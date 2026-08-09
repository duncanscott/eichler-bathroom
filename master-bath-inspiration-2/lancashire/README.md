# Reference Listing Archive — 1279 Lancashire Dr, Concord (MLS #41144292)

Archived August 9, 2026. A 1964 Claude Oakland Eichler, currently listed, whose kitchen and baths were designed by **Destination Eichler** using **Fireclay Tile** — the same designer/tile pairing already in this project's research. It is effectively a built, local example of the direction we've been circling. Archived because the listing page will disappear once the property sells.

Full details and takeaways: **`listing.md`**
Photo index: **`gallery.html`**

## What's here

| File | What it is |
|---|---|
| `listing.md` | Archived listing facts, description, and remodel-relevant takeaways. |
| `gallery.html` | Contact sheet of all 86 photos; bathroom shots highlighted. Uses local files if downloaded, otherwise loads live. |
| `photo-urls.txt` | All 86 full-size photo URLs in listing order. |
| `photos.csv` | Photo number, filename, URL, notes on the known bathroom shots. |
| `download-photos.sh` | Run once with internet to fetch all 86 into `photos/`. |
| `01-primary-bath-vanity-closeup.jpg` | **The vanity, straight on** — MLS photo 46. |
| `02-primary-bath-vanity-wide.jpg` | **Same vanity, wide** — MLS photo 45. |
| `03-second-bath-vanity.jpg` | **Second bath** — MLS photo 37. |

## To preserve every image

The three vanity images are already saved as files. The other 83 are recorded as URLs, because the environment that built this archive has no direct internet access to the photo CDN. To pull them all down at full size:

```bash
cd master-bath-inspiration-2/lancashire   # or wherever this folder lives
bash download-photos.sh
```

That fills `photos/` with `01.jpg`–`86.jpg` and makes `gallery.html` fully self-contained offline. Do it before the listing sells — the URLs die with the listing.

## Key corrections from the listing text

Worth noting, because the photos are misleading on both counts:

- The warm wood vanities are **custom Sequoia bamboo cabinetry**, not walnut.
- The gray speckled bathroom floor is **period-correct VCT** (vinyl composition tile), **not terrazzo**. It's a cheap, authentic-to-the-era way to get a speckled mid-century floor — but VCT is not suitable inside a wet shower pan, so it doesn't replace the terrazzo/porcelain work in `../shower-floor-terrazzo-porcelain.md`.

## Why the vanity is worth copying

Flat slab fronts with continuous vertical grain across the doors, small round recessed chrome pulls, a counter running wall-to-wall with integrated sinks, a full-width mirrored medicine cabinet instead of separate mirrors, a linear light bar above, and a shaped hex tile (gray in the primary, white in the second bath) rather than plain subway. Both baths keep the original compact Eichler footprint and gain presence from the long counter, the skylight, and the wall of mirror — not from expanding the room. That's the most transferable idea here.

MLS listing images © CCAR / Bay East / bridgeMLS 2026, saved for private design reference. Deliberately **not** published to the public contractor site.
