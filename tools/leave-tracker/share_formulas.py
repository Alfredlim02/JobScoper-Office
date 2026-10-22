"""Rewrite filled-down formulas in an .xlsx as Excel shared formulas (same result, much smaller file)."""
import html
import re
import sys
import zipfile
from collections import defaultdict

from openpyxl.formula.translate import Translator

src, dst = sys.argv[1], sys.argv[2]
CELL = re.compile(r'<c r="([A-Z]+)(\d+)"([^>]*)><f>(.*?)</f><v></v></c>')


def share(xml):
    cells = [(m.group(1), int(m.group(2)), m.group(4), m.span()) for m in CELL.finditer(xml)]
    by_col = defaultdict(list)
    for col, row, f, span in cells:
        by_col[col].append((row, f, span))
    replace = {}  # span -> new xml
    si = 0
    for col, items in by_col.items():
        items.sort()
        runs, cur = [], []
        for row, f, span in items:
            if cur:
                arow, af = cur[0][0], cur[0][1]
                prev_row = cur[-1][0]
                want = Translator("=" + html.unescape(af), origin=f"{col}{arow}").translate_formula(f"{col}{row}")
                if row == prev_row + 1 and want == "=" + html.unescape(f):
                    cur.append((row, f, span))
                    continue
                runs.append(cur)
            cur = [(row, f, span)]
        if cur:
            runs.append(cur)
        for run in runs:
            if len(run) < 2:
                continue
            first, last = run[0][0], run[-1][0]
            for k, (row, f, span) in enumerate(run):
                attrs = CELL.match(xml, span[0]).group(3)
                if k == 0:
                    fx = f'<f t="shared" ref="{col}{first}:{col}{last}" si="{si}">{f}</f>'
                else:
                    fx = f'<f t="shared" si="{si}"/>'
                replace[span] = f'<c r="{col}{row}"{attrs}>{fx}<v></v></c>'
            si += 1
    out, pos = [], 0
    for span in sorted(replace):
        out.append(xml[pos:span[0]])
        out.append(replace[span])
        pos = span[1]
    out.append(xml[pos:])
    return "".join(out), si


with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename.startswith("xl/worksheets/sheet") and item.filename.endswith(".xml"):
            text, n = share(data.decode("utf-8"))
            data = text.encode("utf-8")
            print(item.filename, "shared groups:", n)
        zout.writestr(item, data)
