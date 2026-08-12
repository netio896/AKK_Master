# 01 CAD Visual Reference v3.0

**Status:** RELEASE_CANDIDATE / CONTROLLED DOWNSTREAM REFERENCE  
**Controls:** `AKK_Master_Baseline_v3.0.md` and the four controlled engineer drawings  
**Not For:** construction approval, structural design, MEP design or statutory approval

## Confirmed geometry

- Building footprint: `110 ft x 60 ft`.
- Horizontal chain: `15 + 15 + 15 + 20 + 15 + 15 + 15 = 110 ft`.
- Depth chain: `25 + 10 + 25 = 60 ft`.
- Levels: Ground, First, Second and Roof.
- The 20 ft value is the central structural module, not a confirmed clear stair width.

## CAD production rule

Engineer drawings alone control the outline, grid, columns, stairs, walls, wet-zone positions, doors and windows. Visual overlays may supply room IDs, furniture intent, material zones and wayfinding, but may not overwrite geometry.

Ground contains Study Room, Store, Dining Area, Reception, Office, Lobby, Female Toilet, Male Toilet and Central Stair. First is Girls Hostel, 46 beds. Second is Boys Hostel, 46 beds. Each accommodation floor has ten 4-bed rooms and one 6-bed room, a 10 ft central corridor, a central stair module and west/east wet zones. Roof confirms only the principal geometry and the labels `Bath & W.C` and `Kitchen & Dining`.

## Layer discipline

- `CONFIRMED`: directly visible/dimensioned engineer geometry.
- `VISUAL`: room IDs, loose furniture, finishes, lighting and signs.
- `VERIFY`: wall thickness, construction build-ups, door/window schedules, stair clear width, structure, fire, MEP and roof unlabeled-area use.
- `MISSING`: details absent from controlled evidence.

No retired `110 ft x 66 ft`, `48 beds/floor`, `96 beds` or universal room-module data may be restored.
