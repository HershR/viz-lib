# shadcn Chart Style — Breakdown

A visual analysis of the shadcn chart reference images in [`references/`](./references)
(`ShadcnBar1`, `ShadcnBar2`, `ShadcnLine1`, `ShadcnLine2`), written to guide chartcn's
`shadcn` theme. All four references are **dark mode**. Hex values below were sampled
directly from the images, so they're accurate to the source.

> **Headline finding:** the reference palette is a **two-tone blue** (a light
> periwinkle + a vivid blue), *not* the multi-hue coral/teal set. Our current
> `shadcn`/`shadcn-dark` theme uses coral/teal (light) and blue/green/orange (dark),
> which is the biggest divergence from these references. See §10.

---

## 1. Composition — the card, not just the plot

Every reference is a **Card**, and the chart is only the middle band of it. The
"shadcn look" is as much this framing as the plot itself:

- **Page** background: near-black `#080808`.
- **Card**: a slightly lighter panel `#101010`, a **thin ~1px border** (`~#181818`),
  **rounded corners** (~12px / `rounded-xl`), and generous internal **padding** (~24px).
- **Header** (top of card): a **title** (semibold, near-white) directly above a
  **description** (muted gray) — e.g. **"Bar Chart"** / "January – June 2024".
- **Footer** (bottom of card): two lines — a **bold trend line** with an up-arrow
  icon ("Trending up by 5.2% this month ↗") and a **muted caption** ("Showing total
  visitors for the last 6 months").
- The plot sits between header and footer with a **wide aspect ratio** (~2.5–3 : 1)
  and no plot border.

*(The "Bar Chart / Copy / View Code" strip above each card is the shadcn docs UI, not
part of the chart.)*

---

## 2. Color palette (sampled from the references)

| Role | Hex | Notes |
|---|---|---|
| **Series 1 — light blue** | `#88c0f8` | Primary bar/line fill in single-series charts (`ShadcnBar1`). |
| **Series 2 — vivid blue** | `#2878f8` | Second series / emphasis; dominant in `ShadcnBar2` (multiple, stacked, label). |
| Line (single) | `~#a8c8e0` | Slightly desaturated light steel-blue stroke (`ShadcnLine1`). |
| Line "white" series | `~#e8f8f8` | The lighter of the two lines in `Line - Multiple` (`ShadcnLine2`). |
| Page background | `#080808` | Behind the cards. |
| Card surface | `#101010` | The chart panel. |
| Border / gridline | `~#181818` | Card border **and** the faint horizontal gridlines (same family). |
| Title text | `~#fafafa` | Near-white, semibold. |
| Muted text (description, axis labels, footer caption) | `~#a1a1aa` | Zinc-400 gray. |

**The palette is monochromatic-blue**: a light periwinkle (`#88c0f8`) paired with a
saturated blue (`#2878f8`). Multi-series charts stay within this blue family
(light + vivid, or a near-white line + a blue line) rather than introducing new hues.

---

## 3. Bars (`ShadcnBar1`, `ShadcnBar2`)

- **Fill**: flat, single color — light blue `#88c0f8` for a single series; the vivid
  blue `#2878f8` is the second series. No borders, no gradients (though shadcn offers
  gradient variants elsewhere).
- **Rounded ends**: corners are rounded on the **data end** only and the rounding is
  **subtle** (~4–6px): top corners for vertical bars, right corners for the
  horizontal chart. The baseline end stays square.
- **Spacing**: generous category gap (~25–30% of the band); bars read as slim, well
  separated.
- **Grouped** (`Bar - Multiple`): two bars per category side by side (light + vivid
  blue), small intra-group gap.
- **Stacked** (`Bar - Stacked + Legend`): light-blue base + vivid-blue top; only the
  **top of the whole stack** is rounded; a **bottom legend** ("● Desktop ● Mobile").
- **Value labels** (two patterns):
  - *`Bar - Label`*: the value sits **above each bar** (white, small) — no y-axis.
  - *`Bar - Custom Label`* (horizontal): the **category name inside the bar** (left,
    white) **and** the value **outside** to the right (muted). Bars are the vivid blue.

---

## 4. Lines (`ShadcnLine1`, `ShadcnLine2`)

- **Stroke**: ~2px, rounded caps/joins, light blue.
- **Curve types** shown: **natural** (smooth monotone spline — the default look),
  **linear** (straight segments), and **step**. The default reference line is the
  **smooth natural curve**, which is a signature of the shadcn line look.
- **Dots** (`Line - Dots`): filled circular markers (~4–5px) at each point in the line
  color; otherwise lines carry no markers.
- **Multiple** (`Line - Multiple`): two lines — one near-white (`#e8f8f8`), one blue —
  no legend, no direct labels in the static view.
- **No area fill** in these references (line only); **no y-axis**; faint horizontal
  grid; muted x labels.

---

## 5. Axes

- **Value axis (y): hidden entirely** — no axis line, no ticks, no numbers. Values are
  read from bar labels (when present) or the tooltip (interactive).
- **Category axis (x): labels only** — muted gray (`~#a1a1aa`), ~12px, with a small
  **top margin** between the plot and the labels. **No axis line, no tick marks.**

---

## 6. Gridlines

- **Horizontal only**, **very faint** (`~#181818`, essentially the border color),
  thin, solid. Just a few lines. **No vertical gridlines.** The grid barely reads —
  it's a whisper, not a structure.

---

## 7. Typography

- Clean grotesque sans (**Inter / Geist** on the real site).
- **Hierarchy**: card **title** semibold ~16px near-white → **description** ~13px
  muted → chart → **footer** bold line + muted caption; **axis labels** ~12px muted.
- Everything is tight, small, and low-contrast except the title and the footer's
  trend line.

---

## 8. Interaction (context, out of scope for static output)

The live shadcn charts add a **hover tooltip** (a small card showing the series and
value) and a cursor highlight. These references are static, so the tooltip isn't
visible — chartcn renders static images, so this is informational only.

---

## 9. The essence, in one paragraph

A shadcn chart is a **dark card** (`#101010` on `#080808`, thin border, rounded,
padded) with a **semibold title + muted description** on top and a **bold trend +
muted caption** footer. The plot itself is **chrome-light**: **no y-axis**, **no
spines**, a **whisper-faint horizontal grid**, and **muted x labels**. Marks are a
**two-tone blue** (`#88c0f8` + `#2878f8`) — **subtly rounded bars** or **smooth 2px
lines** — with **generous spacing**. Values live in **on-mark labels** or the tooltip,
never on a value axis.

---

## 10. How chartcn's `shadcn` theme compares — gaps & recommendations

What our current `shadcn`/`shadcn-dark` theme already matches: rounded bar ends, no
spines, hidden value axis, faint horizontal-only grid, muted labels, near-black card
surface. The gaps against these references:

1. **Palette (biggest gap).** We use coral/teal (light) and blue/green/orange (dark).
   The references are **two-tone blue**: `#88c0f8` + `#2878f8`. To match *these*
   demos, `shadcn-dark`'s slots 1–2 should be light-blue + vivid-blue, and the palette
   should stay blue-monochromatic rather than multi-hue. *(Note: shadcn's own default
   `--chart-*` tokens are the coral/teal set; these particular demo screenshots use a
   blue theme. Worth confirming which target we want — the coral/teal "brand" palette
   or the blue demo palette.)*
2. **Line curve.** Reference default lines are a **smooth natural spline**; ours draw
   straight segments. Adding a smooth (`type="natural"`-style) option would match the
   signature line look.
3. **Bar radius.** ✅ Aligned — dialed our `bar_radius` down to **0.10** to match the
   references' subtle (~4–6px) rounding.
4. **Card frame + footer.** We render title + subtitle only; the references have a
   bordered, rounded, padded **card** and a **footer** (trend line + caption). A
   `caption` already exists; a subtle card background/border + a trend footer would
   complete the framing (optional, more involved in matplotlib).
5. **Value-above-bar labels.** The `Bar - Label` pattern (value centered above each
   bar, no y-axis) is very shadcn; our `label="auto"` only labels the extreme. An
   "all bars, above" label mode would match it.
6. **Neutrals.** ✅ Aligned — `shadcn-dark` now uses the reference card `#101010` and
   grid `#181818` (was `#0a0a0a` / `#27272a`).

Remaining gaps: **#1 (palette)** is intentionally left as coral/teal for now (a
deliberate choice — the references use a blue demo theme); **#2 (smooth lines)** and
**#4–5 (card frame/footer, value-above-bar labels)** are larger, optional
enhancements. The neutral/radius items (**#3, #6**) are aligned.
