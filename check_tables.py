import docx
from docx.shared import Pt

doc = docx.Document(r'C:\Users\brian\Downloads\Grupo_4_TP2_entrega_4.docx')

for ti, table in enumerate(doc.tables):
    rows = len(table.rows)
    cols = len(table.columns)
    first = table.rows[0].cells[0].text.strip()[:50] if rows > 0 else ''
    print(f'Table {ti:2d}: {rows}r x {cols}c - "{first}"')
    # Check if any cell has merged/span issues
    if rows <= 5:
        for ri, row in enumerate(table.rows):
            cells = [c.text.strip()[:25] for c in row.cells]
            print(f'       Row {ri}: {cells}')
