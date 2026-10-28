# JobScoper Leave Tracker

**Also called:** leave tracker, the tracker
**Status:** v2 live in Alfred's Google Sheet (imported 22 Oct 2026). Alfred is trialling it.
**Owner / only editor:** Alfred
**Generator:** `tools/leave-tracker/build_tracker.py` (openpyxl) + `share_formulas.py`

## History
- **Old version:** `2026_JobScoper_Leave_Tracker.xlsx`. It had a Summary tab plus 12 month tabs, with people hard-coded as columns (Alfred, I-Leng, Sam, Shamirah). Every joiner or leaver meant editing 13 tabs, which was painful with high turnover.
- **v1 (22 Oct 2026):** rebuilt around one Staff list and one Leave Log. Placeholder colours.
- **v2 (22 Oct 2026):**
  - JobScoper branding.
  - Birthday Leave fully automatic.
  - Separate Holidays 2026 and Holidays 2027 tabs.
  - Delivered as `JobScoper_Leave_Tracker_2026-2027_v2.xlsx`. Alfred imported it with "Replace spreadsheet".

## Tabs (v2)
- **How to use:** guide, including "how to apply leave" with 3 worked examples.
- **Summary 2026 / Summary 2027:** auto, one row per person employed that year.
  - KPI tiles: Headcount, On leave, Joiners, As of.
  - Columns: AL entitled / CF / taken / balance, MC, BL entitled / date / taken, AL used %, notes.
- **Calendar:** Year + Month dropdowns. Shows AL / MC / BL, ½ for half days, PH, and · for not employed. Today's date is highlighted yellow.
- **Leave Log:** the only place leave is entered.
  - Input columns: Name, Type (AL/MC), From, To, Day (Full/AM/PM), Status (Approved/Pending/Cancelled), Remarks.
  - Auto columns: Working Days, Year, ⚠ Check.
  - 500 rows.
  - Hidden helper columns K–P.
- **Staff:** Name, Position, Start Date, Last Working Day, Birthday, BL date override, Carry-Fwd into 2026, plus auto Status and Service. 30 slots.
- **Holidays 2026, Holidays 2027:** editable lists of Selangor + national PH.
- **Settings:** policy numbers, statutory tiers, the "Today override" cell (B4; keep blank), and the brand palette.
- **_calc (hidden):** per-year blocks, the calendar block, and the code→label table.
- Named ranges are used throughout (Staff_A, LeaveLog_H, Hols_2026, ALrem_2026, AutoBL_2027, …).

## Rules built in (confirmed with Alfred)
- **AL:**
  - 12 days a year.
  - Pro-rated for joiners and leavers by **completed months** (EA s.60E): 12 × months ÷ 12, with ≥ ½ day rounding up.
  - Never below the statutory minimum: 8 / 12 / 16 days for under 2 / 2–5 / 5+ years of service.
- **MC:**
  - 14 days a year, not pro-rated.
  - Auto-raised to the statutory minimum: 18 days at 2–5 years, 22 days at 5+ years. Alfred gets 18 days from 2027.
- **BL:**
  - 1 day, only if the birthday falls within employment that year.
  - Applied automatically on the birthday, or the next working day if it falls on a weekend or PH.
  - The override date wins if filled.
  - BL Taken flips to 1 once the date passes. It is never logged in the Leave Log.
  - If an AL/MC range covers the BL day, that day is not deducted.
- **Carry-forward:** MIN(6, unused AL), usable until 31 Dec of the next year. Alfred's 2025 → 2026 carry-forward was set to **0** by Alfred on 28 Oct 2026 (it was 1.5 from the old tracker).
- **Work week:** Mon–Fri, with Selangor + national PH.
- **Status:** Upcoming → New Joiner (first 3 months) → Active → Resigning (last working day set, still ahead) → Left.

## Data as of 22 Oct 2026
- **Alfred:**
  - AL taken 2026: 2 Jan, 29–30 Apr, 30 Jun (4 days). Confirmed correct, no other past leave.
  - 2026 AL: 12 + 0 carried forward = 12. With the 4 migrated days, the balance is 8 (before any leave logged after 22 Oct).
  - 2027: carry-forward is calculated as MIN(6, unused 2026 AL), so 6 if the balance stays ≥ 6. MC 18.
- **Shamirah:** 2026 AL is 4 days (4 completed months).
- **Zack:** 2026 AL is 1 day (1 completed month).
- **Birthdays:** not entered yet. Alfred will add them, and BL then applies automatically.

## Holidays
- **2026:** all confirmed, including:
  - Aidilfitri 21–22 Mar, with 23 Mar in lieu.
  - Wesak in lieu 2 Jun.
  - Silver Jubilee 25 Oct, with 26 Oct in lieu.
  - Deepavali 8 Nov, with 9 Nov in lieu.
  - Sultan of Selangor's Birthday 11 Dec.
- **2027:** fixed dates entered. The Islamic dates are marked "subject to moon sighting"; update them when they are declared.

## Things Alfred asked / was told
- **Carry-forward columns (28 Oct 2026):** Staff column G ("Carry-Fwd into 2026") is a one-time manual input for the 2025 → 2026 opening balance only. The tracker never writes into it. The 2026 → 2027 carry-forward is calculated in `_calc` and shown on Summary 2027 → Carry-Fwd. There's no manual override for it; offered to add one if Alfred wants it. Setting Settings → Max AL carry-forward to 0 turns carry-forward off for everyone.
- **Today's date:** updates automatically via TODAY(). Check that the Sheet's time zone is GMT+8 Kuala Lumpur and set recalculation to "On change and every hour". The Calendar month dropdown does not auto-advance.
- **Seeing one year at a time:** don't duplicate the Leave Log, because the formulas only read the "Leave Log" tab. Use Data → Filter views (2026 / 2027) instead.
- **Future years (2028+):** the current build hard-codes 2026/2027. Two options were proposed:
  - **Option A:** multi-year upgrade (2026–2035 built in, duplicate-and-rename Holidays tabs, a year cell on the Summary, chained carry-forward, a bigger log). Before building it, Alfred downloads the live sheet and uploads it so the Staff and Leave Log data can be migrated.
  - **Option B:** Claude adds each year on request.
  - **Alfred's decision:** keep v2 for now. **Do NOT start Option A unless Alfred explicitly asks.**

## How to rebuild / verify
```
cd tools/leave-tracker
python3 build_tracker.py v2.xlsx
python3 share_formulas.py v2.xlsx JobScoper_Leave_Tracker_2026-2027.xlsx
# recalc with the xlsx skill's scripts/recalc.py (LibreOffice), then:
python3 check.py <recalculated.xlsx>          # expect Alfred 12/0/4/8, Shamirah 4, Zack 1
python3 edge2.py - 2026 Oct e1.xlsx           # birthday/holiday edge cases (reads v2.xlsx)
```
- Formulas must stay Google-Sheets-safe:
  - No FILTER/XLOOKUP etc.
  - No cross-tab references inside conditional formatting; use local helper cells.
- Shared formulas keep the file at about 74 KB.
- Rebuilding and importing with "Replace spreadsheet" **wipes data typed into the Sheet**. Always migrate Alfred's live Staff and Leave Log data first.
