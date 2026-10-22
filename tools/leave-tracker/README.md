# Leave tracker generator

These scripts build **JobScoper Leave Tracker 2026–2027** (v2), which Alfred imports into his Google Sheet. Full context, rules and decisions are in `Claude memory - Leave Tracker/projects/leave-tracker.md`.

| File | Purpose |
|------|---------|
| `build_tracker.py` | Builds the workbook (openpyxl): tabs, formulas, named ranges, validation, branding |
| `share_formulas.py` | Rewrites filled-down formulas as Excel shared formulas (~74 KB instead of ~240 KB) |
| `check.py` | Prints Summary/Staff/Log/Calendar values from a recalculated file |
| `edge2.py` | Birthday-leave and holiday edge-case scenario (reads `v2.xlsx`) |

```
python3 build_tracker.py v2.xlsx
python3 share_formulas.py v2.xlsx JobScoper_Leave_Tracker_2026-2027.xlsx
```

Rebuilding does **not** include data Alfred has typed into the live Sheet. Migrate his Staff and Leave Log rows before handing over a replacement.
