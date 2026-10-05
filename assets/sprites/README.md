# Office redesign — Pokémon Emerald style

Design mockup (canvas): https://claude.ai/artifact/CKcj1bLayzc3GD6bwkhM7C

Reference markup for the mockup is in `../../design/mockup/` (`Main.dc.html` = office map,
`Sprites.dc.html` = sprite & tile sheet). Those files use a design-canvas runtime, so read
them for layout, colours and CSS values; they don't run on their own.

## Sprite files

All PNGs are native pixel size. Render at 2x with `image-rendering: pixelated`.

| File | Size | Layout |
|---|---|---|
| `npc_v1.png` … `npc_v8.png` | 64×88 | 16×22 cells. Columns: stand, stepL, stand, stepR. Rows: down, up, left, right. |
| `desk_pc.png` | 32×30 | Wooden desk with a beige CRT PC, keyboard, mug and papers. |
| `chair.png` | 14×14 | Office chair, shown at empty desks. |
| `brain.png` | 160×72 | 2 frames of 80×72 side by side. Alternate them for blinking rack lights. Screen area: x 22–57, y 5–32. |

Character variants: v1 red cap · v2 short brown hair · v3 long blonde hair · v4 short black hair ·
v5 blue cap · v6 long brown hair · v7 grey hair · v8 long dark hair.

`src/gen.py` and `src/brain.py` regenerate the PNGs (Python + Pillow). They write output next
to themselves.

## Prompt for Claude Code

```
Redesign the office view in the style of Pokémon Emerald (GBA), matching the mockup in
design/mockup and the sprites in assets/sprites (see assets/sprites/README.md). Keep all
existing data and behaviour. Only change the visuals, layout and movement.

ASSETS (PNG sprite sheets, render at 2x with image-rendering: pixelated)
- npc_v1.png … npc_v8.png: character sheets. Each cell is 16x22. 4 columns = stand, stepL, stand, stepR.
  4 rows = down, up, left, right. 8 characters (cap, short hair, long hair, with colour swaps).
- desk_pc.png (32x30): wooden desk with a beige CRT PC, keyboard, mug and papers.
- chair.png (14x14): purple office chair, shown at empty desks.
- brain.png: 2 frames of 80x72 side by side, for The Brain mainframe.

LAYOUT
- Pod width is automatic: cols = ceil(deskCount / 2); width = 80*cols + 80 px. Every pod has 2 desk rows.
  Beta 6 → 320px, Emails 5 → 320px, Alpha 11 → 560px, Biz Dev 6 → 320px.
- Closed pods reserve their planned desk count: Blank 1 and Blank 2 = 10 desks → 480px each.
  When a chain is attached, the shutter opens and the desks appear.
- Map width grows to fit the widest row. Shorter rows are centred.
- Each pod is a room seen from above. It has a 72px back wall with a team-colour top band, a name plate with
  the headcount, and windows/clock/notice board/mail cubby on the wall. The floor is below the wall:
  Beta wood, Emails tiles, Alpha light wood, Biz Dev carpet. A team-colour door mat sits at the bottom centre.
- Seated workers stand just south of their desk, facing up. Empty desks show a chair.
- Middle row: Office Spend (left), The Brain (centre, on a vertical path), Roles Done (right).
  A small pond with tall grass sits between Office Spend and The Brain. No round bushes or trees.

RENDERING
- Use a 16x16 tile grid with integer scaling only and no sub-pixel positions.
- Use flat colours with 2–3 shades per material, dark outlines and light from the top-left. Remove all dither/checker patterns.
- Grass has a dot texture. Tall-grass tufts and flowers sway on a 2-frame steps() animation.
- Dirt paths with darker edge rows join the pods and replace the thin coloured wires.
- When the weather is cloudy, soft cloud shadows drift across the map. There is an optional evening/night tint overlay.

CHARACTERS AND MOVEMENT
- Animate walking by stepping background-position through the 4 columns (about 0.64s per cycle).
  Draw a small oval drop shadow under the feet.
- Movement is grid-locked: one tile per step, about 4 tiles per second, no diagonals.
  A character turns to face the new direction before moving. Use tile-based pathfinding along the paths.
- Idle NPCs turn to a random direction every 2–5 seconds.
- Emote bubbles appear above the head: "!" when a job arrives, "…" while working, "♪" when a role is done.

UI
- Panels use the Emerald text box style: white fill, 4px dark border, an inner light-blue ring, 12px radius,
  grey text with a 2px light shadow, and a mixed-case pixel font (Pixelify Sans).
- Office Spend uses an HP-style bar labelled SPEND. It is green, turns yellow above 50% and red above 80%.
- The Brain uses brain.png. Alternate its 2 frames every 0.6s so the rack lights blink.
  Overlay the live note count on the screen area (x 22–57, y 5–32 in sprite pixels).
  The 6 console sockets light green for each active chain.
- Roles Done is a brown badge case with 4x2 slots and one gold octagon badge per completed role.
- Closed pods show a grey roller shutter with a "Closed / No chain" sign and a padlock.
- The bottom status bar is an Emerald text box. The message types out letter by letter and a red ▼ blinks.
```
