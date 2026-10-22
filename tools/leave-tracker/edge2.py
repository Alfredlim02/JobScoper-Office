import openpyxl, sys
from datetime import date
today, calyear, calmon, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
wb=openpyxl.load_workbook('v2.xlsx')
s=wb['Staff']
s['E5']=date(1988,12,5)     # Alfred: Sat 5 Dec 2026 -> Mon 7 Dec; Sun 5 Dec 2027 -> Mon 6 Dec
s['E6']=date(1995,10,26)    # Shamirah: 26 Oct 2026 is PH (in lieu) -> Tue 27 Oct
s['E7']=date(1997,3,3)      # Zack: before start in 2026 -> no BL; 2027 Wed 3 Mar
s['A8'],s['B8'],s['C8'],s['D8'],s['E8'],s['F8']='Tester','QA',date(2020,3,1),date(2026,8,18),date(1990,5,14),date(2026,5,15)
if today!='-': wb['Settings']['B4']=date.fromisoformat(today)
l=wb['Leave Log']
rows=[('Shamirah','AL',date(2026,10,26),date(2026,10,30),'Full','Approved'),   # 26 PH, 27 BL -> 3 days
      ('Alfred','AL',date(2026,12,7),None,'AM','Approved'),                     # half on BL day -> 0
      ('Zack','MC',date(2027,2,8),None,'Full','Approved'),                      # PH in lieu -> 0 days
      ('Tester','AL',date(2026,5,15),None,'Full','Approved')]                   # override BL day -> 0
for i,rw in enumerate(rows):
    for j,v in enumerate(rw): l.cell(8+i,1+j,v)
wb['Calendar']['B2']=calyear; wb['Calendar']['G2']=calmon
wb.save(out)
